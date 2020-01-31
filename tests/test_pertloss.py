import unittest

from riskquant import pertloss


class Test(unittest.TestCase):
    def setUp(self):
        min_freq = 0.1
        max_freq = .7
        most_likely = .3
        kurtosis = 1
        low_loss = 1
        high_loss = 10
        self.s = pertloss.PERTLoss(low_loss, high_loss, min_freq, max_freq, most_likely, kurtosis=kurtosis)

    def testAnnualized(self):
        # Returns the mean of the configured distribution scaled by the mode of frequency distribution
        self.assertAlmostEqual(self.s.annualized_loss(), 1.2120038962444237)

    def testDistribution(self):
        # We defined the cdf(low) ~ 0.05 and the cdf(hi) ~ 0.95 so that
        # it would be the 90% confidence interval. Check that it's true.
        self.assertTrue(0.049 < self.s.magnitude_distribution.cdf(1) < 0.051)
        self.assertTrue(0.949 < self.s.magnitude_distribution.cdf(10) < 0.951)

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
        losses = []
        for _ in range(100):
            losses.append(self.s.simulate_losses_one_year())
            self.assertGreater(sum(losses), 0.05)
            self.assertLess(sum(losses), 10000)

    def testSimulateYears(self):
        # Should return a list of length == years
        # whose mean is close to the annualized loss.
        years = 10000
        losses = self.s.simulate_years(years)
        self.assertEqual(len(losses), years)
        mean_loss = sum(losses) / years
        self.assertGreater(mean_loss, 0.5)
        self.assertLess(mean_loss, 1.5)

    def testMinMaxFrequency(self):
        # Min must be less than max.
        with self.assertRaises(AssertionError):
            pertloss.PERTLoss(10, 100, .7, .1, .3)  # min > max

    def testMostLikelyFrequency(self):
        # Most likely frequency must be between min and max.
        with self.assertRaises(AssertionError):
            pertloss.PERTLoss(10, 100, .1, .7, .8)  # most_likely > max

    def testLowHighLoss(self):
        # High loss must exceed low loss
        with self.assertRaises(AssertionError):
            pertloss.PERTLoss(100, 10, .1, .7, .3)  # min > max

    def testSummary(self):
        loss_array = self.s.simulate_years(1000)
        summary = self.s.summarize_loss(loss_array)
        self.assertEqual(summary['minimum'], 0)
        self.assertEqual(summary['tenth_percentile'], 0)
        self.assertEqual(summary['mode'], 0)
        self.assertGreaterEqual(summary['median'], 1)
        self.assertGreaterEqual(summary['ninetieth_percentile'], 2)
        self.assertGreater(summary['maximum'], 5)
