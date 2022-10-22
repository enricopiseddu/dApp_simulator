"""
This software is distributed under MIT/X11 license

Copyright (c) 2022 Enrico Piseddu - University of Cagliari

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""


from BaseTXType import *
from Component import *
from Event import Event
from Operator import *
from Customer import *
from ARandom import *
from operator import attrgetter
from sortedcontainers import SortedList

import csv


# from ResubmitTx import ResubmitTx
from StartTx import StartTx


class Simulator:
    __instance = None

    @staticmethod
    def getInstance():
        if Simulator.__instance is None:
            Simulator()
        return Simulator.__instance

    def __init__(self):
        if Simulator.__instance is not None:
            raise Exception('The class is a singleton!')
        else:
            Simulator.__instance = self

        self.actors = []
        self.complexTxs = []
        self.components = []
        self.eventQueue = SortedList()  # SortedList based on events' timestamp
        self.schedules = {
            "OP1": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0.10, 0.13, 0.13, 0.13, 0.07, 0.04, 0.12, 0.12, 0.12, 0.04, 0, 0, 0, 0,
                    0],
            "CU1": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.03, 0.06, 0.08, 0.08, 0.12, 0.06, 0.06, 0.08, 0.08, 0.08, 0.05,
                    0.10,
                    0.07, 0.05]}
        self.time = 0

    def componentNamed(self, aString):
        for each in self.components:
            if each.name == aString:
                assert isinstance(each, Component)
                return each

    def readActorsFrom(self, actorFileName):

        rand = ARandom()

        with open(actorFileName) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1  # skip first line of file
                else:
                    if line_count == 1:
                        print(
                            f'ACTOR \t{row[0]} NUMBER TOTAL {row[1]}, nr. TXs/day {row[2]}, std.dev. TXs/day {row[3]}, schedule {row[4]}')
                        numberOfOperators = int(row[1])
                        avgTxOper = int(row[2])
                        stTxOp = int(row[3])
                        scheduleOp = str(row[4])

                        line_count += 1
                    else:
                        print(
                            f'ACTOR \t{row[0]} NUMBER TOTAL {row[1]}, nr. TXs/day {row[2]}, std.dev. TXs/day {row[3]}, schedule {row[4]}')
                        numberOfCustomers = int(row[1])
                        avgTxCust = int(row[2])
                        stTxCu = int(row[3])
                        scheduleCu = str(row[4])
                        line_count += 1

        # actors: operators and customers creation
        for i in range(0, numberOfOperators):
            actor = Operator()
            actor.id = 'OP' + str(i)
            actor.nrTx = int(rand.logNormal(avgTxOper, stTxOp))
            actor.schedule = scheduleOp
            self.actors.append(actor)

        for i in range(0, numberOfCustomers):
            actor = Customer()
            actor.id = 'CU' + str(i)
            actor.nrTx = int(rand.logNormal(avgTxCust, stTxCu))
            if actor.nrTx == 0:
                actor.nrTx = 1

            actor.schedule = scheduleCu
            self.actors.append(actor)

    def readComponentsFrom(self, componentFileName):
        with open(componentFileName) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    name = str(row[0])
                    avgDelay = int(row[1])
                    stDevDelay = int(row[2])
                    maxNrTxs = int(row[3])
                    delayWhenFull = int(row[4])

                    newComponent = Component()

                    newComponent.name = name
                    newComponent.avgDelay = avgDelay
                    newComponent.stDevDelay = stDevDelay
                    newComponent.maxNrTxs = maxNrTxs
                    newComponent.delayWhenFull = delayWhenFull

                    self.components.append(newComponent)

    def readTransactionsFrom(self, txFileName):

        with open(txFileName) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            txs1 = []
            txs2 = []
            txs3 = []
            txs4 = []
            line_count = 1
            for row in csv_reader:
                if line_count == 1 or line_count == 2:  # skip first two lines of file
                    line_count += 1
                else:
                    if line_count == 3:
                        txs1.append(row)

                    if 4 <= line_count <= 8:
                        txs1.append(row)

                    if line_count == 9:
                        txs2.append(row)

                    if 10 <= line_count <= 15:
                        txs2.append(row)

                    if line_count == 16:
                        txs3.append(row)

                    if 17 <= line_count <= 18:
                        txs3.append(row)

                    if line_count == 19:
                        txs4.append(row)

                    if 20 <= line_count <= 23:
                        txs4.append(row)
                    line_count += 1

            for each in [txs1, txs2, txs3, txs4]:
                tx = ComplexTXType()
                tx.id = each[0][0]
                tx.minNrBTX = int(each[0][1])
                tx.percOper = float(each[0][2])
                tx.percCust = float(each[0][3])
                tx.avgBTX = int(each[0][4])
                tx.stDevBTX = int(each[0][5])

                self.complexTxs.append(tx)

                for i in range(1, len(each)):
                    bTx = BaseTXType()
                    bTx.id = str(each[i][0])
                    bTx.compType = str(each[i][1])
                    bTx.avgTime = int(each[i][2])
                    bTx.stdDevTime = int(each[i][3])

                    tx.bTXBloc.append(bTx)

                for anActor in self.actors:
                    tx.createTransactionFor(anActor)

    def run(self):
        while len(self.eventQueue) != 0:
            # simulator takes the event with minimum timestamp
            event = self.eventQueue.pop(0)
            self.time = event.time
            event.execute()

    @staticmethod
    def showTime(timeMsec):
        h = int(timeMsec * 0.001 / 3600)
        m = int(((timeMsec * 0.001) - (h * 3600)) / 60)
        s = round(((timeMsec * 0.001) - (h * 3600) - (m * 60)))
        print(h, ':', m, ':', s)

    @staticmethod
    def timeOfHour(anInt):
        return anInt * 3600000

    @staticmethod
    def timeOfHour(anInt, minInt):
        return Simulator.timeOfHour(anInt) + (minInt * 60000)


class ComplexTXType:

    def __init__(self):
        self.avgBTX = 0
        self.bTXBloc = []
        self.id = 0
        self.minNrBTX = 0
        self.percCust = 0
        self.percOper = 0
        self.stDevBTX = 0

    def createBasicTransactionsFor(self, anActor: Actor, anInt):
        first = True
        ind = 1
        prob = anInt * 0.01

        schedule = Simulator.getInstance().schedules[anActor.schedule]

        r = ARandom()
        k = r.eventFrom(schedule)

        time = (k - 1) * 3600000

        time = time + round(3600000 * r.rand())

        nrBlocks = self.avgBTX

        if self.stDevBTX > 0:
            r = ARandom()
            nrBlocks = r.logNormal(self.avgBTX, self.stDevBTX)
            nrBlocks = round(max(1, nrBlocks))

        prevTx = None

        for i in range(0, nrBlocks):
            for each in self.bTXBloc:
                tx = Transaction()

                tx.id = str(anActor.id) + str('-') + str(anInt) + str('.') + str(ind)
                tx.type = each
                tx.actor = anActor
                tx.component = Simulator.getInstance().componentNamed(each.compType)
                tx.previous = prevTx

                if prevTx is not None:
                    prevTx.next = tx

                prevTx = tx
                ind = ind + 1
                anActor.transactions.append(tx)

                if first:
                    anActor.nrComplexTx = anActor.nrComplexTx + 1
                    event = StartTx()
                    event.time = time
                    event.tx = tx

                    Simulator.getInstance().eventQueue.add(event)

                    first = False

    def createTransactionFor(self, actor):

        if actor.isOperator():
            prob = self.percOper * 0.01
        else:
            prob = self.percCust * 0.01

        r = ARandom()
        for k in range(0, int(actor.nrTx)):
            if r.rand() < prob:
                self.createBasicTransactionsFor(actor, k)


class StartTx(Event):

    def execute(self):
        if self.tx.component.isFull():
            duration = self.tx.component.delayWhenFull
            event = ResubmitTx()
        else:
            r = ARandom()
            duration = r.logNormal(self.tx.type.avgTime, self.tx.type.stdDevTime)
            duration = duration + self.tx.component.delay()
            self.tx.creationTime = self.time
            self.tx.component.addTransaction(self.tx)
            self.tx.actor.addTransaction(self.tx)
            event = EndTx()

        event.time = int(self.time + duration)
        event.tx = self.tx

        s = Simulator.getInstance()
        s.eventQueue.add(event)


class EndTx(Event):

    def execute(self):
        if self.tx is None:
            return self

        self.tx.component.subTxsUnderWork()
        self.tx.endTime = self.time
        newTx = self.tx.next

        if newTx is None:
            return self

        event = StartTx()
        event.time = self.time
        event.tx = newTx

        s = Simulator.getInstance()
        s.eventQueue.add(event)


class ResubmitTx(Event):

    def execute(self):
        if self.tx.component.isFull():
            duration = self.tx.component.delayWhenFull
            event = ResubmitTx()
        else:
            r = ARandom()
            duration = r.logNormal(self.tx.type.avgTime, self.tx.type.stdDevTime)
            duration = duration + self.tx.component.delay()
            self.tx.creationTime = self.time
            self.tx.component.addTransaction(self.tx)
            self.tx.actor.addTransaction(self.tx)
            event = EndTx()

        event.time = self.time + duration
        event.tx = self.tx

        Simulator.getInstance().eventQueue.add(event)


