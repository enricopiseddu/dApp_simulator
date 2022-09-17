import math
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
        ls = math.sqrt(math.log(avg**2 + std**2)/avg**2)
        return math.exp(self.gauss(lm, ls))

    def rand(self):
        # Returns a random number
        return r.random()
