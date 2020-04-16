import unittest

from riskquant.model import pert_frequency


class TestPERTFrequency(unittest.TestCase):
    def setUp(self):
        min_freq = 0
        max_freq = 10
        most_likely = 5
        kurtosis = 1
        self.s = pert_frequency.PERTFrequency(min_freq, max_freq, most_likely, kurtosis=kurtosis)

    def test_draw_integers(self):
        # Draw returns integer values
        self.assertEqual(int, type(self.s.draw()[0]))

    def test_draw(self):
        num_values = 10000
        total = sum(self.s.draw(num_values))
        self.assertTrue(4.7 < float(total) / float(num_values) < 5.3)

    def test_draw_small(self):
        num_values = 100000
        s = pert_frequency.PERTFrequency(0, 0.01, 0.005, kurtosis=1)
        total = sum(s.draw(num_values))
        self.assertTrue(0.0040 < float(total) / float(num_values) < 0.006)


if __name__ == '__main__':
    unittest.main()
