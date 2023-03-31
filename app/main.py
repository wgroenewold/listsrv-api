from typing import Union, Annotated 
from fastapi import FastAPI, Path, Query
from fastapi.responses import PlainTextResponse
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
    
@app.get("/test", response_class=PlainTextResponse)
def test():
    command = 'thanks'
    r = requests.post(config['FQDN'] + '/command', json={'command': command})     

    return r.text

@app.get("/user/{email}")
def get_user(email: str):
    command = 'QUERY+'+config['MAILINGLIST']+'+FOR+'+email
    r = requests.post(config['FQDN'] + '/command', json={'command': command})     

    email = re.search('&lt;(.*?)&gt;', r.text)
    name = re.search('(.*?)&lt;', r.text)
    
    if email and name:
        email = email.group(1)
        name = name.group(1)
        
        resp = {
            "name": name[25:],
            "email": email.lower()
        }

        return resp
    else:
        return False
    
@app.post("/user")
def create_user(user: CreateUser):    
    command = 'QUIET+ADD+'+config['MAILINGLIST']+'+'+user.email+'+'+user.firstname+'+'+user.lastname
    r = requests.post(config['FQDN'] + '/command', json={'command': command})     

    if r.text == False:
        #error
        resp =  r.text        
    elif 'is already subscribed to the' in r.text:
        #already subscribed
        resp = True    
    else: 
        resp = {
            "name": user.firstname+' '+user.lastname,
            "email": user.email.lower()
        }       

    return resp

@app.delete("/user")
def delete_user(user: DeleteUser):
    command = 'QUIET+DELETE+'+config['MAILINGLIST']+'+'+user.email
    r = requests.post(config['FQDN'] + '/command', json={'command': command})     

    return r.text

@app.get("/list")
def get_users():
    command = 'REVIEW+'+config['MAILINGLIST']+'+MSG'
    r = requests.post(config['FQDN'] + '/command', json={'command': command})     

    return r.text

@app.get("/stats")
def get_stats():
    command = 'REVIEW+'+config['MAILINGLIST']+'+MSG+NOH+SH'
    r = requests.post(config['FQDN'] + '/command', json={'command': command})     

    return r.text