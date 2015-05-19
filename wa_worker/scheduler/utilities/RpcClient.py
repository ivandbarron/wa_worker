import pika
import uuid

class RpcClient(object):
    def __init__(self, host, port):
        self.conn = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port))
        self.channel = self.conn.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, body, queue):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='', routing_key=queue,
                             properties=pika.BasicProperties(
                                reply_to=self.callback_queue,
                                correlation_id=self.corr_id,
                                ),
                             body=body)
        while self.response is None:
            self.conn.process_data_events()
        return self.response
