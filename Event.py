from simulator import *


class Event:

    def __init__(self):
        self.time = 0
        self.tx = None

    def isEndSimulation(self):
        return False

    def showTime(self):
        Simulator.showTime(self.time)
