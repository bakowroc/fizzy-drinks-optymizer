from Drink.Drink import Drink


class Wine(Drink):
    def __init__(self):
        super().__init__('Wine', 18, 200, 0.5)
