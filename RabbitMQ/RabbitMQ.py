from config.Config import Config
from pika import BlockingConnection, ConnectionParameters, PlainCredentials


class RabbitMQ:
    def __init__(self):
        credentials = PlainCredentials('rabbitmq', 'rabbitmq')
        connection_parameters = ConnectionParameters(Config.RABBIT.HOST, Config.RABBIT.PORT, '/', credentials)
        self.connection = BlockingConnection(connection_parameters)
        self.channel = self.connection.channel()

    def callback(self, method, body, interpreter):
        try:
            interpreter(body)
        except EnvironmentError:
            raise Exception('Bad interpreter')
        finally:
            self.channel.basic_ack(delivery_tag=method.delivery_tag)

    def publish(self, body: str, queue_name: str):
        self.channel.queue_declare(queue_name)
        self.channel.basic_publish(exchange='', routing_key=queue_name, body=body)

    def consume(self, queue_name: str, interpreter: lambda: str, ):
        callback = lambda ch, method, properties, body: self.callback(method, body, interpreter)

        self.channel.queue_declare(queue_name)
        self.channel.basic_consume(callback, queue=queue_name, no_ack=False)
        self.channel.start_consuming()
