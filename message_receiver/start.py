import logging
import os
import receive
import sys
import time
import etcd


def init_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler('events.log')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s : %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)


def init_search_path():
    sys.path.append(os.path.dirname(__file__)+'/eggs')


def get_mq_params():
    etcd_endpoint = os.getenv('ETCD_ENDPOINT', '127.0.0.1')
    etcd_port = os.getenv('ETCD_PORT', '4001')
    instance = os.getenv('MQ_INSTANCE', '1')
    queue = os.getenv('MQ_QUEUE', 'WA_MESSAGE_QUEUE')
    client = etcd.Client(host=etcd_endpoint, port=etcd_port)
    service = client.read('/services/rabbitmq@'+instance).value
    return service['host'], service['port'], queue


if __name__ == '__main__':
    init_search_path()
    init_logger()
    log = logging.getLogger(__name__)
    while True:
        try:
            host, port, queue = get_mq_params()
            log.info('Trying to connect...')
            receive.from_queue(host, port, queue)
            break
        except:
            log.warn('Error with config: %s:%s %r, retry in 40 seconds' % (host, port, queue))
            time.sleep(30)
            '''TODO: replication
            log.warn('Error with config: %s:%s %r' % (host, port, queue))
            if get_slave:
                log.error('Error connecting to slave! Retry in 30 seconds')
                time.sleep(30)
            else:
                get_slave = True
            '''
