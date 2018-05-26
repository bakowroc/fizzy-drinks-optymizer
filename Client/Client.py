import json
from random import randint

from Ebac.Ebac import Ebac
from RabbitMQ.RabbitMQ import RabbitMQ
from Sex.Sex import Sex
from Store.Store import Store
from config.Config import Config

rabbit = RabbitMQ()

class Client:
    def __init__(self, name, sex: Sex, weight, store: Store):
        self.name = name
        self.ebac = 0
        self.sex = sex
        self.weight = weight
        self.store = store
        self.cant_drinks = []
        self.start_again()

    def drink(self, drink_type):
        self.ebac += Ebac(self, drink_type).get_ebac()
        print(self.ebac)
        print('{} drank.'.format(self.name))
        # self.start_again()

    def may_i_drink(self, drink):
        return not self.ebac + Ebac(self, drink).get_ebac() >= 0

    def start_again(self):
        print('{} is reading menu.'.format(self.name))
        (_, drink) = self.choose_drink()
        if self.may_i_drink(drink):
            rabbit.publish(json.dumps({'client_name': self.name, 'drink': drink.name}), Config.RABBIT.QUEUES['ToBar'])
        else:
            self.cant_drinks = self.cant_drinks.append(drink.name)
            print('niemoge', self.cant_drinks)
            self.start_again()

    def choose_drink(self):
        print('wybieram', self.cant_drinks)
        if self.cant_drinks is []:
            print('dupsasasasa')
            # store_i_can_access = list(filter(lambda drink_tuple: drink_tuple[1].name not in self.cant_drinks, self.store.read()))
        #else:
        store_i_can_access = self.store.read()

        return store_i_can_access[randint(0, len(self.store.read()) - 1)]
