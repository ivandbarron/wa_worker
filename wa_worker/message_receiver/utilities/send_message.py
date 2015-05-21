import os
import sys
import json
import argparse
import pika


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--phones', nargs='+', help='phone list')
    parser.add_argument('--mails', nargs='+', help='mail list')
    parser.add_argument('--msg', nargs=1, required=True,
                    help='"message to send"')
    return parser.parse_args()


def make_body(phones, mails, msg):
    return '{"phones":[%s], "mails":[%s], "msg": "%s"}' % (
        ','.join(['"%s"' % (p,) for p in phones]),
        ','.join(['"%s"' % (m,) for m in mails]),
        msg.replace('\n', '#13'))


def send(host, port, queue, body):
    conn = pika.BlockingConnection(pika.ConnectionParameters(host, port))
    channel = conn.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange='', routing_key=queue, body=body)
    conn.close()


if __name__ == '__main__':
    args = get_args()
    body = make_body(args.phones, args.emails, args.msg[0])
    sys.path.append(os.path.join(os.getenv('MOUNT_POINT'), 'wa_worker', 'base'))
    import bootstrap
    host, port, queue = bootstrap.get_mq_params('MQ_SEND_MESSAGE_QUEUE')
    send(host, port, queue, body)
