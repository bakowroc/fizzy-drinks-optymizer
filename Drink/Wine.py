from Drink.Drink import Drink


class Wine(Drink):
    def __init__(self):
        super().__init__('Wine', 18)
        self.volume = 100
