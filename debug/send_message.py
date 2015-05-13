import os
import sys
import json
import pika
import etcd


if len(sys.argv) < 2:
    msg = '''{
        "phones": ["5212287779788"],
        "mails": ["dbarron@crediland.com.mx"],
        "msg": "test with newline#13test again"
    }'''
else:
    msg = sys.argv[1]
    try:
        _json = json.loads(msg)
        if not 'phones' in _json or
            not 'mails' in _json or
            not 'msg' in _json or
            not type(_json['phones']) == list or
            not type(_json['mails']) == list or
            not type(_json['msg']) == str:
            raise Exception()
    except:
        print('Invalid format for message')
        sys.exit(1)
etcd_endpoint = os.getenv('ETCD_ENDPOINT', '127.0.0.1')
etcd_port = int(os.getenv('ETCD_PORT', '4001'))
instance = os.getenv('MQ_INSTANCE', '1')
queue = os.getenv('MQ_QUEUE', 'WA_MESSAGE_QUEUE')
client = etcd.Client(host=etcd_endpoint, port=etcd_port)
service = json.loads(client.read('/services/rabbitmq@'+instance).value)
conn = pika.BlockingConnection(
    pika.ConnectionParameters(service['host'],int(service['port'])))
channel = conn.channel()
channel.queue_declare(queue=queue)
channel.basic_publish(exchange='', routing_key=queue, body=msg)
conn.close()
