# from typing import Union

# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

import smtplib

server = smtplib.SMTP('localhost')
server.set_debuglevel(1)
server.sendmail("From: wgroenewold@gmail.com", "To: wgroenewold@gmail.com", "Hoera, dit werkt")
server.quit();