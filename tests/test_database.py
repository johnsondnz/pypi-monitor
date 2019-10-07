#!/usr/bin/env python

"""
Tests that the database structure is correct.
Tests that the key value pairs are valid.
"""

import unittest
import requests
import json
import sys
sys.path.append("..")
from box import Box
import xmlrunner

with open("app/database.json", "r") as json_file:
    database = json.load(json_file)


class TestDatabase(unittest.TestCase):
    def test_structure(self):
        """
        Test the database structure
        """
        self.assertIsInstance(database, list)
        for package in database:
            package = Box(package)
            self.assertIsInstance(package, dict)
            self.assertIsInstance(package.repository, dict)
            self.assertIn("pypi_tracked", package)
            self.assertIn("scm_base_url", package.repository)
            self.assertIn("owner_user", package.repository)
            self.assertIn("repo_name", package.repository)
            self.assertIn("ssh_checkout", package.repository)
            self.assertIn("version_file", package.repository)

    def test_tracked_package_exists(self):
        """
        Verify tracked package exists in pypi
        """
        for package in database:
            package = Box(package)
            r = requests.get(f"https://pypi.python.org/pypi/{package.pypi_tracked}/json")
            self.assertEqual(200, r.status_code)

    def test_my_repo_exists(self):
        """
        Verify user repository exists
        """
        for package in database:
            repository = Box(package["repository"])
            r = requests.get(f"{repository.scm_base_url}/{repository.owner_user}/{repository.repo_name}")
            self.assertEqual(200, r.status_code)

    def test_versionfile_exists(self):
        """
        Verify repository versionfile exists
        """
        for package in database:
            repository = Box(package["repository"])
            r = requests.get(f"{repository.version_file}")
            self.assertEqual(200, r.status_code)

    def test_data(self):
        """
        Tests the key value pairs for correct instance types
        """
        for package in database:
            package = Box(package)
            repository = Box(package.repository)
            self.assertIsInstance(package.pypi_tracked, str)
            self.assertIsInstance(repository.scm_base_url, str)
            self.assertIsInstance(repository.owner_user, str)
            self.assertIsInstance(repository.repo_name, str)
            self.assertIsInstance(repository.ssh_checkout, str)
            self.assertIsInstance(repository.version_file, str)


if __name__ == "__main__":
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        failfast=False, buffer=False, catchbreak=False
    )
