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
    #elapsed_time = time.time()
    Sobering_timer_trigger = 1 # 1 jednostka = 1s
    SOBER_RATE_PER_HOUR = 0.016

    sober_update_rate = SOBER_RATE_PER_HOUR *Sobering_timer_trigger/3600

    def __init__(self, name, sex: Sex, weight, ebac_goal, store: Store):
        super(Client, self).__init__()
        self.daemon = True
        self.cancelled = False
        self.ebac = 0
        self.cant_drinks = []
        self.is_in_queue = False
        self.is_reading = False
        self.drinking_start_time = 0
        self.last_drinking_time: time = time.time()
        self.non_drinking_period = 0
        self.sobering_last_update_time = time.time()
        self.start_time = time.time()
        self.elapsed_time = self.start_time
        self.name = name
        self.sex = sex
        self.weight = weight
        self.ebac_goal = ebac_goal
        self.store = store

        self.start()

    @property
    def non_drinking_period(self):
        return "Non drink period: "+str(time.time() - self.last_drinking_time)

    @non_drinking_period.setter
    def non_drinking_period(self, value):
        return time.time() - self.last_drinking_time
    @property
    def elapsed_time(self):
        return time.time() - self.start_time

    @elapsed_time.setter
    def elapsed_time(self, value):
        """
         Zabezpieczenie przed zmiana
        :param value:
        :return:
        """
        #self.elapsed_time = time.time() - self.start_time
        return self.elapsed_time

    def run(self):
        self.drinking_start_time = time.time()

        while not self.cancelled:
            time.sleep(1)
            self.sobering()
            # here is sobering if ebac > 0 ofc
            if not self.is_in_queue and not self.is_reading:
                self.open_menu()

    def sobering(self):
        if (time.time() - self.sober_update_rate) >= Client.Sobering_timer_trigger:
            self.ebac -= Client.sober_update_rate
            self.sober_update_rate = time.time()
            print("NO OK SPRAWDZAMY\n NON DRINKING PERIOD: {}\n sober_update_rate: {}\n Elapsed_time: {}\n".format(self.non_drinking_period, self.sober_update_rate, self.elapsed_time))

    def start_over(self):
        self.is_in_queue = False
        self.is_reading = False

    def drink(self, drink):
        self.ebac += Ebac(self, drink).get_ebac()

        self.last_drinking_time = time.time()
        time.sleep(drink.drinking_period)
        # print('{} drank.'.format(self.name))
        self.is_in_queue = False


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
            self.print_result()
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

    def print_result(self):
        print('\033[92mAfter {} {} is going home\033[0m.'.format(time.time() - self.drinking_start_time, self.name))
        print('Non-drinking period: {}'.format(self.non_drinking_period))
        print('Final EBAC value: {}'.format(self.ebac))
        print('Is satisfied: {}'.format(self.ebac > 0.85 * self.ebac_goal)) #TODO fajnie by zrobic czy zawiera sie w przedziale z wikipedii. Wtedy jako parametr nie wpadalaby liczba (ebac_goal) tylko konkretny enum
        print(50 * '=')