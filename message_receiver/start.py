import logging
import os
import json
import receive
import sys
import time
import etcd


def init_logger():
    logging.basicConfig(format='[%(asctime)s] %(levelname)s : %(message)s',
        datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.INFO,
        filename=os.path.join(os.path.dirname(__file__), 'events.log'))


def get_mq_params():
    etcd_endpoint = os.getenv('ETCD_ENDPOINT', '127.0.0.1')
    etcd_port = int(os.getenv('ETCD_PORT', '4001'))
    instance = os.getenv('MQ_INSTANCE', '1')
    queue = os.getenv('MQ_QUEUE', 'WA_MESSAGE_QUEUE')
    client = etcd.Client(host=etcd_endpoint, port=etcd_port)
    service = json.loads(client.read('/services/rabbitmq@'+instance).value)
    return service['host'], int(service['port']), queue


if __name__ == '__main__':
    init_logger()
    while True:
        host, port, queue = get_mq_params()
        try:
            logging.info('Service started in queue %s:%s %r...' % (
                host, port, queue))
            receive.from_queue(host, port, queue)
            break
        except KeyboardInterrupt:
            break
        except Exception as e:
            logging.warn('Error with %s:%s %r, retry in 60 seconds: %r' % (
                host, port, queue, str(e)))
            time.sleep(60)
