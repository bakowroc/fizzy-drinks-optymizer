import json

from Bar.Bar import Bar
from Client.Client import Client
from RabbitMQ.RabbitMQ import RabbitMQ
from Sex.Sex import Sex
from Ebac.Manager import  EbacManager, EbacEventWorker, BarWorker
from config.Config import Config
from Store.Store import Store
from threading import Event, Lock, Thread
import time
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
    #print("CHP0\n\n\n")
    #bar = Bar(clients, store)
    #print("CHP1")
    #print(5 * "\n")
    #bar.start()
    ClientList = [
        Client('John', Sex.Male, 75, store),
        Client('Karina', Sex.Female, 190, store),
        Client('Johhny', Sex.Male, 45, store),
        Client('Jerry', Sex.Male, 75, store),
        Client('Jim', Sex.Male, 69, store),
        Client('George', Sex.Male, 140, store)
    ]

    ebm =  EbacManager(Lock(), ClientList, Event(), 15, store)
    ebm.bar_worker.run()
    ebm.ebac_worker.run()
    time.sleep(5)
    print("DUPA PRINT1")
    ebm.shutdown()
    print("DUPA PRINT2")

if __name__ == "__main__":
    main()
