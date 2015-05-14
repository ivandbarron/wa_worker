import logging
import keystore
import mail
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
            logging.warn('Failed auth for account %s' % (account,))
        except Exception as e:
            logging.error('Exception: %r, for account: %s' % (str(e), account))
    if not sucess:
        logging.warn('Message not delivered by whatsapp, trying by email...')
        try:
            mail.send(mails, message)
            logging.info('Message sended to emails: %r' % (mails,))
        except Exception as e:
            logging.error('Message was not sended :' % (str(e),))
