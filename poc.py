#! /usr/local/bin/python

import requests, re, html

username = 'w.groenewold@rug.nl'
password = 'supersecret'
mailinglist = 'Paardenmeisjes' 
base_url = 'https://list.rug.nl/cgi-bin/wa'
verify_ssl = False
email = 'anniko@rtl4.nl'
firstname = 'Anniko'
lastname = 'van Santen'
command = 'QUIET+ADD+' + mailinglist + '+' + html.escape(email) + '+' + html.escape(firstname) + '+' + html.escape(lastname)

payload = 'LOGIN1=&Y=' + html.escape(username) +'&p=' + html.escape(password) + '&e=Log+In&L=' + html.escape(mailinglist) + '&X='
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': 'WALOGIN=RESET'
}
r = requests.post(base_url, headers=headers, data=payload, verify=verify_ssl)

login_cookie = r.cookies.get_dict()
login_cookie = login_cookie['WALOGIN']

headers = {
  'Cookie': 'WALOGIN=' + login_cookie
}
r = requests.get(base_url + '?LCMD=CHARSET+UTF-8+' + command + '&L=' + mailinglist, headers=headers, verify=verify_ssl)

res = r.text.replace('\n','')
res = res.replace('<br>','')
match = re.search('<pre>(.*?)</pre>', res)

if match:
    substring = match.group(1)
    print(html.unescape(substring))