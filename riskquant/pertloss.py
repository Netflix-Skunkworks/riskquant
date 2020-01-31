"""A loss model based on a single loss scenario with

* low_loss = Low loss amount
* high_loss = High loss amount
* min_freq: The lowest number of times a loss will occur
* max_freq: The highest number of times a loss will occur
* most_likely_freq: The most likely number of times a loss will occur over some interval of time.
* kurtosis: Defaults to 4.  Controls the shape of the distribution. Higher values cause a sharper peak.


The range low_loss -> high_loss should represent the 90% confidence interval
that the loss will fall in that range.

These values are then fit to a lognormal
distribution so that they fall at the 5% and 95% cumulative probability points.

The range min_freq -> max_freq should represent the 90% confidence interval
that the frequency will fall in that range.

The most_likely_freq will be used to skew the PERT distribution so that more of these values occur in the simulation.

The kurtosis will be used to control the shape of the distribution; even more of the most_likely_freq values will
occur in the simulation with higher kurtosis.

These values are then used to create Modified PERT distribution.

"""
import math

import numpy as np
from scipy.stats import lognorm, mode, norm
import tensorflow_probability as tfp


tfp = tfp.experimental.substrates.numpy
tfd = tfp.distributions
factor = -0.5 / norm.ppf(0.05)


class PERTLoss:
    def __init__(self, low_loss, high_loss, min_freq, max_freq, most_likely_freq, kurtosis=4):
        if min_freq >= max_freq:
            # Min frequency must exceed max frequency
            raise AssertionError
        if not min_freq <= most_likely_freq <= max_freq:
            # Most likely should be between min and max frequencies.
            raise AssertionError
        if low_loss >= high_loss:
            # High loss must exceed low loss
            raise AssertionError

        # Set up the lognormal distribution
        mu = (math.log(low_loss) + math.log(high_loss)) / 2.  # Average of the logn of low/high
        shape = factor * (math.log(high_loss) - math.log(low_loss))  # Standard deviation
        self.magnitude_distribution = lognorm(shape, scale=math.exp(mu))

        # Set up the PERT distribution
        # From FAIR: the most likely frequency will set the skew/peak, and
        # the "confidence" in the most likely frequency will set the kurtosis/temp of the distribution.
        self.frequency_distribution = tfd.PERT(low=min_freq, peak=most_likely_freq, high=max_freq, temperature=kurtosis)

    def annualized_loss(self):
        """Expected mean loss per year as scaled by the most likely frequency

        :returns: Scalar of expected mean loss on an annualized basis."""

        return self.frequency_distribution.mode().flat[0] * self.magnitude_distribution.mean()

    def single_loss(self):
        """Draw a single loss amount. Not scaled by probability of occurrence.

        :returns: Scalar value of a randomly generated single loss amount."""

        return self.magnitude_distribution.rvs()

    def simulate_losses_one_year(self):
        """Generate a random frequency and random magnitude from distributions.

        :returns: Scalar value of one sample loss exposure."""
        sample_frequency = self.frequency_distribution.sample(1)[0]
        sample_magnitude = self.single_loss()
        loss = sample_frequency * sample_magnitude
        return loss

    def simulate_years(self, n):
        """Draw randomly to simulate n years of possible losses.

        :arg: n = Number of years to simulate
        :returns: Numpy array of shape (n,) with loss amounts per year."""
        # Create array of possible frequencies
        frequency_array = self.frequency_distribution.sample(n)
        # The loss amounts for all the losses across all the years, generated all at once.
        # This is much higher performance than generating one year at a time.
        magnitude_array = self.magnitude_distribution.rvs(size=n)
        # Multiply frequency times magnitude from each array.
        loss_array = frequency_array * magnitude_array
        return loss_array

    @staticmethod
    def summarize_loss(loss_array):
        """Get statistics about a numpy array.
        Risk is a range of possibilities, not just one outcome.

        :arg: loss_array = Numpy array of simulated losses
        :returns: Dictionary of statistics about the loss
        """
        percentiles = np.percentile(loss_array, [10, 50, 90]).astype(int)
        loss_summary = {'minimum': loss_array.min().astype(int),
                        'tenth_percentile': percentiles[0],
                        'mode': mode(loss_array)[0][0].astype(int),
                        'median': percentiles[1],
                        'ninetieth_percentile': percentiles[2],
                        'maximum': loss_array.max().astype(int)}
        return loss_summary
