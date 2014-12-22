from __future__ import absolute_import
import time
import logging
from splinter import Browser


LOG = logging.getLogger(__name__)


def render(context):
    browser = context.case.variables['browser']
    browser.visit(context.step.url)
    if getattr(context.step, 'sleep', None):
        time.sleep(context.step.sleep)


def run(case, **kwargs):
    browser = Browser(**kwargs)
    case.variables.add_variable('browser', browser)
    return browser.quit
