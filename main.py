import json

from Bar.Bar import Bar
from Client.Client import Client, Sex
from RabbitMQ.RabbitMQ import RabbitMQ
from config.Config import Config
from Manager.manager import Manager

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
    Client('Andrew',    float(190), float(80), Sex(1), int(25)),
    Client('John',      float(190), float(80), Sex(1), int(25)),
    Client('Jimmy',     float(186), float(80), Sex(1), int(25)),
    Client('Johhny',    float(186), float(80), Sex(1), int(25)),
    Client('Jerry',     float(186), float(80), Sex(1), int(25)),
    Client('Jim',       float(186), float(80), Sex(1), int(25)),
    Client('George',    float(190), float(80), Sex(1), int(25))
]


def main():
    for order in orders:
        rabbit.publish(json.dumps(order), Config.RABBIT.QUEUES['ToBar'])

    bar = Bar(clients)
    bar.start()

    P1 = Client(180,50,Sex.Female, 20)
    P2 = Client(190,80, Sex.Male, 30)
    P3 = Client(150, 40, Sex.Female, 15)
    L = [P1,P2,P3]
    m = Manager(L)

    m.run()

if __name__ == "__main__":
    main()
