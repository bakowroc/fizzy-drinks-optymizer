import json
from threading import Thread
from Client.Client import Client
from RabbitMQ.RabbitMQ import RabbitMQ
from config.Config import Config


class Cancer(Thread):
    def __init__(self, clients: [Client], rabbit: RabbitMQ):
        super(Cancer, self).__init__()
        self.clients = clients
        self.rabbit = rabbit

    def run(self):
        while False in map(lambda client: client.cancelled, self.clients):
            pass
        self.rabbit.publish(json.dumps({'message': 'STOP'}), Config.RABBIT.QUEUES['ToBar'])

