from Drink.Drink import Drink


class Whisky(Drink):
    def __init__(self):
        super().__init__("Whisky", 30)
        self.volume = 100
