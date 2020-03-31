import unittest

from riskquant import loss


class FixedValueModel(object):
    def __init__(self, value):
        self.value = value

    def draw(self, n=1):
        return [self.value] * n


class TestLoss(unittest.TestCase):
    def test_simulate_losses_one_year(self):
        loss_model = loss.Loss(FixedValueModel(1), FixedValueModel(0.5))
        single_loss = loss_model.simulate_losses_one_year()
        self.assertEqual([0.5], single_loss)

    def test_simulate_losses_one_year_multiple_loss(self):
        loss_model = loss.Loss(FixedValueModel(3), FixedValueModel(0.5))
        single_loss = loss_model.simulate_losses_one_year()
        self.assertEqual([0.5, 0.5, 0.5], single_loss)

    def test_simulate_years(self):
        loss_model = loss.Loss(FixedValueModel(1), FixedValueModel(0.5))
        multiple_years = loss_model.simulate_years(3)
        self.assertEqual([0.5, 0.5, 0.5], multiple_years)

    def test_simulate_years_frequency(self):
        loss_model = loss.Loss(FixedValueModel(2), FixedValueModel(0.5))
        multiple_years = loss_model.simulate_years(3)
        self.assertEqual([1.0, 1.0, 1.0], multiple_years)

    def test_simulate_zeros(self):
        loss_model = loss.Loss(FixedValueModel(0), FixedValueModel(0.5))
        multiple_years = loss_model.simulate_years(3)
        self.assertEqual([0, 0, 0], multiple_years)


if __name__ == '__main__':
    unittest.main()
