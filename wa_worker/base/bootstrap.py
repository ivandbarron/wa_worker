import logging
import os
import json
import sys
import time
import etcd
import pika


def get_mq_params(mq_name):
    etcd_endpoint = os.getenv('ETCD_ENDPOINT', '127.0.0.1')
    etcd_port = int(os.getenv('ETCD_PORT', '4001'))
    instance = os.getenv('MQ_INSTANCE', '1')
    queue = os.getenv(mq_name, 'MESSAGE_QUEUE')
    #client = etcd.Client(host=etcd_endpoint, port=etcd_port)
    #service = json.loads(client.read('/services/rabbitmq@'+instance).value)
    #return service['host'], int(service['port']), queue
    return etcd_endpoint, 8672, queue


def receive_from_queue(host, port, queue, callback):
    conn = pika.BlockingConnection(pika.ConnectionParameters(host, port))
    channel = conn.channel()
    channel.queue_declare(queue=queue)
    channel.basic_consume(callback, queue=queue)
    channel.start_consuming()


def start(mq_name, callback):
    while True:
        host, port, queue = get_mq_params(mq_name)
        try:
            logging.info('Service started in queue %s:%s %r...' % (
                host, port, queue))
            receive_from_queue(host, port, queue, callback)
            break
        except KeyboardInterrupt:
            break
        except Exception as e:
            logging.warn('Error with %s:%s %r, retry in 60 seconds: %r' % (
                host, port, queue, str(e)))
            time.sleep(60)
