import pika

def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)

connection = pika.BlockingConnection(
                pika.ConnectionParameters('172.16.201.204', 8672))
channel = connection.channel()
channel.queue_declare(queue='hello')
channel.basic_consume(callback, queue='hello',no_ack=True)
print ' [*] Waiting for messages. To exit press CTRL+C'
channel.start_consumming()
