"""A magnitude model based on the lognormal distribution define by a 90% confidence interval
"""

#   Copyright 2019-2020 Netflix, Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import math

from scipy.stats import norm
from scipy.stats import lognorm


class LognormalMagnitude(object):
    def __init__(self, low_loss, high_loss):
        """:param  low_loss = Low loss estimate
        :param high_loss = High loss estimate

        The range low_loss -> high_loss should represent the 90% confidence interval
        that the loss will fall in that range.

        These values are then fit to a lognormal distribution so that they fall at the 5% and
        95% cumulative probability points.
        """
        if low_loss >= high_loss:
            # High loss must exceed low loss
            raise AssertionError
        self.low_loss = low_loss
        self.high_loss = high_loss
        self._setup_lognormal(low_loss, high_loss)

    def _setup_lognormal(self, low_loss, high_loss):
        # Set up the lognormal distribution
        factor = -0.5 / norm.ppf(0.05)
        mu = (math.log(low_loss) + math.log(high_loss)) / 2.  # Average of the logn of low/high
        shape = factor * (math.log(high_loss) - math.log(low_loss))  # Standard deviation
        self.distribution = lognorm(shape, scale=math.exp(mu))

    def draw(self, n=1):
        return self.distribution.rvs(size=n)

    def mean(self):
        return self.distribution.mean()
