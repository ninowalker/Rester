from logging import getLogger
from rester.exc import TestCaseExec
from rester.loader import TestSuite, TestCase


class ApiTestCaseRunner:
    logger = getLogger(__name__)

    def __init__(self, options={}):
        self.options = options
        self.results = []

    def run_test_suite(self, test_suite_file_name):
        test_suite = TestSuite(test_suite_file_name)
        test_suite.load()
        for test in test_suite.test_cases:
            self._run_case(test)

    def run_test_case(self, test_case_file_name, suite=None):
        case = TestCase(test_case_file_name, suite)
        case.load()
        self._run_case(case)

    def _run_case(self, case):
        tc = TestCaseExec(case, self.options)
        self.results.append(tc())


#TODO
# Support enums
# post processing
