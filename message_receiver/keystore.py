import os
import base64
import sys
import logging
from ConfigParser import ConfigParser
from simplecrypt import encrypt, decrypt


def get_credentials():
    secret = os.getenv('SECRET_KEY', 'my_secret_key')
    current_path = os.path.dirname(os.path.realpath(__file__))
    keystore_path = os.path.join(current_path, 'keystore')
    for f in os.listdir(keystore_path):
        if f.endswith('.ini'):
            try:
                config = ConfigParser()
                config.read(os.path.join(keystore_path, f))
                account = f[:-4]
                password = base64.b64decode(config.get('key', 'password'))
                decrypted_pass = decrypt(secret, password)
                yield account, decrypted_pass
            except Exception as e:
                logging.error('Error getting credentials: %r' % (str(e),))



if __name__ == '__main__':
    '''Utility for adding whatsapp keys'''
    if len(sys.argv) < 3:
        print('''Usage:
            python keystore.py wa_account wa_password
            python keystore.py wa_account wa_password encrypt_key

            Example
                python keystore.py 5212288227733 ExamPlE/Wq+i/KEy912qwWqabJJ=
                (Encrypt key will be taken from environment)
                python keystore.py 5212288227733 ExamPlE/Wq+i/KEy912qwWqabJJ= MyEncrYptKey
                (Encrypt key taken from param)
            ''')
        sys.exit(1)
    account = sys.argv[1]
    password = sys.argv[2]
    if len(sys.argv) == 3:
        secret = os.getenv('SECRET_KEY', 'my_secret_key') #get secret from env
    else:
        secret = sys.argv[3] #get secret by param
    current_path = os.path.dirname(os.path.realpath(__file__))
    keystore_path = os.path.join(current_path, 'keystore')
    if not os.path.exists(keystore_path):
        os.makedirs(keystore_path)
    newfile = os.path.join(keystore_path, account+'.ini')
    with open(newfile, 'w') as f:
        f.write('[key]\n')
        f.write('password='+base64.b64encode(encrypt(secret, password)))
        print('done')
