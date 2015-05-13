import pika

conn = pika.BlockingConnection(
    pika.ConnectionParameters('172.16.201.204',8672)
)
channel = conn.channel()
channel.queue_declare(queue='WA_MESSAGE_QUEUE')
msg = '''{
    "phones": ["5212287779788"],
    "mails": ["dbarron@crediland.com.mx"],
    "msg": "test"
}'''
channel.basic_publish(exchange='', routing_key='WA_MESSAGE_QUEUE', body=msg)
conn.close()
