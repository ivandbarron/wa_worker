import json
import pika
import messenger
import logging


def callback(ch, method, properties, body):
    ''' "body" debe contener el siguiente json
    {
        "phones": ["5212287779788", "5212287779789"],
        "mails": ["ivandavid77@gmail.com","dbarron@crediland.com.mx"]
        "msg": "algun mensaje#13con varias#13lineas"
    } '''
    _d = json.loads(body)
    messenger.send(_d['phones'], _d['mails'], _d['msg'].replace('#13', '\n'))
    ch.basic_ack(delivery_tag=method.delivery_tag)
    logging.getLogger(__name__).info('Message was processed\n')


def from_queue(host, port, queue)
    conn = pika.BlockingConnection(pika.ConnectionParameters(server, port))
    channel = conn.channel()
    channel.queue_declare(queue=queue)
    channel.basic_consume(callback, queue=queue)
    logging.get_logger(__name__).info('Sucess')
    channel.start_consuming()
