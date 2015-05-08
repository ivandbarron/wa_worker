import pika

connection = pika.BlockingConnection(
                pika.ConnectionParameters('172.16.201.204', 8672))
channel = connection.channel()
channel.queue_declare(queue='hello')
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print " [x] Sent 'Hello World!'"
connection.close()
