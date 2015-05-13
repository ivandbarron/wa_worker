import logging
import keystore
from stack import SendStack
from yowsup.layers.auth import AuthError


def send(phones, mails, message):
    log = logging.getLogger(__name__)
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
            log.warn('Failed auth for account %s' % account)
        except Exception as e:
            log.error('Exception using yowsup library: %r, for account: %s' %(
                str(e), account))
    if not sucess:
        log.error('Message was not delivered')
        #TODO: send email
