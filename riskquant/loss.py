"""A generic loss container that can be populated with different models.
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


class Loss(object):
    def __init__(self, frequency_model, magnitude_model):
        """:param frequency_model: A class with method draw(n=1) to draw a list of n int values
        :param magnitude_model: A class with method draw(n=1) to draw a list of n float values
        """
        self.frequency_model = frequency_model
        self.magnitude_model = magnitude_model

    def annualized_loss(self):
        return self.frequency_model.mean() * self.magnitude_model.mean()

    def simulate_losses_one_year(self):
        """:return List of zero or more loss magnitudes for a single simulated year"""
        num_losses = self.frequency_model.draw()[0]  # Draw a single number of events
        return list(self.magnitude_model.draw(num_losses))

    def simulate_years(self, n):
        """:param n = Number of years to simulate
        :return A list of length n, each entry is the sum of losses for that simulated year"""
        num_losses = self.frequency_model.draw(n)  # Draw a list of the number of events in each year
        loss_values = self.magnitude_model.draw(sum(num_losses))
        losses = [0] * n
        losses_used = 0
        for i in range(n):
            new_losses = num_losses[i]
            losses[i] = sum(loss_values[losses_used:losses_used + new_losses])
            losses_used += new_losses
        return losses
