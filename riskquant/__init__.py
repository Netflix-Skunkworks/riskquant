"""Risk quantification library. Import models in this package as needed."""

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

from argparse import ArgumentParser
import csv
import os
import sys

from riskquant import multiloss
from riskquant import simpleloss


__appname__ = 'riskquant'
__version__ = '1.0.3'

NAME_VERSION = '%s %s' % (__appname__, __version__)


def csv_to_simpleloss(file):
    """Convert a csv file with parameters to SimpleModel objects

    :arg: file = Name of CSV file to read. Each row should contain rows with
                 name, probability, low_loss, high_loss

    :returns: List of SimpleLoss objects
    """

    loss_list = []
    with open(file, 'r', newline='\n') as csvfile:
        loss_reader = csv.reader(csvfile)
        for label, name, p, low_loss, high_loss in loss_reader:
            label: str
            name: str
            loss_list += [simpleloss.SimpleLoss(
                label, name, float(p), float(low_loss), float(high_loss))]
    return loss_list


def _sigdigs(number, digits):
    """Round the provided number to a desired number of significant digits
    :arg: number = A floating point number
          digits = How many significant digits to keep
    :returns: A formatted currency string rounded to 'digits' significant digits.
              Example: _sigdigs(1234.56, 3) returns $1,230"""
    float_format = "{:." + str(digits) + "g}"
    return "${:,.0f}".format(float(float_format.format(number)))


def main(args=None):
    parser = ArgumentParser(args)

    parser.add_argument('--file', metavar='FILE', help='CSV of scenario name and parameters')

    parser.add_argument('-V', '--version', action='version', version=NAME_VERSION)

    parser.add_argument('--years', help='number of years to simulate', type=int)
    parser.add_argument('--sigdigs', help='number of significant digits in output values')

    parser.add_argument('--plot', dest='plot', action='store_true')

    parser.set_defaults(plot=False,
                        years=100000,
                        sigdigs=3)

    if args:
        args = parser.parse_args(args)
    else:
        args = parser.parse_args()

    if args.file:
        loss_list = csv_to_simpleloss(args.file)
    else:
        loss_list = None

    m = multiloss.MultiLoss(loss_list)
    priorities = m.prioritized_losses()
    if args.file:
        path, ext = os.path.splitext(args.file)
        output = path + '_prioritized' + ext
        sys.stderr.write("Writing prioritized threats to:\n{}\n".format(output))
        with open(output, 'w') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
            for label, name, annualized_loss in priorities:
                writer.writerow([label, name, _sigdigs(annualized_loss, args.sigdigs)])
        if args.plot:
            m.loss_exceedance_curve(args.years, savefile=path + '.png')
    else:
        print("\n".join([str(x) for x in priorities]))
        if args.plot:
            m.loss_exceedance_curve(args.years)

    return 0


if __name__ == '__main__':
    main(sys.argv[1:])
