import json
import time

from Client.Client import Client
from RabbitMQ.RabbitMQ import RabbitMQ
from Store.Store import Store
from config.Config import Config

rabbit = RabbitMQ()


class Bar:
    def __init__(self, clients: [Client]):
        self.store = Store()
        self.clients = clients

    def is_able_to_serve(self, drink: str) -> bool:
        return next((True for stored_drink in self.store.read() if stored_drink[1].name == drink), False)

    def get_current_client(self, name: str) -> Client:
        return next((client for client in self.clients if client.name == name), None)

    def serve_drink(self, drink: str) -> bool:
        is_store_has_enough = self.is_able_to_serve(drink)

        if is_store_has_enough:
            print("Serving {}.".format(drink))
            self.store.update(drink)
        else:
            print("Cannot serve {}. No drinks available".format(drink))

        return is_store_has_enough

    def deal_with_client(self, order: bytes) -> None:
        print(15*'-')
        drink = json.loads(order.decode())['drink']
        client_name = json.loads(order.decode())['client_name']

        current_client = self.get_current_client(client_name)
        is_success = self.serve_drink(drink)

        if is_success:
            current_client.drink(drink)
        else:
            current_client.start_again()

        time.sleep(5)

    def start(self) -> None:
        print("Bar started working")
        rabbit.consume(Config.RABBIT.QUEUES['ToBar'], lambda order: self.deal_with_client(order))
