import os
import ConfigParser
import logging
from simplecrypt import decrypt
import pdb

def get_keystore():
    pdb.set_trace()
    current_path = os.path.dirname(os.path.realpath(__file__))
    keystore_path = os.path.join(current_path, 'keystore')
    for f in os.listdir(keystore_path):
        if f.endswith('.ini'):
            config = ConfigParser.ConfigParser()
            config.read(os.path.join(current_path, f))
            account = config.get('key', 'account', '0')
            password = config.get('key', 'password', '0')
            yield account, password


def get_credentials():
    secret = os.getenv('SECRET_KEY', 'my_secret_key')
    for account, password in get_keystore():
        pdb.set_trace()
        if account == '0':
            logging.warn('Error in keystore config, verify your keys!')
            continue
        yield account, decrypt(secret, password)
