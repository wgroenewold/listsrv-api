from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import requests, re, html, tempfile

app = FastAPI()

fqdn = 'https://listsrv-api.rug.nl'

username = 'w.groenewold@rug.nl'
password = 'banaan'

base_url = 'https://list.rug.nl/cgi-bin/wa'
verify_ssl = False
mailinglist = 'HABROK'

class Login(BaseModel):
    username: str
    password: str    

class CreateUser(BaseModel):
    email: str
    firstname: str | None = None
    lastname: str | None = None
    
class DeleteUser(BaseModel):
    email: str    

class SendCommand(BaseModel):
    command: str

@app.post("/login")
def login(login: Login):
    headers = {
     'Content-Type': 'application/x-www-form-urlencoded',
     'Cookie': 'WALOGIN=RESET'
    }
    
    payload = 'LOGIN1=&Y=' + html.escape(login.username) +'&p=' + html.escape(login.password) + '&e=Log+In&L=' + html.escape(mailinglist) + '&X='
    r = requests.post(base_url, headers=headers, data=payload, verify=verify_ssl)

    login_cookie = r.cookies.get_dict()
    login_cookie = login_cookie['WALOGIN']

    with tempfile.TemporaryFile() as store:
        store.write(login_cookie)

    return login_cookie

@app.post("/command")
def send_command(command: SendCommand):
    with tempfile.TemporaryFile() as store:
        store.seek(0)
        login_cookie = store.read()    

    headers = {
        'Cookie': 'WALOGIN=' + login_cookie
    }

    r = requests.get(base_url + '?LCMD=CHARSET+UTF-8+' + command.command + '&L=' + mailinglist, headers=headers, verify=verify_ssl)     

    res = r.text.replace('\n','')
    res = res.replace('<br>','')
    match = re.search('<pre>(.*?)</pre>', res)

    if match:
        substring = match.group(1)
        return substring
    else:
        return False
    
@app.get("/test")
def test():
    command = 'thanks'
    r = requests.post(fqdn + '/command', data={'command': command})     

    return r.content

@app.get("/user/{email}")
def get_user(email: str):
    command = 'QUERY+'+mailinglist+'+FOR+'+email
    r = requests.post(fqdn + '/command', data={'command': command})     

    return r.content
    
@app.post("/user")
def create_user(user: CreateUser):    
    command = 'QUIET+ADD+'+mailinglist+'+'+user.email+'+'+user.firstname+'+'+user.lastname
    r = requests.post(fqdn + '/command', data={'command': command})     

    return r.content

@app.delete("/user")
def delete_user(user: DeleteUser):
    command = 'QUIET+DELETE+'+mailinglist+'+'+user.email
    r = requests.post(fqdn + '/command', data={'command': command})     

    return r.content

@app.get("/list")
def get_users():
    command = 'REVIEW+'+mailinglist+'+MSG'
    r = requests.post(fqdn + '/command', data={'command': command})     

    return r.content

@app.get("/stats")
def get_stats():
    command = 'REVIEW+'+mailinglist+'+MSG+NOH+SH'
    r = requests.post(fqdn + '/command', data={'command': command})     

    return r.content