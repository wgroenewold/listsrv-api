# LISTSRV API

This repo contains the scripts necessary control LISTSRV with a Python-based API

## Installation

Dockerfile is included. It assumes some sort of reverse proxy for SSL.

## Development

To install the scripts, clone the repo:

```shell
git clone git@github.com:wgroenewold/listsrv-api.git
```

## Notes
commands are:
POST /login data = username / pw
See PoC in main.py

GET /test
command = 'thanks'
result = You're welcome

GET /user data = email
command 'QUERY+HABROK+FOR+anniko@rtl4.nl'

POST /user data = email, firstname, lastname
command = 'QUIET+ADD+HABROK+anniko@rtl4.nl+Anniko+Zanten

DELETE /user data = email
command 'QUIET+DELETE+HABROK+anniko@rtl4.nl'

GET /list
command 'REVIEW+HABROK+MSG'

GET /stats
command 'REVIEW+HABROK+MSG+NOH+SH'

## Todo
- ~~Transparent endpoint for /command to mimic lcmdx~~
- ~~Add commands to hooks~~
- ~~Make requests to listsrv~~
- Sanitizing data and outputs
- Sync command
    - Get list of users from hb-user-management
    - Get list of users from listrsv-api
    - Diff
    - Create some users with listsrv-api
    - Delete some users with listsrv-api
- Create Docker-compose or Ansible playbook (or both) to make a turnkey-solution, with SSL and everything
- Add tests (https://fastapi.tiangolo.com/tutorial/testing/)


