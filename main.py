import json

from Bar.Bar import Bar
from Client.Client import Client
from RabbitMQ.RabbitMQ import RabbitMQ
from Sex.Sex import Sex
from config.Config import Config

rabbit = RabbitMQ()
orders = [
    {
        'client_name': 'John',
        'drink': 'Vodka'
    },
    {
        'client_name': 'Jim',
        'drink': 'Whiskey'
    },
    {
        'client_name': 'Jerry',
        'drink': 'Beer'
    },
    {
        'client_name': 'Johhny',
        'drink': 'Vodka'
    },
    {
        'client_name': 'Jimmy',
        'drink': 'Vodka'
    },
    {
        'client_name': 'George',
        'drink': 'Beer'
    }
]
clients = [
    Client('John', Sex.Male, 75),
    Client('Karina', Sex.Female, 190),
    Client('Johhny', Sex.Male, 45),
    Client('Jerry', Sex.Male, 75),
    Client('Jim', Sex.Male, 69),
    Client('George', Sex.Male, 140)
]


def main():
    for order in orders:
        rabbit.publish(json.dumps(order), Config.RABBIT.QUEUES['ToBar'])

    bar = Bar(clients)
    bar.start()


if __name__ == "__main__":
    main()
