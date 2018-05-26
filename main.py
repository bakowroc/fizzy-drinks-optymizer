import json

from Bar.Bar import Bar
from Client.Client import Client
from RabbitMQ.RabbitMQ import RabbitMQ
from Sex.Sex import Sex
from config.Config import Config
from Store.Store import Store

store = Store()


rabbit = RabbitMQ()

clients = [
    Client('John', Sex.Male, 75, store),
    Client('Karina', Sex.Female, 190, store),
    Client('Johhny', Sex.Male, 45, store),
    Client('Jerry', Sex.Male, 75, store),
    Client('Jim', Sex.Male, 69, store),
    Client('George', Sex.Male, 140, store)
]


def main():
    bar = Bar(clients, store)
    bar.start()


if __name__ == "__main__":
    main()
