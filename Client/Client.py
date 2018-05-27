import json
from random import randint

from Ebac.Ebac import Ebac
from RabbitMQ.RabbitMQ import RabbitMQ
from Sex.Sex import Sex
from Store.Store import Store
from config.Config import Config

rabbit = RabbitMQ()

HARD_CODED_EBAC_DESTINATION_VALUE = 0.9
INFINITY = 99999999

class Client:
    def __init__(self, name, sex: Sex, weight, store: Store):
        self.name = name
        self.ebac = 0.2
        self.sex = sex
        self.weight = weight
        self.store = store
        #self.preference = preference
        self.cant_drinks = []
        #self.start_again()

    def metabolize(self, time):
        self.ebac -= 0.016*time

    def drink(self, drink_type):
        self.ebac += Ebac(self, drink_type).get_ebac()
        print(self.ebac)
        print('{} drank.'.format(self.name))
        # self.start_again()

    def can_i_drink(self):
        store_content = self.drinks_i_can_drink()
        #print(store_content)

        choice = self.choose_best_drink(store_content)
        print("best choice is:",choice)

        return choice

    def choose_best_drink(self, available_drinks):

        """
            funkcja wybierajaca drink ktory zapewni docelowo wartosc ebac najbliższą wartości
            docelowej (HARD_CODED_EBAC_DESTINATION_VALUE). Możliwe jest przedawkowanie
        :return:
        """
        smallest_caught_value = INFINITY
        best_drink = None
        for drink_tuple in available_drinks:
            diff = HARD_CODED_EBAC_DESTINATION_VALUE - self.calculate_ebac_for_drink(drink_tuple[1])
            if abs(diff) < smallest_caught_value:
                final_ebac_for_drink, best_drink = abs(diff), drink_tuple

        return final_ebac_for_drink, best_drink

    def calculate_ebac_for_drink(self, drink):
        return self.ebac + Ebac(self, drink).get_ebac()

    def may_i_drink(self, drink):
        ret_val = self.ebac + Ebac(self, drink).get_ebac()
        print(ret_val)
        cond = bool(ret_val >= 0)
        print(cond)
        return not cond

    def start_again(self):
        print('{} is reading menu.'.format(self.name))
        (_, drink) = self.choose_drink()
        print("START AGAIN CHP1", drink)
        print("Start_again chp2", self.cant_drinks)
        if self.may_i_drink(drink):
            rabbit.publish(json.dumps({'client_name': self.name, 'drink': drink.name}), Config.RABBIT.QUEUES['ToBar'])
        else:
            print("start_again chp3", self.cant_drinks)
            print("start_again chp4", drink.name)

            #print("start_again chp5 ", self.cant_drinks.append(drink.name))
            #self.cant_drinks = self.cant_drinks.append(drink.name)

            self.cant_drinks.append(drink.name)
            #szybkie obejscie, na razie niech zostanie
            self.cant_drinks = list(set(self.cant_drinks))

            print("start_again chp backup 5 SPECIAL", self.cant_drinks)
            print('niemoge', self.cant_drinks)
            import time
            time.sleep(3)
            self.start_again()

    def choose_drink(self):
        print('CHOOSE DRINK: wybieram', self.cant_drinks)
        if self.cant_drinks is not []:
            print('dupsasasasa')
            store_i_can_access = list(filter(lambda drink_tuple: drink_tuple[1].name not in self.cant_drinks, self.store.read()))
        else:
            store_i_can_access = self.store.read()
        return store_i_can_access[randint(0, len(self.store.read()) - 1)]

    def drinks_i_can_drink(self):
        if self.cant_drinks is []:
            drinks = filter(lambda drink_tuple: drink_tuple[1].name not in self.cant_drinks, self.store.read())
        else:
            drinks = self.store.read()

        return drinks