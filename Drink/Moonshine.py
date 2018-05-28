from Drink.Drink import Drink


class Moonshine(Drink):
    def __init__(self):
        super().__init__('Moonshine', 60, 100, 0.1)
