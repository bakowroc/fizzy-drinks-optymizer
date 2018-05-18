import re

from RabbitMQ.RabbitMQ import RabbitMQ
from Store.Store import Store
from config.Config import Config

rabbit = RabbitMQ()


class Bar:
    def __init__(self):
        self.store = Store()

    def serve_drink(self, client):
        drink_name = client.decode()
        print("Serving {}".format(drink_name))
        self.store.update(drink_name)

    def read_menu(self):
        return self.store.read()

    def start(self):
        print("Bar started working")
        rabbit.consume(Config.RABBIT.QUEUES['ToBar'], lambda client: self.serve_drink(client))
