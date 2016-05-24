from collections import Counter
from statistics import mean, median, mode, pvariance, StatisticsError

class CStatistics(object):
    """docstring for CStatistics"""
    def __init__(self, values):
        super(CStatistics, self).__init__()
        self._values = values

    def __repr__(self):
        statistics = [
            "|{:^9}|{:^9}|{:^9}|{:^9}|".format("Mean", "Median", "Mode", "PVariance"),
            "|{:^9}|{:^9}|{:^9}|{:^9}|".format(self.cmean, self.cmedian, self.cmode, self.cpvariance)
        ]
        return "\n".join(statistics)

    def reset(self):
        self._values = None
        self._mean = None
        self._median = None
        self._mode = None
        self._pvariance = None

    @property
    def cmean(self):
        if hasattr(self, '_mean') and self._mean:
            return self._mean
        self._mean = mean(self._values)
        return self._mean

    @property
    def cmedian(self):
        if hasattr(self, '_median') and self._median:
            return self._median
        self._median = median(self._values)
        return self._median

    @property
    def cmode(self):
        if hasattr(self, '_mode') and self._mode:
            return self._mode
        try:
            self._mode = mode(self._values)
        except StatisticsError:
            self._mode = Counter(self._values).most_values()[0]
        except Exception as e:
            self._mode = 0
            print("WARNING -- Most common value canno't be found : %s" % e)
        return self._mode

    @property
    def cpvariance(self):
        if hasattr(self, '_pvariance') and self._pvariance:
            return self._pvariance
        self._pvariance = pvariance(self._values)
        return self._pvariance
