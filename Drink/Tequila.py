from Drink.Drink import Drink


class Tequila(Drink):
    def __init__(self):
        super().__init__('Tequila', 38)
        self.volume = 75
