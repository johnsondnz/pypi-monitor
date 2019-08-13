[![pipeline status](https://gitlab.com/johnsondnz/pypi-monitor/badges/master/pipeline.svg)](https://gitlab.com/johnsondnz/pypi-monitor/commits/master)

# Pypi-monitor
Monitors configured repositorys for changes in versions.

## Uses
I use this for tracking ansible releases.  On detection this script checks out my container-ansible repository.  Updates the VERSION file to the new ansible release version and commits the change.  A CI/CD on the container-ansible repository then builds the new container and publishes it to dockerhub/

- [container-ansible](https://gitlab.com/johnsondnz/container-ansible)
- [docker-hub](https://hub.docker.com/r/johnsondnz/ansible)

## Database
`app/database.json`

## Options
- tracked: Package name being tracked on pypi
  - example 1: ansible
  - example 2: django
- my_repo: Personal repository name from github/gitlab
- my_version: Raw link to repository VERSION file
- github_url: URL to repository, supports any git based repository

## Example database.json
```
[
	{
		"tracked": "ansible",
		"my_repo": "container-ansible",
		"my_version": "https://gitlab.com/johnsondnz/container-ansible/raw/master/VERSION",
		"github_url": "git@gitlab.com:johnsondnz/container-ansible.git"
	}
]
```

# Build
`docker-compose build`

# Run
`docker-compose up`

# Scheduling
I use a cron task for checking ansible upstream daily.
```
# Check for upstream repo releases every day at midnight
0 0 * * * /usr/local/bin/docker-compose -f ~/pypi-monitor/docker-compose.yml up >> ~/pypi-app/log.log 2>&1
```

# SSH Keys
Ensure the owner of the SSH key has the same UID owner on the host docker machine and within the container.  The container runs with the UID 1000.
