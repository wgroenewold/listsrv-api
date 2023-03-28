from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

base_url = 'https://list.rug.nl/cgi-bin/wa'
list = 'HABROK'

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
    return login

@app.get("/test")
def test():
    return True

@app.get("/user/{email}")
def get_user(email: str):
    return email

@app.post("/user")
def create_user(user: CreateUser):   
    return user

@app.delete("/user")
def delete_user(user: DeleteUser):
    return user    

@app.get("/list")
def get_users():
    req = 'foo'
    return req

@app.get("/stats")
def get_stats():
    req = 'bar'
    return 'bar'

@app.post("/command")
def send_command(command: SendCommand):
    return True