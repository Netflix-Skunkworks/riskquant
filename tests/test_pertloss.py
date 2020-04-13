import unittest

from riskquant import pertloss


class TestPERTLoss(unittest.TestCase):
    def setUp(self):
        self.min_freq = 0.1
        self.max_freq = .7
        most_likely = .3
        kurtosis = 1
        low_loss = 1
        high_loss = 10
        self.s = pertloss.PERTLoss(low_loss, high_loss, self.min_freq, self.max_freq, most_likely, kurtosis=kurtosis)

    def testAnnualized(self):
        # Returns the mean of the configured distribution scaled by the mode of frequency distribution
        self.assertAlmostEqual(self.s.annualized_loss(), 1.2120038962444237)

    def testSimulateLossesOneYear(self):
        # Should return a list of zero or more losses that fall mostly within the
        # configured range (1, 10)
        count = 0
        years = 100
        for _ in range(years):
            losses = self.s.simulate_losses_one_year()
            count += len(losses)
            for loss in losses:
                self.assertGreater(loss, 0.05)
                self.assertLess(loss, 10000)
        self.assertTrue(0.5 * self.min_freq * years < count < self.max_freq * years * 2)

    def testSimulateYears(self):
        # Should return a list of length == years
        # whose mean is close to the annualized loss.
        years = 10000
        losses = self.s.simulate_years(years)
        self.assertEqual(len(losses), years)
        mean_loss = sum(losses) / years
        self.assertGreater(mean_loss, 0.25)
        self.assertLess(mean_loss, 2)

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
