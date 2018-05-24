from Drink.Drink import Drink


class Gin(Drink):
    def __init__(self):
        super().__init__('Gin', 35)
        self.volume = 100
