import json
import time

from Client.Client import Client
from Drink.Drink import Drink
from RabbitMQ.RabbitMQ import RabbitMQ
from Store.Store import Store
from config.Config import Config

rabbit = RabbitMQ()


class Bar:
    def __init__(self, clients: [Client], store: Store):
        self.store = store
        self.clients = clients
        self.runtime_flag: bool = True

    def get_drink_instance(self, drink_name: str) -> (int, Drink):
        for stored_drink in self.store.read():
            (_, drink) = stored_drink

            if drink.name == drink_name:
                return stored_drink

    def get_current_client(self, name: str) -> Client:
        return next((client for client in self.clients if client.name == name), None)

    def serve_drink(self, drink: Drink) -> None:
        # print("Serving {}.".format(drink.name))
        self.store.update(drink)

    def deal_with_client(self, order: bytes) -> None:
        if 'message' in json.loads(order.decode()) is not None:
            print('Drawing chart')
            Client.draw()
            exit(0)

        time.sleep(0.01)
        current_client = self.get_current_client(json.loads(order.decode())['client_name'])
        drink_tuple = self.get_drink_instance(json.loads(order.decode())['drink'])

        if drink_tuple and current_client:
            (_, drink) = drink_tuple
            self.serve_drink(drink)
            current_client.drink(drink)
        elif current_client:
            # print("Cannot serve. No drinks available")
            current_client.start_over(self.store.is_empty())

        self.runtime_flag = False

        for client in self.clients:
            if client.cancelled is False:
                self.runtime_flag = True

        if not self.runtime_flag:
            rabbit.channel.basic_cancel('')

    def start(self) -> None:
        print("Bar started working")
        rabbit.consume(Config.RABBIT.QUEUES['ToBar'], self.deal_with_client)
