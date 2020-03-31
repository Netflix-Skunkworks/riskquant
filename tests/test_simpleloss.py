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

import unittest

from riskquant import simpleloss


class Test(unittest.TestCase):
    def setUp(self):
        frequency = 0.1
        low = 1
        high = 10
        self.s = simpleloss.SimpleLoss('L1', 'loss_name', frequency, low, high)

    def testVariables(self):
        self.assertEqual(self.s.label, 'L1')
        self.assertEqual(self.s.name, 'loss_name')
        self.assertEqual(self.s.frequency, 0.1)
        self.assertEqual(self.s.low_loss, 1)
        self.assertEqual(self.s.high_loss, 10)

    def testAnnualized(self):
        # Returns the mean of the configured distribution scaled by the probability
        # of occurrence p
        self.assertAlmostEqual(self.s.annualized_loss(), 0.4040012826945718)

    def testLargeFrequency(self):
        lg = simpleloss.SimpleLoss('Large', 'large_loss', 3.0, 1, 10)
        self.assertAlmostEqual(lg.annualized_loss(), 12.120038480837177)  # 30x the value above

    def testSimulateLossesOneYear(self):
        # Should return a list of zero or more losses that fall mostly within the
        # configured range (1, 10)
        self.s = simpleloss.SimpleLoss('L1', 'loss_name', 10, 1, 10)
        for _ in range(100):
            losses = self.s.simulate_losses_one_year()
            if len(losses) == 0:
                self.assertEqual([], losses)
            else:
                self.assertGreater(100, len(losses))
                self.assertLess(0.05 * len(losses), sum(losses))
                self.assertGreater(100 * len(losses), sum(losses))

    def testSimulateYears(self):
        # Should return a list of length == years
        # whose mean is close to the annualized loss.
        years = 10000
        losses = self.s.simulate_years(years)
        self.assertEqual(len(losses), years)
        mean_loss = sum(losses) / years
        self.assertGreater(mean_loss, 0.36)
        self.assertLess(mean_loss, 0.45)

    def testContract(self):
        # Frequency must be >= 0.
        self.assertRaises(AssertionError, simpleloss.SimpleLoss, "L2", "loss2", -1, 100, 1000)

        # High loss must exceed low loss
        self.assertRaises(AssertionError, simpleloss.SimpleLoss, "L2", "loss2", 0.5, 1000, 100)
