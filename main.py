from Bar.Bar import Bar
from Client.Client import Client
from RabbitMQ.RabbitMQ import RabbitMQ
from Sex.Sex import Sex
from Store.Store import Store

store = Store()


rabbit = RabbitMQ()

clients = [
    Client('John', Sex.Male, 75, 0.2, store),
    Client('Karina', Sex.Female, 190, 0.7, store),
    Client('Johhny', Sex.Male, 45, 0.4, store),
    Client('Jerry', Sex.Male, 75, 0.6, store),
    Client('Jim', Sex.Male, 69, 0.5, store),
    Client('George', Sex.Male, 140, 0.15, store)
]


def main():
    bar = Bar(clients, store)
    bar.start()


if __name__ == "__main__":
    main()
