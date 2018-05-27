from Bar.Bar import Bar
from Client.Client import Client
from RabbitMQ.RabbitMQ import RabbitMQ
from Sex.Sex import Sex
from Store.Store import Store

store = Store()


rabbit = RabbitMQ()

clients = [
    Client('Abdul', Sex.Male, 86, 0.154, store),
    Client('Berry', Sex.Female, 79, 0.43, store),
    Client('Kate', Sex.Male, 45, 0.42, store),
    Client('Matthew', Sex.Male, 75, 0.12, store),
    Client('Fender', Sex.Male, 69, 0.33, store),
    Client('Fabric', Sex.Female, 140, 0.124, store),
    Client('Bill', Sex.Male, 75, 0.233, store),
    Client('Bohdan', Sex.Female, 190, 0.124, store)
]


def main():
    bar = Bar(clients, store)
    bar.start()


if __name__ == "__main__":
    main()
