import math
import copy
from ARandom import *
from simulator import *


class Component:

    def __init__(self):
        self.allTxs = []
        self.avgDelay = 0
        self.delayWhenFull = 500
        self.maxNrTxs = 0
        self.name = 0
        self.stDevDelay = 0.0
        self.txsUnderWork = 0

    def addTxsUnderWork(self, time):
        self.txsUnderWork = self.txsUnderWork + 1
        if self.isFull():
            print(self.name, ' is full', 'tx under work ', self.txsUnderWork, ' at ', Component.showTime(time))

    def addTransaction(self, aTransaction):
        self.addTxsUnderWork(aTransaction.creationTime)
        self.allTxs.append(aTransaction)

    def delay(self):
        # Ad hoc delay. There is delay if we are above 70% of max nr of TXs
        r = ARandom()
        delay = r.logNormal(self.avgDelay, self.stDevDelay)
        ratio = self.txsUnderWork / self.maxNrTxs

        if ratio <= 0.7:
            return delay
        else:
            return delay + round(delay * (ratio - 0.7) * 3.33)

    def durations(self):
        # Return the durations of all transactions, in decreasing order
        allT = copy.deepcopy(self.allTxs)
        allT.sort(key=lambda x: x.duration, reverse=True)
        return allT

    def isFull(self):
        # Return true if the max no of transactions under work has been reached
        return self.txsUnderWork >= self.maxNrTxs

    def nrTxsInterval(self, secs):
        # Return the number of transactions managed at given time intervals
        if len(self.allTxs) < 2:
            return []

        startTime = self.allTxs[0].creationTime / 1000
        endTime = self.allTxs[-1].creationTime / 1000

        nrTxs = []
        for i in range(1, 3 + (int((endTime - startTime)/secs))):
            nrTxs.append(0)

        for each in self.allTxs:
            t = math.ceil(((each.creationTime/1000) - startTime)/secs) + 1
            t1 = math.ceil(((each.endTime/1000) - startTime)/secs) + 1

            for k in range(t, t1+1):
                nrTxs[k] = nrTxs[k] + 1

        return nrTxs

    def removeTransaction(self, aTransaction):
        self.txsUnderWork -= 1

    def subTxsUnderWork(self):
        self.txsUnderWork = self.txsUnderWork - 1

    def txsDurationInInterval(self, start, stop):
        # Return a list with the duration of every tx within the given interval (given in millisec)
        durations = []

        for each in self.allTxs:
            if each.creationTime >= start and each.endTime <= stop:
                durations.append(each.endTime-each.creationTime)

        return durations

    def txsDurationInInterval(self, start, stop, nameOfFile):
        # Write on the file the duration of every tx within the given interval (given in millisec)
        file = open(nameOfFile, 'w')
        file.write('tx,duration(ms)\n')

        for each in self.allTxs:
            if each.creationTime >= start and each.endTime <= stop:
                file.write(str(each.id))
                file.write(',')
                file.write(str(int((each.endTime-each.creationTime))))

        file.close()

    def txsInInterval2(self, start, stop, step):
        # Return an Array with the nr. of started / ended / active txs for all the given intervals (given in millisec)
        result = []

        for ini in range(start, stop+1, step):
            result.append(self.txsInInterval(ini, step))

        return result

    def txsInInterval(self, start, step):
        # Return the nr. of started / ended / active txs in the given interval
        started = 0
        active = 0
        ended = 0

        for each in self.allTxs:
            code = each.inInterval(start, start+step)
            if code == 0:
                started = started + 1
            if code == 1:
                active = active + 1
            if code == 2:
                ended = ended + 1
            if code == 3:
                started = started + 1
                ended = ended + 1

        return [started, ended, active]

    def txsInInterval_(self, start, stop, step):
        # Return a list with the nr. of started / ended  txs for all the given intervals (given in millisec)
        started = [0] * math.ceil((stop-start)/step)
        ended = [0] * math.ceil((stop-start)/step)

        for each in self.allTxs:
            if each.creationTime >= start and each.endTime <= stop:
                _in = math.floor(((each.creationTime - start)/step))
                started[_in] = started[_in] + 1
                fin = math.floor(((each.endTime - start)/step))
                ended[fin] = ended[fin] + 1

        return [started, ended]

    def txsInInterval(self, start, stop, step, nameOfFile):
        # Write on the file the nr. of started / ended txs for all the given intervals (given in millisec)
        ar = self.txsInInterval_(start, stop, step)
        file = open(nameOfFile, 'w')
        file.write('time,started,ended\n')
        started = ar[0]
        ended = ar[1]
        t = start

        for k in range(0, len(started)):
            file.write(Component.showTime(t))
            file.write(',')
            file.write(str(started[k]))
            file.write(',')
            file.write(str(ended[k]))
            file.write('\n')
            t = t + step
        file.close()

    @staticmethod
    def showTime(timeMsec):
        h = int(timeMsec * 0.001 / 3600)
        m = int(((timeMsec * 0.001) - (h * 3600)) / 60)
        s = round(((timeMsec * 0.001) - (h * 3600) - (m * 60)))
        return str(h) + ':' + str(m) + ':' + str(s)