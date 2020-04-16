import unittest

from riskquant.model import lognormal_magnitude


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.logn = lognormal_magnitude.LognormalMagnitude(1, 10)

    def testDistribution(self):
        # We defined the cdf(low) ~ 0.05 and the cdf(hi) ~ 0.95 so that
        # it would be the 90% confidence interval. Check that it's true.
        self.assertTrue(0.049 < self.logn.distribution.cdf(1) < 0.051)
        self.assertTrue(0.949 < self.logn.distribution.cdf(10) < 0.951)

    def testHardParameters(self):
        # Test difficult-to-fit parameter values
        hard = lognormal_magnitude.LognormalMagnitude(635000, 19000000)
        self.assertAlmostEqual(5922706.83351131, hard.mean())


if __name__ == '__main__':
    unittest.main()
