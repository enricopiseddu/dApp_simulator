from ResubmitTx import *
from ARandom import *
from simulator import *


class StartTx(Event):

    def execute(self):
        if self.tx.component.isFull():
            duration = self.tx.component.delayWhenFull
            event = ResubmitTx()
        else:
            # duration = Simulator rand logNormal: self tx type avgTime std: self tx type stdDevTime
            r = ARandom()
            duration = r.logNormal(self.tx.type.avgTime, self.tx.type.stdDevTime)

            # duration = duration + self.tx.component.delay()
            duration = duration + self.tx.component.delay()
            self.tx.creationTime = self.time
            self.tx.component.addTransaction(self.tx)
            self.tx.actor.addTransaction(self.tx)
            event = EndTx()

        event.time = self.time + duration
        event.tx = self.tx

        # Simulator current eventQueue add: event
        s = Simulator.getInstance()
        s.eventQueue.add(event)


