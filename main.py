import json

from Bar.Bar import Bar
from Client.Client import Client
from RabbitMQ.RabbitMQ import RabbitMQ
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
    Client('John'),
    Client('Jimmy'),
    Client('Johhny'),
    Client('Jerry'),
    Client('Jim'),
    Client('George')
]


def main():
    for order in orders:
        rabbit.publish(json.dumps(order), Config.RABBIT.QUEUES['ToBar'])

    bar = Bar(clients)
    bar.start()


if __name__ == "__main__":
    main()
