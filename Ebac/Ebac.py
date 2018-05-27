from Drink.Drink import Drink
from Sex.Sex import Sex


class Ebac:

    def __init__(self, client, drink: Drink):
        self.client = client
        self.drink = drink
        self.BW = 0
        self.MR = 0
        self.gender_parameters()

    def gender_parameters(self):
        if self.client.sex == Sex.Male:
            self.BW = 0.58
            self.MR = 0.015
        else:
            self.BW = 0.49
            self.MR = 0.017

    def get_standard_drink(self):
        return self.drink.volume * self.drink.alcohol / 1000

    def get_ebac(self):
        ebac_value = (((0.806 * self.get_standard_drink() * 1.2) / (
                    self.BW * self.client.weight)) - self.MR * self.drink.drinking_period)
        return ebac_value

