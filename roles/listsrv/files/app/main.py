from typing import Union, Annotated, Optional
from fastapi import Depends, FastAPI, Path, Query, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from dotenv import dotenv_values
from requests.auth import HTTPBasicAuth
import requests, re, html, pickle


import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

description = """
Listsrv API contains the scripts necessary to control LISTSRV with a Python-based API
"""

app = FastAPI(
    title="Listsrv API",
    description=description,
    version="0.0.1",
    contact={
        "name": "Listsrv API",
        "url": "https://github.com/wgroenewold/listsrv-api",
        "email": "w.groenewold@rug.nl",
    },
    license_info={
        "name": "GNU GPLv3",
        "url": "https://www.gnu.org/licenses/gpl-3.0.html",
    },
)

security = HTTPBasic()

config = dotenv_values(".env")

if config['VERIFY_SSL'] == "False":
    config['VERIFY_SSL'] = False

class CreateUser(BaseModel):
    email: str
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    
class DeleteUser(BaseModel):
    email: str    

class SendCommand(BaseModel):
    command: str

@app.post("/login", status_code=200)
def login(credentials: Annotated[HTTPBasicCredentials, Depends(security)], mailinglist: str):
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'WALOGIN=RESET'
    }

    s = requests.session()   
    payload = 'LOGIN1=&Y=' + html.escape(credentials.username) +'&p=' + html.escape(credentials.password) + '&e=Log+In&L=' + html.escape(mailinglist) + '&X='
    r = s.post(config['BASE_URL'], headers=headers, data=payload, verify=config['VERIFY_SSL'])

    with open('somefile', 'wb') as f:
        pickle.dump(s.cookies, f)

    if s.cookies:
        return 'Login successful'
    else:
        raise HTTPException(status_code=401, detail="Login failed")
    
@app.post("/command", status_code=200)
def send_command(command: SendCommand, mailinglist: str):    
    s = requests.session()
    
    with open('somefile', 'rb') as f:
        s.cookies.update(pickle.load(f))

    r = s.get(config['BASE_URL'] + '?LCMD=CHARSET+UTF-8+' + command.command + '&L=' + mailinglist, verify=config['VERIFY_SSL'])     
    with open('somefile', 'wb') as f:
        pickle.dump(s.cookies, f)

    res = r.text.replace('\n','')
    match = re.search('<pre>(.*?)</pre>', res)

    if match:
        substring = match.group(1)
        return substring
    else:
        raise HTTPException(status_code=400, detail="Request failed")
    
@app.get("/test", response_class=PlainTextResponse, status_code=200)
def test():
    command = 'thanks'
    r = requests.post(config['FQDN'] + '/command', json={'command': command})     

    if "You're welcome" in r.text:
        return r.text.replace('<br>', '')
    else:
        raise HTTPException(status_code=400, detail="Request failed")

#testen
@app.get("/user/{email}", status_code=200)
def get_user(email: str, mailinglist: str):
    command = 'QUERY+'+mailinglist+'+FOR+'+email
    r = requests.post(config['FQDN'] + '/command', json={'command': command})     

    if 'Request failed' in r.text:
        raise HTTPException(status_code=400, detail="Request failed")        
    elif 'There is no subscription' in r.text:
        raise HTTPException(status_code=400, detail="User not found")        
    else:
        email = re.search('&lt;(.*?)&gt;', r.text)
        name = re.search('(.*?)&lt;', r.text)          
        if email and name:
            email = email.group(1)
            name = name.group(1)
    
            resp = {
                "name": name[30:],
                "email": email.lower()
            }

            return resp

@app.post("/user", status_code=200)
def create_user(user: CreateUser, mailinglist: str):
    # user first and lastname shouldnt be mandatory    
    command = 'QUIET+ADD+'+mailinglist+'+'+user.email+'+'+user.firstname+'+'+user.lastname
    r = requests.post(config['FQDN'] + '/command', json={'command': command})     

    if 'Request failed' in r.text:
         raise HTTPException(status_code=400, detail="Request failed")    
    elif 'is already subscribed to the' in r.text:
         raise HTTPException(status_code=409, detail="User is already subscribed")
    elif 'has been added' in r.text:
        # user first and lastname shouldnt be mandatory
        resp = {
            "name": user.firstname+' '+user.lastname,
            "email": user.email.lower()
        }
        return resp
    else: 
        raise HTTPException(status_code=400, detail="Unknown error")    
    
@app.delete("/user", status_code=200)
def delete_user(user: DeleteUser, mailinglist: str):
    command = 'QUIET+DELETE+'+mailinglist+'+'+user.email
    r = requests.post(config['FQDN'] + '/command', json={'command': command})     

    if 'Request failed' in r.text:
        raise HTTPException(status_code=400, detail="Request failed")    
    elif 'is not subscribed' in r.text:
        raise HTTPException(status_code=400, detail="User not found")    
    elif 'has been removed' in r.text:
        return user.email

@app.get("/list", status_code=200)
def get_users(mailinglist: str):
    command = 'REVIEW+'+mailinglist+'+MSG+NOH'
    r = requests.post(config['FQDN'] + '/command', json={'command': command})     

    if 'Request failed' in r.text:
        raise HTTPException(status_code=400, detail="Request failed")    
    else:
        res = r.text[1:].split('<br>')
        del res[-5:]

        data = []

        for val in res:
            val = val.split(" ", 1)

            data.append({
                'name': val[1],
                'email': val[0]
            })

        return data

@app.get("/stats", status_code=200)
def get_stats(mailinglist: str):
    command = 'REVIEW+'+mailinglist+'+MSG+NOH+SH'
    r = requests.post(config['FQDN'] + '/command', json={'command': command})     

    if 'Request failed' in r.text:
        raise HTTPException(status_code=400, detail="Request failed")    
    else:
        resp = r.text.replace('<br>','').split("* ")[1].split("      ")
        
        return int(resp[1])

@app.get("/ldap/group/", status_code=200)
def get_ldap_group(credentials: Annotated[HTTPBasicCredentials, Depends(security)], ldap_group: str):
    

    command = html.escape("/Group/"+group+"?read-attr='member'")
    r = requests.get(config['LDAP_URL'] + command, auth=(config['LDAP_USERNAME'], config['LDAP_PASSWORD']))

    #we need to polish response a bit

    return r.text

@app.get("/ldap/user", status_code=200)
def get_ldap_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)], ldap_group: str):
    
    command = html.escape("/User/"+config['LDAP_GROUP']+"?read-attr=Internet Email Address")
    r = requests.get(config['LDAP_URL'] + command, auth=(config['LDAP_USERNAME'], config['LDAP_PASSWORD']))

    #we need to polish response a bit

    return r.text

# @app.get("/titanic", status_code=200)
# def sync(credentials: Annotated[HTTPBasicCredentials, Depends(security)], ldap_credentials: Annotated[HTTPBasicCredentials, Depends(security)], mailinglist: str, ldap_group: str):
#     # - dump alle adressen naar var vanaf LDAP    
# 	# - delete alle adressen op mailinglijst
# 	# - voeg alle adressen toe van variabele
# 	# - query habrok-extra via mailinglijst
# 	# - voeg die adressen toe aan mailinglijst1