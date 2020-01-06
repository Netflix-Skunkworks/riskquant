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

from riskquant import multiloss


class FixedValueLoss(object):
    """Loss model where loss is a single fixed value each year."""
    def __init__(self, label, name, value):
        self.label = label
        self.name = name
        self.value = value

    def annualized_loss(self):
        return self.value

    def simulate_years(self, n):
        return [self.value for _ in range(n)]


class TestMultiLoss(unittest.TestCase):
    def setUp(self):
        self.m = multiloss.MultiLoss(
            [FixedValueLoss('L1', 'loss1', 1),
             FixedValueLoss('L2', 'loss2', 2)])

    def test_prioritized_losses(self):
        losses = self.m.prioritized_losses()
        expected = [('L2', 'loss2', 2),
                    ('L1', 'loss1', 1)]
        for i in range(len(expected)):
            self.assertEqual(losses[i][0], expected[i][0])        # Labels match
            self.assertEqual(losses[i][1], expected[i][1])        # Names match
            self.assertAlmostEqual(losses[i][2], expected[i][2])  # Amounts match

    def test_simulate_years(self):
        years = 10
        result = self.m.simulate_years(years)
        self.assertEqual(len(result), years)
        for elem in result:
            self.assertTrue(elem == 3)


if __name__ == '__main__':
    unittest.main()
