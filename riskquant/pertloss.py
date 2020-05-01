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

from riskquant import loss
from riskquant.model import lognormal_magnitude, pert_frequency


class PERTLoss(loss.Loss):
    def __init__(self, low_loss, high_loss, min_freq, max_freq, most_likely_freq, kurtosis=4):
        self.frequency_model = pert_frequency.PERTFrequency(min_freq, max_freq, most_likely_freq, kurtosis)
        self.magnitude_model = lognormal_magnitude.LognormalMagnitude(low_loss, high_loss)
        super(PERTLoss, self).__init__(
            self.frequency_model,
            self.magnitude_model)
