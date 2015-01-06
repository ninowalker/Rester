from logging import getLogger
from rester.exc import TestCaseExec
from rester.loader import TestSuite, TestCase
import unittest


LOG = getLogger(__name__)


class ApiTestCaseRunner:
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


#class ResterTestSuite(unittest.TestSuite):
#    @classmethod
#    def load_tests(cls, filename):
#        suite = TestSuite(filename)
#        suite.load()
#        for test in suite.test_cases:
#            self.addTest(ResterTestCase(test))

class ResterTestCase(unittest.TestCase):
    filename = None
    case = None
    suite = None
    _GEN = 0

    @classmethod
    def new(cls, filename=None, case=None, suite=None, options={}):
        cls._GEN += 1
        test = type('ResterTestCase_%s' % cls._GEN, (ResterTestCase,),
                    dict(filename=filename, case=case, suite=suite, options=options))
        return test

    @classmethod
    def setUpClass(cls):
        if cls.filename:
            LOG.info("Loading %s", cls.filename)
            cls.case = TestCase(cls.filename, cls.suite)
        cls.case.load()

    def test_steps(self):
        tc = TestCaseExec(self.case, self.options)
        tc()

