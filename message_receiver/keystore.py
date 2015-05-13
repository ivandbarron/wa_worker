import os
import ConfigParser
import base64
import sys
import logging
from simplecrypt import encrypt, decrypt


def get_keystore():
    current_path = os.path.dirname(os.path.realpath(__file__))
    keystore_path = os.path.join(current_path, 'keystore')
    for f in os.listdir(keystore_path):
        if f.endswith('.ini'):
            config = ConfigParser.ConfigParser()
            config.read(os.path.join(keystore_path, f))
            account = f[:-4]
            password = base64.b64decode(config.get('key', 'password'))
            yield account, password


def get_credentials():
    secret = os.getenv('SECRET_KEY', 'my_secret_key')
    for account, password in get_keystore():
        yield account, decrypt(secret, password)


if __name__ == '__main__':
    '''Utility for adding whatsapp keys'''
    if len(sys.argv) < 4:
        print('Usage: $python keystore.py wa_account wa_password master_key')
        sys.exit(1)
    account = sys.argv[1]
    password = sys.argv[2]
    secret = sys.argv[3]
    current_path = os.path.dirname(os.path.realpath(__file__))
    keystore_path = os.path.join(current_path, 'keystore')
    if not os.path.exists(keystore_path):
        os.makedirs(keystore_path)
    newfile = os.path.join(keystore_path, account+'.ini')
    with open(newfile, 'w') as f:
        f.write('[key]\n')
        f.write('password='+base64.b64encode(encrypt(secret, password)))
        print('done')
