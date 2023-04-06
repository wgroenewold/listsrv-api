#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, pickle, html
import urllib3
from http.cookiejar import MozillaCookieJar

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def login():
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": "WALOGIN=RESET",
    }

    s = requests.session()
    payload = (
        "LOGIN1=&Y="
        + html.escape("w.groenewold@rug.nl")
        + "&p="
        + html.escape("banaan1")
        + "&e=Log+In&L="
        + html.escape("HABROK")
        + "&X="
    )
    s.cookies = (MozillaCookieJar('cookies.txt'))
    r = s.post(
        "https://list.rug.nl/cgi-bin/wa", headers=headers, data=payload, verify=False
    )
    s.cookies.save()
    print('Login headers: \n {}'.format(r.headers))
    s.close()


def command():
    
    s = requests.session()
    s.cookies = (MozillaCookieJar('cookies.txt'))
    s.cookies.revert()

    #print('Restored cookies are: \n {}'.format(s.cookies))

    
    r = s.get(
        "https://list.rug.nl/cgi-bin/wa?LCMD=CHARSET+UTF-8+THANKS&L=HABROK",
        verify=False,
    )
    s.cookies = (MozillaCookieJar('cookies2.txt'))    
    s.cookies.save()
    #s.cookies = (MozillaCookieJar('cookies2.txt'))

    print('request headers: \n {}'.format(r.headers))


login()
command()
command()