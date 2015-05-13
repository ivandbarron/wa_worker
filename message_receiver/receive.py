import json
import pika
import messenger
import logging
import pdb
log=logging.getLogger(__name__)

def callback(ch, method, properties, body):
    ''' "body" debe contener el siguiente json
    {
        "phones": ["5212287779788", "5212287779789"],
        "mails": ["ivandavid77@gmail.com","dbarron@crediland.com.mx"]
        "msg": "algun mensaje#13con varias#13lineas"
    } '''
    try:
        _d = json.loads(body)
        messenger.send(_d['phones'], _d['mails'], _d['msg'].replace('#13', '\n'))
    except Exception as e:
        log.warn('Sending problem: %r' % (str(e),))
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        log.info('Message was processed\n')


def from_queue(host, port, queue):
    conn = pika.BlockingConnection(pika.ConnectionParameters(host, port))
    channel = conn.channel()
    channel.queue_declare(queue=queue)
    channel.basic_consume(callback, queue=queue)
    channel.start_consuming()
