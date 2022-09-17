class Transaction:

    def __init__(self):
        self.actor = None
        self.component = None
        self.creationTime = 0
        self.endTime = 0
        self.id = 0
        self.next = None
        self.previous = None
        self.type = None

    def duration(self):
        # Return the duration of the tx in sec
        return (self.endTime - self.creationTime) / 1000

    def durationInMsec(self):
        # Return the duration in milliseconds
        return self.endTime - self.creationTime

    def first(self):
        if self.previous is None:
            return self
        return self.previous.first()

    def firstId(self):
        return self.first().id

    def firstTime(self):
        return self.first().creationTime

    def interval(self, start, end):
        # Return
        # -1 if the receiver is not active in the given interval;
        # 0 if the receiver started in the interval;
        # 1 if the receiver is active in the whole interval;
        # 2 if the receiver ended in the interval;
        # 3 if the receiver started and ended in the interval"

        if self.creationTime > end or self.endTime < start:
            return -1
        if self.creationTime < start:
            if self.endTime > end:
                return 1
            else:
                return 2
        else:
            if self.endTime > end:
                return 0
            else:
                return 3
