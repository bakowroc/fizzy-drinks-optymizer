import json
import time

from Client.Client import Client
from Drink.Drink import Drink
from RabbitMQ.RabbitMQ import RabbitMQ
from Store.Store import Store
from config.Config import Config

rabbit = RabbitMQ()


class Bar:
    """
        ROSZKO_KOMENT
        to co dodałem za hashami jest moje.
        Idea jest taka:
            lista symuluje kolejke.
            Klasa EventWorker wytrzeźwia ludzi (bo jest złośliwa :D)
            wybiera najlepsze trunki,
            następnie dodaje do obiektu kolejki (listy) dodając elementy na koniec
            natomiast klasa bar zrzuca elementy ze stosu wyjmujac pierwszy element (zeby nie było kolizji)
            za pomocą klasy BarWorker metodą clients.pop(0)
            i aktualizuje poziom najebania sie.
            A no i poza tym dodaje swoje metody zeby nie psuc waszych
            < nie chce mi sie into Diffy) >
    """
    def __init__(self, clients: [Client], store: Store):
        self.store = store
        self.clients = clients

    def get_drink_instance(self, drink_name: str) -> (int, Drink):
        for stored_drink in self.store.read():
            (_, drink) = stored_drink

            if drink.name == drink_name:
                return stored_drink

    def get_current_client(self, name: str) -> Client:
        return next((client for client in self.clients if client.name == name), None)

    def serve_drink(self, drink: Drink) -> None:
        print("Serving {}.".format(drink.name))
        self.store.update(drink)

    def deal_with_client(self, order: bytes) -> None:
        print(15*'-')
        print("\n\n\n\n\n\n\n\n\n\n")
        current_client = self.get_current_client(json.loads(order.decode())['client_name'])
        drink_tuple = self.get_drink_instance(json.loads(order.decode())['drink'])

        if drink_tuple and current_client:
            (_, drink) = drink_tuple
            self.serve_drink(drink)
            current_client.drink(drink)
        elif current_client:
            print("Cannot serve. No drinks available")
            current_client.start_again()

        time.sleep(1)

    def start(self) -> None:
        print("Bar started working")
        rabbit.consume(Config.RABBIT.QUEUES['ToBar'], self.deal_with_client)

################################################
#ROSZKO KOD : TAK WIEM ZJEBANY
# nie uzywam deal with client bo nie operuje na kolejce klientow rabbita
################################################

    def check_if_store_empty(self):
        for drink in self.store.read():
            if drink[0]:
                return False  # cos tam jest

    def get_drink_tuple(self, drink_name: str) -> (int, Drink):
        for stored_drink in self.store.read():
            #(_, drink) = stored_drink
            if stored_drink[1].name == drink_name:
                return stored_drink

    def serve_alcohol(self):
        elem = self.clients.pop(0)
        client, drink_to_get = elem[0], elem[1]
        drink = self.get_drink_tuple(drink_to_get)

        if drink:
            client.drink(drink[1])
            self.serve_drink()
        else:
            if not self.check_if_store_empty():
                #wypierdol programm
                print("STORE IS EMPTY TIME TO SOBER UP")
