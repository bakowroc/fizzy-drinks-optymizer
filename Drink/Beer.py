from Drink.Drink import Drink


class Beer(Drink):
    def __init__(self):
        super().__init__('Beer', 6)
        self.volume = 500
