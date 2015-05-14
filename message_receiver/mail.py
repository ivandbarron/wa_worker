import sys
import os
import base64
import logging
from ConfigParser import ConfigParser
from simplecrypt import encrypt, decrypt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import COMMASPACE, formatdate


def get_config():
    secret = os.getenv('SECRET_KEY', 'my_secret_key')
    current_path = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser()
    config.read(os.path.join(current_path, 'mail.ini'))
    host = base64.b64decode(config.get('smtp', 'host'))
    user = base64.b64decode(config.get('smtp', 'user'))
    password = base64.b64decode(config.get('smtp', 'password'))
    admin = base64.b64decode(config.get('smtp', 'admin'))
    return (decrypt(secret, host),
        decrypt(secret, user),
        decrypt(secret, password),
        decrypt(secret, admin))


def connect_to_smtp(host, user, password):
    intents = 5
    while True:
        try:
            logging.info('Connecting to server %s' % (host,))
            conn = smtplib.SMTP(host)
            conn.login(user, password)
            return conn
        except smtplib.SMTPException as e:
            logging.warn('Connection error: %r' % (str(e),))
            logging.info('Trying in 5 sec.')
            time.sleep(5)
            intents -= 1
        if intents <= 0:
            raise Exception('Could not connect to smtp server!')


def send(rcpt, message):
    host, user, password, admin = get_config()
    mail = MIMEMultipart()
    mail['From'] = user
    mail['To'] = COMMASPACE.join(rcpt)
    mail['Date'] = formatdate(localtime = True)
    mail['Subject'] = 'reporte'
    mail.attach(MIMEText(message))
    conn = connect_to_smtp(host, user, password)
    logging.info('Sending to emails: '+', '.join(rcpt))
    result = conn.sendmail(user, rcpt, mail.as_string())
    for mail in result.keys():
        try:
            logging.error('Error sending to %r: %s' % (mail, result[mail][1]))
        except:
            pass
    # Now send report to admin
    mail['To'] = admin
    mail['Subject'] = 'Error sending whatsapp'
    mail.attach(MIMEText('Verify log, error sending whatsapp! Sent by email'))
    conn.sendmail(user, [admin], mail.as_string())
    conn.close()


if __name__ == '__main__':
    '''Utility for configure email messenger backout'''
    if len(sys.argv) < 5:
        print('''Usage:
            python mail.py host user password admin
            python mail.py host user password admin encrypt_key

            Example:
                python mail.py 172.16.16.16 fallout@mydomain.com xFGt3Swq support@devops.mydomain.com
                (Encrypt key will be taken from environment)
                python mail.py 172.16.16.16 fallout@mydomain.com xFGt3Swq support@devops.mydomain.com MyEncrYptKey
                (Encrypt key taken from param)
              ''')
        sys.exit(1)
    host = sys.argv[1]
    user = sys.argv[2]
    password = sys.argv[3]
    admin = sys.argv[4]
    if sys.argv == 5:
        secret = os.getenv('SECRET_KEY', 'my_secret_key') #get secret from env
    else:
        secret = sys.argv[5] #get secret by param
    current_path = os.path.dirname(os.path.realpath(__file__))
    newfile = os.path.join(current_path, 'mail.ini')
    with open(newfile, 'w') as f:
        f.write('[smtp]\n')
        f.write('host='+base64.b64encode(encrypt(secret, host))+'\n')
        f.write('user='+base64.b64encode(encrypt(secret, user))+'\n')
        f.write('password='+base64.b64encode(encrypt(secret, password))+'\n')
        f.write('admin='+base64.b64encode(encrypt(secret, admin)))
        print('done')
