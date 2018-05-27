from Client.Client import Client
from Bar.Bar import Bar
from Store.Store import Store
from threading import Thread, Event, Lock
import time
import typing

KWANT_CZASU_TRZEZWIENIA = 1/60

# kontenera na wszystkie niezbedne zasoby
class EbacManager:

    def __init__(self, lock: Lock, clients: typing.List[Client], event: Event, evaluation_time: time, store: Store):
        self.clients = clients
        self.resource_lock = lock
        self.work_breakpoint = event
        self.bar_queue = []
        self.worktime: float = evaluation_time
        self.ebac_worker = EbacEventWorker(self)
        self.bar_worker = BarWorker(self, store)
        self.time_expired_event = Event()
        self.can_consume_queue = Event() # jezeli lista jest pusta, watek baru musi czekac
        ###
        # czy mozna przedawkowac?
        ###
        self.can_overdose = True

    def shutdown(self):
        self.time_expired_event.set()
# klasy odpowiedzialne za propagowanie wydarzen w ramach dzialania programu
# czyli przykladowo zmniejszanie ebac'a w czasie rzeczywistym
# wpisywanie osób do kolejki do baru
# wyznaczanie wszystkich wskaźników etc poprzez callbacki
# większość relacji jest zrobiona przez agregacje (instancja klas wewnątrz innych)
# i tak wiem nie robie po waszemu, ale trochę nie kminie idei z rabbitmq,
# mam nadzieje ze chociaż część kodu się przyda


class BarWorker:
    def __init__(self, manager: EbacManager, store: Store):
        self.Ebac_Manager = manager
        self.bar_thread = Thread(target=self.run_task)
        self.interval = 0.01 # to rethink
        self.serving_bar = Bar(self.Ebac_Manager.bar_queue, store)

    def run(self):
        self.bar_thread.start()

    def run_task(self):
        #print("CONSUMER THREAD")
        while True:
            if self.Ebac_Manager.time_expired_event.isSet():
                #print("CONS_TH_END")
                return
            #print("CONSUMER_TH_CHP1")
            self.Ebac_Manager.can_consume_queue.wait()
            #print("CONSUMER_TH_CHP2")
            x = self.serving_bar.serve_alcohol()
            if x is None:
                pass
                #print("bar is empty")
            else:
                print("Client: {}\n drink: {}".format(x[0], x[1]))



class EbacEventWorker:

    def __init__(self, manager: EbacManager):
        self.Ebac_Manager = manager
        self.worker_thread = Thread(target=self.run_task)
        self._interval = 1.0  # in sec

    def run(self):
        self.worker_thread.start()

    def run_task(self):

        curr_time = time.time()

        while True:
            if self.Ebac_Manager.time_expired_event.isSet():
                return

            for client in self.Ebac_Manager.clients:
                client.metabolize(KWANT_CZASU_TRZEZWIENIA*(time.time() - curr_time))
                choice = client.can_i_drink()
                if choice[0] > 0.9 and not self.Ebac_Manager.can_overdose:
                    pass
                else:
                    self.Ebac_Manager.bar_queue.append((client, choice))
                    self.Ebac_Manager.can_consume_queue.set()
                time.sleep(1)

               # print("KLIENT: {} ".format(client.ebac))

            #print("CZAS: {} \n\n\n".format((time.time() - curr_time)% 100))
            #print("KOLEJKA to: {}\n\n\n".format(self.Ebac_Manager.bar_queue))
            time.sleep(5)
            self.Ebac_Manager.time_expired_event.wait(self._interval)

