from Transaction import *


class BaseTXType:

    def __init__(self):
        self.id = ''
        self.compType = ''
        self.avgTime = 0
        self.stdDevTime = 0

