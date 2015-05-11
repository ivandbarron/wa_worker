import os
from simplecrypt import decrypt


CREDENTIALS = []
CREDENTIALS.append({
    'account': '5212281247436',
    'password': 'sc\x00\x02\xf0\xb3\x14\xad\xcb\xf6O\xfe|\x05Q{\x9f\xf7S\xe1X\xd94f%\x04\xf79\xe1\xe7\xfc\xcc`\xa6\xbf\xd3s\x8e\xe8\x8e\xafq\xf7\xb5\t=\xfd.\xca\xb4\xb7~Y\x15p\x9f\x18p\xcb\xb7\xff,J/\x9b\xc5\xc3-\x07Z\xcdB\x11\x14\xd5{F4}\x00\xb4\xbcG\xa2w\xb5O\x91i\x94\xf3T\x0f\xa5\xabY'
})
CREDENTIALS.append({
    'account': '5212281247440',
    'password': ''
})


def get_credentials():
    secret = os.getenv('SECRET_KEY', 'my_secret_key')
    for credential in CREDENTIALS:
        account = credential['account']
        password = decrypt(secret, credential['password'])
        yield account, password
