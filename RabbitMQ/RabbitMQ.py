from config.Config import Config
from pika import BlockingConnection, ConnectionParameters, PlainCredentials


class RabbitMQ:
    def __init__(self):
        credentials = PlainCredentials('rabbitmq', 'rabbitmq')
        connection_parameters = ConnectionParameters(Config.RABBIT.HOST, Config.RABBIT.PORT, '/', credentials)
        self.connection = BlockingConnection(connection_parameters)
        self.channel = self.connection.channel()

    def publish(self, body, queue_name):
        self.channel.queue_declare(queue_name)
        self.channel.basic_publish(exchange='', routing_key=queue_name, body=body)
        self.connection.close()

    def consume(self, queue_name, interpreter):
        callback = lambda ch, method, properties, body: interpreter(body)

        self.channel.queue_declare(queue_name)
        self.channel.basic_consume(callback, queue=queue_name, no_ack=True)
        self.channel.start_consuming()
        self.connection.close()