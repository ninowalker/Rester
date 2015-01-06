from docopt import docopt
from rester.loader import load, TestSuite
from rester.output import display_report
from testcase import ResterTestCase
import logging
import sys
import unittest


def run():
    """
Rester Test Runner.

Usage:
  apirunner [options] <files>...
  apirunner -h | --help
  apirunner --version

Options:
  -h --help       Show this screen.
  --log=<level>   LOG level [default: INFO].
  --vars=<varfile>   Load variables
    """
    arguments = docopt(run.__doc__, version='apirunner 1.0')
    if arguments.get('--help'):
        print run.__doc__
        return 0
    log_level = arguments.get("--log", "INFO").upper()
    logging.basicConfig()
    logger = logging.getLogger('rester')
    logger.setLevel(log_level)

    suites = []
    for fname in arguments["<files>"]:
        cls = ResterTestCase.new(filename=fname)
        suite = unittest.TestLoader().loadTestsFromTestCase(cls)
        suites.append(suite)
    runner = unittest.TextTestRunner()
    return runner.run(unittest.TestSuite(suites))

    #return unittest.TestLoader().loadTestsFromTestCase

if __name__ == '__main__':
    sys.exit(run())
