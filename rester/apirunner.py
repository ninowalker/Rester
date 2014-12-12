from docopt import docopt
from rester.loader import load, TestSuite
from rester.output import display_report
from testcase import ApiTestCaseRunner
import logging
import sys


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
    test_runner = ApiTestCaseRunner(arguments)

    suite = None
    var_file = arguments.get('--vars')
    if var_file:
        suite = TestSuite(var_file)
        suite.load()

    for f in arguments["<files>"]:
        o = load(f, open(f))
        if 'test_cases' in o:
            test_runner.run_test_suite(f)
        else:
            test_runner.run_test_case(f, suite)
    display_report(test_runner)
    return any((result.get('failed') for result in test_runner.results))

if (__name__ == '__main__'):
    sys.exit(run())
