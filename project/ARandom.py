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


import math
import random
import random as r


class ARandom:

    def eventFrom(self, probArray):
        # probArray holds a set of probabilities that a different event happens. The sum of probArray values
        # must be 1. Return the index in probArray of the event actually happening.

        rnd = r.random()
        accum = 0.0

        for k in range(0, len(probArray)):
            accum = accum + probArray[k]
            if rnd < accum:
                return k

        return 'Sum of probabilities < 1'

    def gaussian(self):
        # Answer a normally distributed random number with zero mean and standard deviation 1.0.
        gauss = 0.0

        for k in range(0, 12):
            gauss = gauss + r.random()

        return gauss - 6.0

    def gauss(self, avg, std):
        # Returns a random number with Gaussian distribution having average avg and s.d. std
        return avg + (self.gaussian() * std)

    def logNormal(self, avg, std):
        # Returns a random number with Lognormal distribution having average avg and s.d. std
        lm = math.log(avg**2 / math.sqrt((avg**2 + std**2)))
        ls = math.sqrt(math.log((avg**2 + std**2)/avg**2))
        return math.exp(self.gauss(lm, ls))

    def rand(self):
        # Returns a random number
        return r.random()
