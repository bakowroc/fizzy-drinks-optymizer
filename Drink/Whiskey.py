from Drink.Drink import Drink


class Whiskey(Drink):
    def __init__(self):
        super().__init__("Whiskey", 30)
        self.volume = 100
