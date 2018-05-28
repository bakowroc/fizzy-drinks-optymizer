import json
import time
from random import randint
from threading import Thread, Event

from Ebac.Ebac import Ebac
from Ebac.Levels import Level
from RabbitMQ.RabbitMQ import RabbitMQ
from Sex.Sex import Sex
from Store.Store import Store
from config.Config import Config
import matplotlib.pyplot as pplot
rabbit = RabbitMQ()
AVG_READING_TIME = 0.05
Sobering_timer_trigger = 1 # 1 jednostka = 1s
SOBER_RATE_PER_HOUR = 0.016
sober_update_rate = SOBER_RATE_PER_HOUR *Sobering_timer_trigger/3600
Upper_limit = 999999999

class Client(Thread):
    dataset = {}

    def __init__(self, name, sex: Sex, weight, ebac_goal, store: Store, rabbit: RabbitMQ):
        super(Client, self).__init__()
        self.runtime_condition = Event()
        self.daemon = True
        self.cancelled = False
        self.ebac = 0
        self.cant_drinks = []
        self.is_in_queue = False
        self.is_reading = False

        self.drinking_start_time = 0
        self.last_time_drink = 0
        self.non_drinking_period = 0
        self.start_non_drinking = 0
        self.sober_update_rate = 0

        self.name = name
        self.sex = sex
        self.weight = weight
        self.ebac_goal = ebac_goal
        self.store = store
        self.rabbit = rabbit
        self.optimized = True

        self.start()
        Client.dataset[self] = list()

    def update_dataset(self):
        Client.dataset[self].append((self.elapsed_time, self.ebac))

    @property
    def elapsed_time(self):
        return time.time() - self.drinking_start_time

    @elapsed_time.setter
    def elapsed_time(self, value):
        """
         Zabezpieczenie przed zmiana
        :param value:
        :return:
        """
        # self.elapsed_time = time.time() - self.start_time
        return self.elapsed_time

    def run(self):
        self.drinking_start_time = time.time()

        while not self.cancelled:
            if self.ebac is not 0:
                self.sobering()
            if not self.is_in_queue and not self.is_reading:
                self.open_menu()
                self.update_dataset()

    def sobering(self):
        if (time.time() - self.sober_update_rate) >= Sobering_timer_trigger:
            self.ebac -= sober_update_rate
            self.sober_update_rate = time.time()

    def start_over(self, store_status):
        self.is_in_queue = False
        self.is_reading = False

        if store_status:
            self.cancelled = True
            #self.runtime_condition.set()

    def drink(self, drink):
        self.is_in_queue = False
        time.sleep(drink.drinking_period)
        self.ebac += Ebac(self, drink).get_ebac()
        self.last_time_drink = time.time()
        self.non_drinking_period += time.time() - self.start_non_drinking

    def calculate_ebac_for_drink(self, drink):
        return self.ebac + Ebac(self, drink).get_ebac()

    def may_i_drink(self, drink):
        return not self.ebac + Ebac(self, drink).get_ebac() >= self.ebac_goal[1]

    def open_menu(self):
        self.is_reading = True
        self.start_non_drinking = time.time()
        time.sleep(AVG_READING_TIME)

        if self.optimized:
            drink_tuple = self.choose_drink()
        else:
            dest_ebac, drink_tuple = self.choose_best_drink()

        if drink_tuple is not None:
            (_, drink) = drink_tuple
        else:
            self.print_result()
            return

        if self.may_i_drink(drink):
            self.rabbit.publish(json.dumps({'client_name': self.name, 'drink': drink.name}), Config.RABBIT.QUEUES['ToBar'])
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

    def choose_best_drink(self):
        min = Upper_limit
        best_drink = None
        final_ebac = 0

        if len(self.cant_drinks) is not 0:
            store_i_can_access = list(
                filter(lambda drink_tuple: drink_tuple[1].name not in self.cant_drinks, self.store.read()))
        else:
            store_i_can_access = self.store.read()

        if len(store_i_can_access) is 0:
            self.cancelled = True
            return

        for drink_tuple in store_i_can_access:
            diff = self.ebac_goal[1] - self.calculate_ebac_for_drink(drink_tuple[1])
            if diff < 0:
                break
            elif abs(diff) < min:
                final_ebac, best_drink = abs(diff), drink_tuple

        return final_ebac, best_drink

    def print_result(self):
        print('\033[92mAfter {} {} is going home\033[0m.'.format(self.elapsed_time, self.name))
        print('Non-drinking period: {}'.format(self.non_drinking_period))
        print('Final EBAC value: {}'.format(self.ebac))
        print('Is satisfied: {}'.format(self.ebac_goal[1] > self.ebac > self.ebac_goal[0]))
        print(50 * '=')

    @classmethod
    def draw(cls):
        pplot.xlabel("time")
        pplot.ylabel("EBAC")
        pplot.title("EBAC chart")
        pplot.figure(figsize=(2, 2))

        els = list()
        for key,value in Client.dataset.items():
            els.append(list(map(list, zip(*value))))

        for i in range(len(els)):
            pplot.plot([pt[0] for pt in els][i], [pt[1] for pt in els][i])

        pplot.legend()
        pplot.show()
