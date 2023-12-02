#Master Database file for Users

import os

from deta import Deta
from dotenv import load_dotenv

import uuid

load_dotenv(".env")
DETA_KEY = os.getenv("DETA_KEY")

deta = Deta(DETA_KEY)

db = deta.Base("Users")

def generate_unique_user_id():
    return str(uuid.uuid4())

def create_id(username):
    #user=db.get(username)
    user_id = generate_unique_user_id()
    #return db.put({"key":username,"user_id": user_id})
    return db.update({"user_id": user_id}, username)

def insert_user(username, name, password, email, profile):
    user_id = generate_unique_user_id()  # Generate a unique user ID
    return db.put({"key": username, "user_id": user_id, "name": name, "password": password, "email": email, "profile": profile})

def fetch_all_users():
    res=db.fetch()
    return res.items

def get_user_id(username):
    user = db.get(username)
    return user["user_id"] if user else None

def get_user_fullname(username):
    user = db.get(username)
    return user["name"] if user else None

def get_user(username):
    return db.get(username)

def get_user_by_email(email):
    res = db.fetch({"email": email})
    return res.items[0] if res.count > 0 else None

def update_user_password(username, new_password):
    return db.update({"password": new_password}, username)

#insert_user ("pparker", "Peter Parker" , "abc123" )

#print(get_user("nnarra"))

def update_all_users_with_id():
    users = fetch_all_users()
    for user in users:
        if 'user_id' not in user:
            create_id(user["key"])
        
#update_all_users_with_id()

#print(get_user_id("nnarra"))

#print(get_user_fullname("nnarra"))
        