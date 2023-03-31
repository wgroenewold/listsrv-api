from typing import Union, Annotated 
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel
from dotenv import dotenv_values
import requests, re, html

app = FastAPI()

config = dotenv_values(".env")

if config['VERIFY_SSL'] == "False":
    config['VERIFY_SSL'] = False

class CreateUser(BaseModel):
    email: str
    firstname: str | None = None
    lastname: str | None = None
    
class DeleteUser(BaseModel):
    email: str    

class SendCommand(BaseModel):
    command: str

@app.post("/login")
def login():    
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'WALOGIN=RESET'
    }
    
    payload = 'LOGIN1=&Y=' + html.escape(config['USERNAME']) +'&p=' + html.escape(config['PASSWORD']) + '&e=Log+In&L=' + html.escape(config['MAILINGLIST']) + '&X='
    r = requests.post(config['BASE_URL'], headers=headers, data=payload, verify=config['VERIFY_SSL'])

    login_cookie = r.cookies.get_dict()
    login_cookie = login_cookie['WALOGIN']

    f = open("cookie.txt", "w")
    f.write(login_cookie)
    f.close()

    return True
    
@app.post("/command")
def send_command(command: SendCommand):
    f = open("cookie.txt", "r")
    login_cookie = f.read()

    headers = {
        'Cookie': 'WALOGIN=' + login_cookie
    }

    r = requests.get(config['BASE_URL'] + '?LCMD=CHARSET+UTF-8+' + command.command + '&L=' + config['MAILINGLIST'], headers=headers, verify=config['VERIFY_SSL'])     

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
    r = requests.post(config['FQDN'] + '/command', data={'command': command})     

    return r.content

@app.get("/user/{email}")
def get_user(email: str):
    command = 'QUERY+'+config['MAILINGLIST']+'+FOR+'+email
    r = requests.post(config['FQDN'] + '/command', data={'command': command})     

    return r.content
    
@app.post("/user")
def create_user(user: CreateUser):    
    command = 'QUIET+ADD+'+config['MAILINGLIST']+'+'+user.email+'+'+user.firstname+'+'+user.lastname
    r = requests.post(config['FQDN'] + '/command', data={'command': command})     

    return r.content

@app.delete("/user")
def delete_user(user: DeleteUser):
    command = 'QUIET+DELETE+'+config['MAILINGLIST']+'+'+user.email
    r = requests.post(config['FQDN'] + '/command', data={'command': command})     

    return r.content

@app.get("/list")
def get_users():
    command = 'REVIEW+'+config['MAILINGLIST']+'+MSG'
    r = requests.post(config['FQDN'] + '/command', data={'command': command})     

    return r.content

@app.get("/stats")
def get_stats():
    command = 'REVIEW+'+config['MAILINGLIST']+'+MSG+NOH+SH'
    r = requests.post(config['FQDN'] + '/command', data={'command': command})     

    return r.content