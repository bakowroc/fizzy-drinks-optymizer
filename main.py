from Bar.Bar import Bar
from Cancer.Cancer import Cancer
from Client.Client import Client
from Ebac.Levels import Level
from RabbitMQ.RabbitMQ import RabbitMQ
from Sex.Sex import Sex
from Store.Store import Store

store = Store()
rabbit = RabbitMQ()

clients = [
    Client('Abdul', Sex.Male, 86, Level.DEATH, store, rabbit),
    Client('Berry', Sex.Female, 79, Level.EMO_SWINGS, store, rabbit),
    Client('Kate', Sex.Male, 45, Level.EUPHORIA, store, rabbit),
    Client('Matthew', Sex.Male, 75, Level.NORMAL, store, rabbit),
    Client('Fender', Sex.Male, 69, Level.OVER_EXP, store, rabbit),
    Client('Fabric', Sex.Female, 140, Level.STUPOR, store, rabbit),
    Client('Bill', Sex.Male, 75, Level.TALKATIVE, store, rabbit),
    Client('Bohdan', Sex.Female, 190, Level.COMA, store, rabbit)
]


def main():
    Cancer(clients, rabbit).start()
    bar = Bar(clients, store)
    bar.start()


if __name__ == "__main__":
    main()
