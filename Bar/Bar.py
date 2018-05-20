import json
import time

from Client.Client import Client
from Drink.Drink import Drink
from RabbitMQ.RabbitMQ import RabbitMQ
from Store.Store import Store
from config.Config import Config

rabbit = RabbitMQ()


class Bar:
    def __init__(self, clients: [Client]):
        self.store = Store()
        self.clients = clients

    def get_drink_instance(self, drink_name: str) -> (int, Drink):
        for stored_drink in self.store.read():
            (count, drink) = stored_drink

            if drink.name == drink_name:
                return stored_drink

    def get_current_client(self, name: str) -> Client:
        return next((client for client in self.clients if client.name == name), None)

    def serve_drink(self, drink: Drink) -> None:
        print("Serving {}.".format(drink.name))
        self.store.update(drink)

    def deal_with_client(self, order: bytes) -> None:
        print(15*'-')
        current_client = self.get_current_client(json.loads(order.decode())['client_name'])
        (drink_count, drink) = self.get_drink_instance(json.loads(order.decode())['drink'])

        if drink_count:
            self.serve_drink(drink)
            current_client.drink(drink)
        else:
            print("Cannot serve {}. No drinks available".format(drink.name))
            current_client.start_again()

        time.sleep(5)

    def start(self) -> None:
        print("Bar started working")
        rabbit.consume(Config.RABBIT.QUEUES['ToBar'], self.deal_with_client)
