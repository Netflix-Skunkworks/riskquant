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

import math

from scipy.stats import norm
from scipy.stats import lognorm
import numpy as np


class SimpleLoss:
    def __init__(self, label, name, frequency, low_loss, high_loss):
        if frequency < 0:
            # Frequency must be non-negative
            raise AssertionError
        if low_loss >= high_loss:
            # High loss must exceed low loss
            raise AssertionError
        self.label = label
        self.name = name
        self.frequency = frequency
        self.low_loss = low_loss
        self.high_loss = high_loss

        # Set up the lognormal distribution
        factor = -0.5 / norm.ppf(0.05)
        mu = (math.log(low_loss) + math.log(high_loss)) / 2.  # Average of the logn of low/high
        shape = factor * (math.log(high_loss) - math.log(low_loss))  # Standard deviation
        self.distribution = lognorm(shape, scale=math.exp(mu))

    def annualized_loss(self):
        """Expected mean loss per year as scaled by the probability of occurrence

        :returns: Scalar of expected mean loss on an annualized basis."""

        return self.frequency * self.distribution.mean()

    def single_loss(self):
        """Draw a single loss amount. Not scaled by probability of occurrence.

        :returns: Scalar value of a randomly generated single loss amount."""

        return self.distribution.rvs()

    def simulate_losses_one_year(self):
        """Generate a random number of losses, and loss amount for each.

        :returns: List of loss amounts, or empty list if no loss occurred."""
        num_losses = np.random.poisson(self.frequency, 1)[0]
        return [self.single_loss() for _ in range(num_losses)]

    def simulate_years(self, n):
        """Draw randomly to simulate n years of possible losses.

        :arg: n = Number of years to simulate
        :returns: List of length n with loss amounts per year. Amount is 0 if no loss occurred."""
        # Generate a loss count (of value 0+) for each year being simulated
        losses_each_year = np.random.poisson(self.frequency, n)
        # The total number of loss events across all years
        total_loss_count = sum(losses_each_year)
        # The loss amounts for all the losses across all the years, generated all at once.
        # This is much higher performance than generating one year at a time.
        all_losses = self.distribution.rvs(size=total_loss_count)
        # Create a list of len(n) with the sum of losses in each simulated year.
        i = 0
        year = 0
        result = []
        while year < len(losses_each_year):
            losses_this_year = losses_each_year[year]
            # Extend the result list by the sum of losses that occurred in this simulated
            # year. Here we are drawing 'losses_this_year' loss events from the all_losses
            # list and summing just those.
            result += [sum(all_losses[i:i + losses_this_year])]
            # Iterate the offset into the all_losses array
            i += losses_this_year
            # Iterate the year being examined.
            year += 1
        return result
