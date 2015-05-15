import logging
import keystore
import mail
from stack import SendStack
from yowsup.layers.auth import AuthError


def send_mail_to_admin(message):
    try:
        mail.send_to_admin(message)
    except Exception as e:
        logging.error('Error sending mail to admin: %r, message: %r' % (
            str(e), message))


def send_mail(mails, message):
    try:
        mail.send(mails, message)
        logging.info('Report was sent to emails: %r' % (mails,))
    except Exception as e:
        logging.error('Report was NOT sent to emails : %r, error: %r' % (
            mails, str(e)))


def send(phones, mails, message):
    messages = []
    for phone in phones:
        messages.append((phone, message))
    sucess = False
    try:
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
                error = 'Failed auth for account %s' % (account,)
                logging.warn(error)
                send_mail_to_admin(error)
            except Exception as e:
                error = 'Exception: %r, using account: %s' % (str(e), account)
                logging.error(error)
                send_mail_to_admin(error)
    except:
        pass
    if not sucess:
        logging.warn('Message not delivered by whatsapp, trying by email...')
        send_mail(mails, message)
        send_mail_to_admin('Report was sent by email!, verify the logs')
