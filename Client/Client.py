from Ebac.Ebac import Ebac
from Sex.Sex import Sex


class Client:
    def __init__(self, name, sex: Sex, weight):
        self.name = name
        self.ebac = 0
        self.sex = sex
        self.weight = weight

    def drink(self, drink_type):
        self.ebac += Ebac(self, drink_type).get_ebac()
        print(self.ebac)
        print('{} drank.'.format(self.name))

    def start_again(self):
        print('{} is reading menu again.'.format(self.name))
