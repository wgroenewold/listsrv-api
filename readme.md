# LISTSRV API

This repo contains the scripts necessary control LISTSRV with a Python-based API

## Installation

- Deploy a VM on an OpenStack cluster with Terraform using `deploy-vm.tf`
- Deploy the software on your just created VM with Ansible using `deploy-software.yml`

## Development

To install the scripts, clone the repo:

```shell
git clone git@github.com:wgroenewold/listsrv-api.git
```

## Todo
- ~~Transparent endpoint for /command to mimic lcmdx~~
- ~~Add commands to hooks~~
- ~~Make requests to listsrv~~
- ~~Sanitizing data and outputs~~
- ~~Add annotations for OpenAPI documentation~~
- Sync command  
    - Get list of users from hb-user-management
    - Get list of users from listrsv-api
    - Diff
    - Create some users with listsrv-api
    - Delete some users with listsrv-api
- ~~Create Docker-compose or Ansible playbook (or both) to make a turnkey-solution.~~
- Add manual SSL support
- Add tests (https://fastapi.tiangolo.com/tutorial/testing/)
- If you make auth with external instead of env you can expose port 443 for other services. Update install_firewalld role then.
    - name: 'Configure /etc/dnsmasq.conf to use nameservers as listed in group_vars for this cluster.'

## Stack overview
- [OpenStack](https://www.openstack.org/) - Cluster instrastructure.
- [Terraform](https://www.terraform.io/) - Orchestration.
- [RockyLinux](https://rockylinux.org/) - OS for VM.
- [Ansible](https://www.ansible.com/) - Provisioning.
- [Docker](https://www.docker.com/) - Containerization.
- [Traefik](https://traefik.io/) - Reverse proxy.
- [Python](https://www.python.org/) - Programming language, aka glue.
- [FastAPI](https://fastapi.tiangolo.com/) - API framework.
- [Listserv](https://www.lsoft.com/) - Ancient email list software.