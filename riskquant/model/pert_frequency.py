"""A PERT model suitable for frequency. Returns an array of ints.
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
import tensorflow_probability as tfp


class PERTFrequency(object):

    def __init__(self, min_freq, max_freq, most_likely_freq, kurtosis):
        """:param frequency = Mean rate per interval"""
        if min_freq >= max_freq:
            # Min frequency must exceed max frequency
            raise AssertionError
        if not min_freq <= most_likely_freq <= max_freq:
            # Most likely should be between min and max frequencies.
            raise AssertionError

        # Set up the PERT distribution
        # From FAIR: the most likely frequency will set the skew/peak, and
        # the "confidence" in the most likely frequency will set the kurtosis/temp of the distribution.
        self.distribution = tfp.experimental.substrates.numpy.distributions.PERT(
            low=min_freq, peak=most_likely_freq, high=max_freq, temperature=kurtosis)

    def draw(self, n=1):
        return [np.random.poisson(x) for x in self.distribution.sample(n)]

    def mean(self):
        return self.distribution.mode().flat[0]
