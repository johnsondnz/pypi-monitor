#!/usr/bin/env python3

import os
import json
import requests
from git import Repo
from logzero import logger
from box import Box
from packaging.version import parse

# define base URL for get requests
base_url = "https://pypi.python.org/pypi/{package}/json"

# open and load the database
with open(os.path.join(os.path.dirname(__file__), "database.json"), "r") as json_file:
    database = json.load(json_file)


def get_version(package, url_pattern=base_url):

    r = requests.get(url_pattern.format(package=package))
    version = parse('0')

    if r.status_code == requests.codes.ok:
        j = r.json()
        releases = j.get('releases', [])
        for release in releases:
            ver = parse(release)
            if not ver.is_prerelease:
                version = max(version, ver)
    return version


def main():

    # loop through the database
    for package in database:
        package = Box(package)
        repository = Box(package.repository)
        pypi_version = get_version(package.pypi_tracked)
        logger.info(f"pypi version: {pypi_version}")

        # Look at he tracked github version in repo
        my_version = requests.get(repository.version_file).text
        logger.info(f"repository_version: {my_version}")

        # if pypi version is greater update
        if parse(str(pypi_version)) > parse(str(my_version)):

            logger.info("Newer upstream version found")

            # trigger the git clone
            logger.info(f"Cloning {repository.owner_user}/{repository.repo_name} to /tmp/{repository.repo_name}/")
            clone_dir = os.path.abspath(os.path.join("/tmp/", package.my_repo))
            repo = Repo.clone_from(package.github_url, clone_dir)
            index = repo.index
            origin = repo.remote(name="origin")

            try:

                # Write the new version to the cloned repo
                logger.info(f"Writing version '{pypi_version}' to VERSION file")
                with open(f"/tmp/{repository.repo_name}/VERSION", "w") as VERSION:
                    VERSION.write(str(pypi_version))

                # Add the new VERSION file
                logger.info("Adding modified VERSION file")
                index.add(["VERSION"])

                # Update CHANGELOG
                # logger.info("Updating CHANGELOG")
                # os.system(f"git log --oneline --decorate --color > /tmp/{package.my_repo}/CHANGELOG")

                # Add the new CHANGELOG file
                # logger.info("Adding CHANGELOG to commit")
                # index.add(["CHANGELOG"])

                # Commit the change
                logger.info(f"Writing to commit log: {pypi_version}")
                index.commit(str(pypi_version))

                # Push the update to the repo
                logger.info(f"Pushing updated to {repository.scm_base_url}/{repository.owner_user}/{repository.repo_name}")
                origin.push()

                # Remove the cloned repo
                logger.info(f"rm -rf /tmp/{repository.repo_name}/")
                os.rmdir(f"/tmp/{repository.repo_name}/")

            except Exception:

                # Remove the cloned repo
                logger.info(f"rm -rf /tmp/{repository.repo_name}/")
                os.rmdir(f"/tmp/{repository.repo_name}/")

        else:
            logger.info(f"Container '{repository.repo_name}' matches pypi upstream '{package.pypi_tracked}'")


if __name__ == "__main__":
    main()
