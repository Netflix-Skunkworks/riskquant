"""A Poisson model suitable for frequency. Returns an array of ints.
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

import numpy as np


class PoissonFrequency(object):
    def __init__(self, frequency):
        """:param frequency = Mean rate per interval"""
        if frequency < 0:
            raise AssertionError("Frequency must be non-negative.")
        self.frequency = frequency

    def draw(self, n=1):
        return np.random.poisson(self.frequency, n)

    def mean(self):
        return self.frequency
