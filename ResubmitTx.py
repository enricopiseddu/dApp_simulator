from Event import *


class ResubmitTx(Event):

    def execute(self):
        if self.tx.component.isFull():
            duration = self.tx.component.delayWhenFull
            event = ResubmitTx()
        else:
            r = ARandom()
            duration = r.logNormal(self.tx.type.avgTime, self.tx.type.stdDevTime)
            duration = duration + self.tx.component.delay()
            self.tx.creationTime(self.time)
            self.tx.component.addTransaction(self.tx)
            self.tx.actor.addTransaction(self.tx)
            event = EndTx()

        event.time = self.time + duration
        event.tx = self.tx

        Simulator.getInstance().eventQueue.append(event)

