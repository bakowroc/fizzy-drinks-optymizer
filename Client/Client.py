import json
import time
from random import randint
from threading import Thread

from Ebac.Ebac import Ebac
from RabbitMQ.RabbitMQ import RabbitMQ
from Sex.Sex import Sex
from Store.Store import Store
from config.Config import Config

rabbit = RabbitMQ()
AVG_READING_TIME = 1


class Client(Thread):
    def __init__(self, name, sex: Sex, weight, ebac_goal, store: Store):
        super(Client, self).__init__()
        self.daemon = True
        self.cancelled = False
        self.ebac = 0
        self.cant_drinks = []
        self.is_in_queue = False
        self.is_reading = False
        self.drinking_start_time = 0
        self.non_drinking_period = time.time()

        self.name = name
        self.sex = sex
        self.weight = weight
        self.ebac_goal = ebac_goal
        self.store = store

        self.start()

    def run(self):
        self.drinking_start_time = time.time()

        while not self.cancelled:
            # here is sobering if ebac > 0 ofc
            if not self.is_in_queue and not self.is_reading:
                self.open_menu()

    def start_over(self):
        self.is_in_queue = False
        self.is_reading = False

    def drink(self, drink):
        self.ebac += Ebac(self, drink).get_ebac()
        self.non_drinking_period = time.time() - self.non_drinking_period # TODO cos to gowno zwraca jakis syf
        # print('{} drank.'.format(self.name))
        self.is_in_queue = False
        time.sleep(drink.drinking_period)

    def may_i_drink(self, drink):
        return not self.ebac + Ebac(self, drink).get_ebac() >= self.ebac_goal

    def open_menu(self):
        self.is_reading = True
        time.sleep(AVG_READING_TIME)

        # print('{} is reading menu.'.format(self.name))
        drink_tuple = self.choose_drink()

        if drink_tuple is not None:
            (_, drink) = drink_tuple
        else:
            # JAKIES OUTPUTY / INFO O KLIENCIE GDY JUZ SKONCZYL (Z ROZNYCH POWODOW) TYPU EBAC, DRINKI WYPITE, CZASY ITD
            print('\033[92mAfter {} {} is going home\033[0m. Non-drinking period: {}'.format(
                time.time() - self.drinking_start_time, self.name, self.non_drinking_period))
            return

        if self.may_i_drink(drink):
            rabbit.publish(json.dumps({'client_name': self.name, 'drink': drink.name}), Config.RABBIT.QUEUES['ToBar'])
            self.is_in_queue = True
        else:
            self.cant_drinks.append(drink.name)

        self.is_reading = False

    def choose_drink(self):
        if len(self.cant_drinks) is not 0:
            store_i_can_access = list(
                filter(lambda drink_tuple: drink_tuple[1].name not in self.cant_drinks, self.store.read()))
        else:
            store_i_can_access = self.store.read()

        if len(store_i_can_access) is 0:
            self.cancelled = True
            return
        else:
            return store_i_can_access[randint(0, len(store_i_can_access) - 1)]