import typing
import time
from enum import Enum


class Sex(Enum):
    Male = 1
    Female = 0


class Client(object):

    def __init__(self, name: str, height: float, fatness: float, gender: Sex, age: int):
        self.name: str = name
        self._drink_time: float = 0
        self._total_drink_time = 0
        self.sex: Sex = gender
        self.weight: float = fatness
        self.height: float = height
        self.age: int = age
        self.EBAC = 0


    @property
    def drink_time(self):
        return self._drink_time

    @drink_time.setter
    def drink_time(self, time: float):
        self._drink_time = time- self._drink_time
        self._total_drink_time += self._drink_time

    def _sober(self):
        self.EBAC = self.EBAC - 5
