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
