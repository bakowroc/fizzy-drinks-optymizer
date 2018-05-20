from random import randint

from Drink.Beer import Beer
from Drink.Drink import Drink
from Drink.Vodka import Vodka
from Drink.Whiskey import Whiskey


class Store:
    def __init__(self):
        self.drinks_available = []
        self.fill()

    def fill(self) -> None:
        drinks = [Beer(), Vodka(), Whiskey()]
        for drink in drinks:
            self.drinks_available.append((randint(0, 30), drink))

    def read(self) -> [(int, Drink)]:
        self.drinks_available = list(filter(lambda drink: drink[0] > 0, self.drinks_available))
        return self.drinks_available

    def update(self, current_drink: Drink) -> None:
        self.drinks_available = list(
            map(lambda drink: (drink[0] - 1, drink[1]) if drink[1].name == current_drink.name else drink,
                self.drinks_available)
        )
