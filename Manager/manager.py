from threading import Event, Thread, Lock
import typing
import time
from Client.Client import Client



class Manager(object):
    def __init__(self, persons: typing.List[Client]):
        self.elapsed_time = time.time()
        self.elapsed_time2 = time.time()
        self.worktime = 50000000
        self.exec_thread = Thread(target=self.run)
        self.clients: typing.List[Client] = persons
        self.exec_breakpoint = Event
        self.access_lock = Lock

    def run(self):
        self.worktime = time.time()+5
        self.elapsed_time2 = time.time()

        print(self.elapsed_time2)
        print(self.worktime)

        while time.time() < self.worktime:
            self.elapsed_time = time.time() - self.elapsed_time

            for person in self.clients:
                person.drink_time = self.elapsed_time
                person._sober()
                print(person.EBAC)

        print(time.time()-self.worktime)