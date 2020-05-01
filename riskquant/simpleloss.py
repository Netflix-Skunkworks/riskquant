"""A simple loss model based on a single loss scenario with
* label = An identifier for the scenario
* name = A descriptive name for the scenario
* p = Probability of occurring within one year
* low_loss = Low loss amount
* high_loss = High loss amount

The range low_loss -> high_loss should represent the 90% confidence interval
that the loss will fall in that range.

These values are then fit to a lognormal
distribution so that they fall at the 5% and 95% cumulative probability points.
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

from riskquant import loss
from riskquant.model import lognormal_magnitude, poisson_frequency


class SimpleLoss(loss.Loss):
    def __init__(self, label, name, frequency, low_loss, high_loss):
        self.label = label
        self.name = name
        self.frequency = frequency
        self.low_loss = low_loss
        self.high_loss = high_loss
        super(SimpleLoss, self).__init__(
            poisson_frequency.PoissonFrequency(frequency),
            lognormal_magnitude.LognormalMagnitude(low_loss, high_loss))
