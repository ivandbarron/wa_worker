import os
import json
import sys
import uuid
import pika
import argparse
from RpcClient import RpcClient


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', nargs=1, required=True, help='"task name"')
    parser.add_argument('--phones', nargs='+', help='phone list')
    parser.add_argument('--emails', nargs='+', help='email list')
    parser.add_argument('--cron', nargs=1, required=True,
                        help='one string with cron schedule')
    parser.add_argument('--sql_file', nargs=1, required=True,
                        help='path to sql file')
    parser.add_argument('--params', nargs='*',
                        help='param list for sql script file')
    return parser.parse_args()


def sanitize_params(params):
    '''Example ("@" is for var declaration, "#" is for replace content inside sql query):
    --params @FECHA_ACTUAL=CURDATE()   "@FECHA_ANTERIOR=DATE_SUB(@FECHA_ACTUAL,INTERVAL 364 DAY)"   "@LEYENDA=CONCAT('Del mismo dia en la semana ',WEEK(@FECHA_ACTUAL,6),' del anio')"   "#FILTROS=v.clave_muebleria NOT LIKE 'TCI%' AND v.clave_muebleria NOT IN ('TC00','TC96','TC43','TC99')"
    '''
    dparams = {p.split('=',1)[0]: p.split('=',1)[1] for p in params}
    sql_vars = []
    sql_replace = []
    for key, value in dparams:
        if key.startswith('@'):
            sql_vars.append((sanitize(key), sanitize(value)))
        elif key.startswith('#'):
            sql_replace.append((sanitize(key), sanitize(value)))
    return sql_vars, sql_replace


def sanitize(text):
    return ((text.replace('"', '\"')).replace('\n', '#13')).replace('%', '%%')


def make_body(name, phones, mails, cron, sql_file, params):
    with open(sql_file) as f:
        sql = ''.join([sanitize(line) for line in f])
    sql_vars, sql_replace = sanitize_params(params)
    for key, value in sql_replace:
        sql = sql.replace(key, value)
    for key, value in sql_vars:
        sql = 'SELECT %s INTO %s;#13' % (value, key) + sql
    return '''{
"operation": "add",
"task_name": "%s",
"phones": [%s],
"mails": [%s],
"cron": [%s]
"sql": "%s"}''' % (
        sanitize(name),
        ','.join(['"%s"' % (p,) for p in phones]),
        ','.join(['"%s"' % (e,) for e in emails]),
        cron,
        sql)


if __name__ == '__main__':
    args = get_args()
    body = make_body(args.name[0], args.phones, args.emails, args.cron[0],
                     args.sql_file[0], args.params)
    sys.append(os.path.join(os.getenv('MOUNT_POINT'), 'wa_worker'))
    from wa_worker.base.bootstrap import get_mq_params
    host, port, queue = get_mq_params('MQ_TASK_MANAGEMENT_QUEUE')
    rpc = RpcClient(host, port)
    print(rpc.call(body, queue))
