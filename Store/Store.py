from random import randint

from Drink.Beer import Beer
from Drink.Brandy import Brandy
from Drink.Drink import Drink
from Drink.Gin import Gin
from Drink.Moonshine import Moonshine
from Drink.Tequila import Tequila
from Drink.Vodka import Vodka
from Drink.Whisky import Whisky
from Drink.Wine import Wine


class Store:
    def __init__(self):
        self.drinks_available = []
        self.fill()

    def fill(self) -> None:
        drinks = [Beer(), Vodka(), Whisky(), Brandy(), Gin(), Moonshine(), Tequila(), Wine()]
        for drink in drinks:
            self.drinks_available.append((randint(1, 30), drink))

    def read(self) -> [(int, Drink)]:
        self.drinks_available = list(filter(lambda drink: drink[0] > 0, self.drinks_available))
        return self.drinks_available

    def update(self, current_drink: Drink) -> None:
        self.drinks_available = list(
            map(lambda drink: (drink[0] - 1, drink[1]) if drink[1].name == current_drink.name else drink,
                self.drinks_available)
        )
