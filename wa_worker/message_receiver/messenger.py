import logging
import time
import keystore
import mail
from stack import SendStack
from yowsup.layers.auth import AuthError


def send_mail_to_admin(msg):
    try:
        mail.send_to_admin(msg)
    except Exception as e:
        logging.error('Error sending mail to admin: %r, message: %r' % (
            str(e), msg))


def send_mail(mails, msg):
    try:
        mail.send(mails, msg)
        logging.info('Report was sent to emails: %r' % (mails,))
    except Exception as e:
        logging.error('Report was NOT sent to emails : %r, error: %r' % (
            mails, str(e)))


def send_wa(account, password, messages):
    intents = 2
    sucess = False
    sleep = False
    while not sucess and intents >= 1:
        if sleep:
            time.sleep(60)
        try:
            stack = SendStack((account, password), messages)
            try:
                stack.start()
            except KeyboardInterrupt: #Sucess!
                sucess = True
        except AuthError:
            if intents == 2: #First time that happen in this session
                logging.warn('Failed auth for account %r, retrying in 1 min.' %
                             (account,))
                sleep = True
                intents -= 1
            else:
                error = 'Failed auth for account %s' % (account,)
                logging.warn(error)
                send_mail_to_admin(error)
                break
        except Exception as e:
            error = 'Exception: %r, using account: %s' % (str(e), account)
            logging.error(error)
            send_mail_to_admin(error)
            intents -= 1
    return sucess


def send(phones, mails, msg):
    messages = []
    for phone in phones:
        messages.append((phone, msg))
    sucess = False
    generator = keystore.get_credentials()
    while not sucess:
        try:
            account, password = next(generator)
            sucess = send_wa(account, password, messages)
        except StopIteration:
            break
        except Exception as e:
            error = 'Error in local keystore: %r' % (str(e),)
            logging.error(error)
            send_mail_to_admin(error)
            continue
    if not sucess:
        logging.warn('Message not delivered by whatsapp, trying by email...')
        send_mail(mails, msg)
        send_mail_to_admin('Report was sent by email!, verify the logs')
