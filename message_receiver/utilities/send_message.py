import os
import sys
import json
import argparse
import pika
from wa_worker.base.bootstrap import get_mq_params


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--phones', nargs='+', help='phone list')
    parser.add_argument('--emails', nargs='+', help='email list')
    parser.add_argument('--message', nargs=1, required=True,
                    help='"message to send"')
    return parser.parse_args()


def make_body(phones, emails, message):
    return '{"phones":[%s], "emails":[%s], "message": "%s"}' % (
        ','.join(['"%s"' % (p,) for p in phones]),
        ','.join(['"%s"' % (e,) for e in emails]),
        message)


def send(host, port, queue, body):
    conn = pika.BlockingConnection(pika.ConnectionParameters(host, port))
    channel = conn.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange='', routing_key=queue, body=body)
    conn.close()


if __name__ == '__main__':
    args = get_args()
    body = make_body(args.phones, args.emails, args.message[0])
    host, port, queue = get_mq_params('MQ_SEND_MESSAGE_QUEUE')
    send(host, port, queue, body)
