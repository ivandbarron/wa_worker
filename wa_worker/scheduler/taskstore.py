import logging
import os
def init_logger(log_name, debug=False):
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(format='[%(asctime)s] %(levelname)s : %(message)s',
        datefmt='%d/%m/%Y %I:%M:%S %p', level=level, filename=log_name)
init_logger(os.path.join(os.path.dirname(__file__), 'taskstore.log'), True)
import sys
import argparse
import base64
import mysql.connector
from ConfigParser import ConfigParser
from crontab import CronTab
from simplecrypt import encrypt, decrypt
try:
    logging.info('Name value:'+__name__)
    logging.info('Importing bootstrap / send_message')
    logging.info('A) MOUNT_POINT value: '+str(os.getenv('MOUNT_POINT')))
    from wa_worker.base import bootstrap
    from wa_worker.message_receiver.utilities import send_message
    logging.info('imported')
except Exception as e:
    logging.info('Exception: '+str(e))
    sys.path.append(os.path.join(os.getenv('MOUNT_POINT'), 'wa_worker'))
    from wa_worker.base import bootstrap
    from wa_worker.message_receiver.utilities import send_message

logging.info('Here')
logging.info('B) MOUNT_POINT value: '+str(os.getenv('MOUNT_POINT')))
logging.info('Here 2')

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--task', nargs=1, required=True,
                        help='"task to execute"')
    parser.add_argument('--debug', action='store_true')
    return parser.parse_args()


def get_task_folder(name):
    current_path = os.path.dirname(__file__)
    taskstore_path = os.path.join(current_path, 'taskstore')
    return os.path.join(taskstore_path, name)


def add_task(name, cron, phones, mails, sql):
    task_folder = get_task_folder(name)
    if not os.path.exists(task_folder):
        os.makedirs(task_folder)
    with open(os.path.join(task_folder, 'config.ini'), 'w') as f:
        f.write('[dest]\n')
        f.write('phones=%s\n' % (','.join(phones),))
        f.write('mails=%s\n' % (','.join(mails),))
    with open(os.path.join(task_folder, 'query.sql'), 'w') as f:
        f.write(sql)
    crond = CronTab(user=True)
    job = crond.new(command='/usr/bin/python '+__file__+' --task '+name)
    job.set_comment(name)
    job.setall(cron)
    crond.write_to_user(user=True)


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
            cursor.execute(query)
        row = cursor.fetchone() # Last column always do a select
        if row:
            if type(row[0]) is not str:
                msg = row[0].decode()
            else:
                msg = row[0]
            return msg.replace('%%', '%')+'\n\n'
        else:
            return None
    finally:
        if conn:
            conn.close()


def get_dest(task_folder):
    config = ConfigParser()
    config.read(os.path.join(task_folder, 'config.ini'))
    phones = (config.get('dest', 'phones')).split(',')
    mails = (config.get('dest', 'mails')).split(',')
    return phones, mails


def get_sql(task_folder):
    return os.path.join(task_folder, 'query.sql')


def run_task(name):
    task_folder = get_task_folder(name)
    logging.info('task folder: '+task_folder)
    phones, mails = get_dest(task_folder)
    sqlfile = get_sql(task_folder)
    result = do_sql(sqlfile)
    if result:
        body = send_message.make_body(phones, mails, result)
    else:
        body = send_message.make_body(phones, mails, 'Task %r was executed' %
                                      (name,))
    host, port, queue = bootstrap.get_mq_params('MQ_SEND_MESSAGE_QUEUE')
    send_message.send(host, port, queue, body)


def config_taskstore():
    if len(sys.argv) < 5:
        print('''Usage for configure taskstore.ini for database connection:
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
    if len(sys.argv) == 5:
        secret = os.getenv('SECRET_KEY', 'my_secret_key') #get secret from env
    else:
        secret = sys.argv[5] #get secret by param
    current_path = os.path.dirname(os.path.realpath(__file__))
    newfile = os.path.join(current_path, 'taskstore.ini')
    with open(newfile, 'w') as f:
        f.write('[db_connection]\n')
        f.write('host='+base64.b64encode(encrypt(secret, host))+'\n')
        f.write('user='+base64.b64encode(encrypt(secret, user))+'\n')
        f.write('password='+base64.b64encode(encrypt(secret, password))+'\n')
        f.write('db='+base64.b64encode(encrypt(secret, db)))
        print('done')


#def init_logger(log_name, debug=False):
#    level = logging.DEBUG if debug else logging.INFO
#    logging.basicConfig(format='[%(asctime)s] %(levelname)s : %(message)s',
#        datefmt='%d/%m/%Y %I:%M:%S %p', level=level, filename=log_name)


if __name__ == '__main__':
    logging.info('argv value: %r' %(str(sys.argv),))
    if len(sys.argv) == 1:
        config_taskstore()
    else:
        args = get_args()
        #init_logger(os.path.join(os.path.dirname(__file__), 'taskstore.log'),
        #            args.debug)
        run_task(args.task[0])
