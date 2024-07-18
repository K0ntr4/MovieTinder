import hashlib
import json

def getdbconfig():
    file = open('dbconfig.json')
    data = json.load(file)
    file.close()

    return data

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
  