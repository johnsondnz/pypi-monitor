#!/usr/bin/env python3

"""
Tests the get_verion method of the app
"""

import sys
sys.path.append("..")
import unittest
import xmlrunner
from app.app import get_version
from packaging.version import Version


class TestGetVersion(unittest.TestCase):
    def test_get_version(self):
        version = get_version('ansible')
        self.assertIsInstance(version, Version)


if __name__ == "__main__":
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        failfast=False, buffer=False, catchbreak=False
    )
