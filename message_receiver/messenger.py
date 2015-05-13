import logging
import keystore
from stack import SendStack
from yowsup.layers.auth import AuthError


def send(phones, mails, message):
    messages = []
    for phone in phones:
        messages.append((phone, message))
    sucess = False
    for account, password in keystore.get_credentials():
        credentials = (account, password)
        try:
            stack = SendStack(credentials, messages)
            try:
                stack.start()
            except KeyboardInterrupt:
                sucess = True
            break
        except AuthError:
            logging.warn('Failed auth for account %s' % account)
        except Exception as e:
            logging.error('Exception using yowsup library: %r, for account: %s' %(
                str(e), account))
    if not sucess:
        logging.error('Message was not delivered')
        #TODO: send email
