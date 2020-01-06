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

import sys

from matplotlib import pyplot as plt
from matplotlib import ticker as mtick
import numpy as np


class MultiLoss(object):
    """A container for a list of loss objects and methods for generating summaries of them."""

    def __init__(self, loss_list):
        self.loss_list = loss_list

    def prioritized_losses(self):
        """Generate a prioritized list of losses from the loss list.

        :returns: List of [(name, annualized_loss), ...] in descending order of annualized_loss.
        """
        result = [(loss.label, loss.name, loss.annualized_loss()) for loss in self.loss_list]
        return sorted(result, key=lambda x: x[2], reverse=True)

    def simulate_years(self, n):
        """Simulate n years across all the losses in the list.

        :arg: n = The number of years to simulate

        :returns: List of [loss_year_1, loss_year_2, ...] where each is a sum of all
                  losses experienced that year."""

        return np.array([loss.simulate_years(n) for loss in self.loss_list]).sum(axis=0)

    def loss_exceedance_curve(self,
                              n,
                              title="Aggregated Loss Exceedance",
                              xlim=[1000000, 10000000000],
                              savefile=None):
        """Generate the Loss Exceedance Curve for the list of losses. (Uses simulate_years)

        :arg: n = Number of years to simulate and display the LEC for.
              [title] = An alternative title for the plot.
              [xlim] = An alternative lower and upper limit for the plot's x axis.
              [savefile] = Save a PNG version to this file location instead of displaying.

        :returns: None. If display=False, returns the matplotlib axis array
                  (for customization)."""

        losses = np.array([np.percentile(self.simulate_years(n), x) for x in range(1, 100, 1)])
        percentiles = np.array([float(100 - x) / 100.0 for x in range(1, 100, 1)])
        _ = plt.figure()
        ax = plt.gca()
        ax.plot(losses, percentiles)
        plt.title(title)
        ax.set_xscale("log")
        ax.set_ylim(0.0, percentiles[np.argmax(losses > 0.0)] + 0.05)
        ax.set_xlim(xlim[0], xlim[1])
        xtick = mtick.StrMethodFormatter('${x:,.0f}')
        ax.xaxis.set_major_formatter(xtick)
        ytick = mtick.StrMethodFormatter('{x:.000%}')
        ax.yaxis.set_major_formatter(ytick)
        plt.grid(which='both')
        if savefile:
            sys.stderr.write("Saving plot to {}\n".format(savefile))
            plt.savefig(savefile)
        else:
            plt.show()
