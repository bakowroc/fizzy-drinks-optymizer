from Drink.Drink import Drink


class Vodka(Drink):
    def __init__(self):
        super().__init__('Vodka', 40)
        self.volume = 50
