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
        p = 0.1
        low = 1
        high = 10
        self.s = simpleloss.SimpleLoss('L1', 'loss_name', p, low, high)

    def testVariables(self):
        self.assertEqual(self.s.label, 'L1')
        self.assertEqual(self.s.name, 'loss_name')
        self.assertEqual(self.s.p, 0.1)
        self.assertEqual(self.s.low_loss, 1)
        self.assertEqual(self.s.high_loss, 10)

    def testAnnualized(self):
        # Returns the mean of the configured distribution scaled by the probability
        # of occurrence p
        self.assertAlmostEqual(self.s.annualized_loss(), 0.4040012826945718)

    def testDistribution(self):
        # We defined the cdf(low) ~ 0.05 and the cdf(hi) ~ 0.95 so that
        # it would be the 90% confidence interval. Check that it's true.
        self.assertTrue(0.049 < self.s.distribution.cdf(1) < 0.051)
        self.assertTrue(0.949 < self.s.distribution.cdf(10) < 0.951)

    def testSingleLoss(self):
        # The mean of many single losses should be close to the
        # mean of the distribution. We are not using probability p here.
        iterations = 10000
        mean_loss = sum([self.s.single_loss() for _ in range(iterations)]) / iterations
        self.assertGreater(mean_loss, 3.9)
        self.assertLess(mean_loss, 4.2)

    def testSimulateLossesOneYear(self):
        # Should return a list of zero or more losses that fall mostly within the
        # configured range (1, 10)
        for _ in range(100):
            losses = self.s.simulate_losses_one_year()
            if len(losses) == 0:
                self.assertEqual(sum(losses), 0)
            else:
                self.assertGreater(sum(losses), 0.05)
                self.assertLess(sum(losses), 10000)

    def testSimulateYears(self):
        # Should return a list of length == years
        # whose mean is close to the annualized loss.
        years = 10000
        losses = self.s.simulate_years(years)
        self.assertEqual(len(losses), years)
        mean_loss = sum(losses) / years
        self.assertGreater(mean_loss, 0.36)
        self.assertLess(mean_loss, 0.45)

    def testHardParameters(self):
        # Test difficult-to-fit parameter values
        hard = simpleloss.SimpleLoss('H1', 'hard_loss', 0.07, 635000, 19000000)
        self.assertAlmostEqual(hard.annualized_loss(), 414589.4783457917)

    def testContract(self):
        # Probability must be <= 1.
        try:
            simpleloss.SimpleLoss("L2", "loss2", 10, 100, 1000)  # p > 1
            self.fail("Probability <= 1. not enforced")
        except AssertionError:
            pass

        # Probability must be >= 0.
        try:
            simpleloss.SimpleLoss("L2", "loss2", -1, 100, 1000)  # p < 0
            self.fail("Probability >= 0. not enforced")
        except AssertionError:
            pass

        # High loss must exceed low loss
        try:
            simpleloss.SimpleLoss("L2", "loss2", 0.5, 1000, 100)  # low_loss > high_loss
            self.fail("low_loss <= high_loss not enforced")
        except AssertionError:
            pass
