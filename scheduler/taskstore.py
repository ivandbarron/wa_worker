import sys
import os
import argparse
import base64
import logging
import mysql.connector
from ConfigParser import ConfigParser
from crontab import CronTab
from simplecrypt import encrypt, decrypt
sys.path.append(os.path.join(os.getenv('MOUNT_POINT'), 'wa_worker', 'base'))
from bootstrap import get_mq_params
sys.path.append(os.path.join(os.getenv('MOUNT_POINT'), 'wa_worker', 'message_receiver', 'utilities'))
from send_message import make_body, send


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--task_name', nargs=1, required=False,
                        help='"task to execute"')
    return parser.parse_args()


def get_task_folder(name):
    current_path = os.path.dirname(__file__)
    taskstore_path = os.path.join(current_path, 'taskstore')
    return os.path.join(taskstore_path, name)


def add_task(name, cron, phones, emails, sql):
    task_folder = get_task_folder()
    if not os.path.exists(task_folder):
        os.makedirs(task_folder)
    with open(os.path.join(task_folder, 'config.ini'), 'w') as f:
        f.write('[dest]\n')
        f.write('phones=%s\n' % (','.join(phones),))
        f.write('emails=%s\n' % (','.join(emails),))
    with open(os.path.join(task_folder, 'query.sql'), 'w') as f:
        f.write(sql)
    cron = CronTab(user=True)
    job = cron.new(command='/usr/bin/python '+__file__+' --task_name '+name)
    job.set_comment(name)
    job.setall(' '.join(cron))
    cron.write_to_user(user=True)


def get_config():
    secret = os.getenv('SECRET_KEY', 'my_secret_key')
    current_path = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser()
    config.read(os.path.join(current_path, 'taskstore.ini'))
    host = base64.b64decode(config.get('db_connection', 'host'))
    user = base64.b64decode(config.get('db_connection', 'user'))
    password = base64.b64decode(config.get('db_connection', 'password'))
    db = base64.b64decode(config.get('db_connection', 'db'))
    return (decrypt(secret, host),
        decrypt(secret, user),
        decrypt(secret, password),
        decrypt(secret, db))


def extract_queries(filename):
    with open(filename) as file_obj:
        buffer = ''
        for line in file_obj:
            if line == '\n' or line.startswith('#'):
                continue
            buffer += line.replace('%','%%')
            if line.endswith(';\n') or line.endswith(';'):
                yield buffer
                buffer = ''


def do_sql(sqlfile):
    host, user, password, db = get_config()
    conn = None
    try:
        conn = mysql.connector.connect(user=user, password=password, host=host,
                                     database=db, charset='latin1',
                                     use_unicode=True)
        cursor = conn.cursor()
        for query in extract_queries(sqlfile):
            cursor.execute((query,))
        row = cursor.fetchone() # Last column always do a select
        if row:
            '''if type(resultado) is not str:
                message += resultado.decode() + '\n\n'
            else:
                message += resultado + '\n\n'''
            return row[0]+'\n\n'
        else:
            logging.warn("Last query does not return any results")
    finally:
        if conn:
            conn.close()


def get_dest(task_folder):
    config = ConfigParser()
    config.read(os.path.join(task_folder, 'config.ini'))
    phones = (config.get('dest', 'phones')).split(',')
    emails = (config.get('dest', 'emails')).split(',')
    return phones, emails


def get_sql(task_folder):
    return os.path.join(task_folder, 'query.sql')


def run_task(name):
    task_folder = get_task_folder()
    phones, emails = get_dest(task_folder)
    sqlfile = get_sql(task_folder)
    result = do_sql(sqlfile)
    body = make_body(phones, emails, result.replace('\n', '#13'))
    host, port, queue = get_mq_params('MQ_SEND_MESSAGE_QUEUE')
    send(host, port, queue, body)


def config_taskstore():
    if len(sys.argv) < 5:
        print('''Usage for configure exec_task.ini for database connection:
            python taskstore.py host user password database
            python taskstore.py host user password database encrypt_key

            Example:
                python taskstore.py 172.16.16.16 root xFGt3Swq test
                (Encrypt key will be taken from environment)
                python taskstore.py 172.16.16.16 root xFGt3Swq test MyEncrYptKey
                (Encrypt key taken from param)
              ''')
        sys.exit(1)
    host = sys.argv[1]
    user = sys.argv[2]
    password = sys.argv[3]
    db = sys.argv[4]
    if sys.argv == 5:
        secret = os.getenv('SECRET_KEY', 'my_secret_key') #get secret from env
    else:
        secret = sys.argv[5] #get secret by param
    current_path = os.path.dirname(os.path.realpath(__file__))
    newfile = os.path.join(current_path, 'exec_task.ini')
    with open(newfile, 'w') as f:
        f.write('[db_connection]\n')
        f.write('host='+base64.b64encode(encrypt(secret, host))+'\n')
        f.write('user='+base64.b64encode(encrypt(secret, user))+'\n')
        f.write('password='+base64.b64encode(encrypt(secret, password))+'\n')
        f.write('db='+base64.b64encode(encrypt(secret, db)))
        print('done')


if __name__ == '__main__':
    args = get_args()
    if args.task_name:
        run_task(args.taskname[0])
    else:
        config_taskstore()
