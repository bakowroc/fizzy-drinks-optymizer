class Client:
    def __init__(self, name):
        self.name = name
        self.ebac = 0

    def drink(self, drink_type):
        print('{} drank.'.format(self.name))

    def start_again(self):
        print('{} is reading menu again.'.format(self.name))