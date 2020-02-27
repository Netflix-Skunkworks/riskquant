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
import os
import tempfile

import riskquant


class TestRiskquant(unittest.TestCase):
    """Test the functions implemented in riskquant/__init__.py"""

    def test_csv_to_simpleloss(self):
        csvdata = "L1,loss1,0.1,1,10\n" \
                  "L2,loss2,0.2,1,10"
        expected = [('L1', 'loss1', 0.1, 1, 10),  # name, p, low_loss, high_loss
                    ('L2', 'loss2', 0.2, 1, 10)]

        path = TestRiskquant._write_to_tempfile(csvdata)
        losses = riskquant.csv_to_simpleloss(path)
        for i in range(len(expected)):
            loss = (losses[i].label, losses[i].name, losses[i].frequency,
                    losses[i].low_loss, losses[i].high_loss)
            for j in range(5):
                self.assertEqual(loss[j], expected[i][j])

    @staticmethod
    def _write_to_tempfile(data):
        fp, path = tempfile.mkstemp()
        os.write(fp, data.encode('UTF-8'))
        os.close(fp)
        return path


if __name__ == '__main__':
    unittest.main()
