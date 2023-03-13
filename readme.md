# LISTSRV API

This repo contains the scripts necessary control LISTSRV with a Python-based API

## Installation

To install the scripts, clone the repo:

```shell
git clone git@github.com:wgroenewold/listsrv-api.git
```

## Notes
- Binary for lcmdx is a patched version, found in bin/src. Original version can be found [here](https://ftp.lsoft.com/CONTRIB/lcmdx.c), you can compile it yourself with

```shell
sudo gcc -O lcmdx.c -o lcmdx
```