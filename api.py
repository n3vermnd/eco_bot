import json
import uuid
import requests
import requests.sessions
import urllib3
import random
from config import USERNAME, PASSWORD
from config import ST_LOGIN, FT_LOGIN 
from config import ST_SUB, FT_SUB
from config import ST_ADDCLIENT, FT_ADDCLIENT
import utils
import database

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

session = requests.Session()


async def login(tarif_type):
    login_payload = {
        'username': USERNAME,
        'password': PASSWORD
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    loginUrl = ST_LOGIN if tarif_type == 'st' else FT_LOGIN
    response = session.post(loginUrl, headers=headers, data=login_payload, verify=False)
    print("Login Status:", response.status_code)
    print("Login Response:", response.text)
    return response
    
    
async def addClient(tarif_type, sub_period, tg_id):
    await login(tarif_type)
    client_id = str(uuid.uuid4())
    client_inapp_id = random.randint(100000000, 999999999)
    expiryTime = utils.utime(sub_period)
    client_data = {
        "id": client_id,
        "alterId": 0,
        "email": f"{client_inapp_id}414",
        "limitIp": 1,
        "totalGB": 0,
        "expiryTime": expiryTime,
        "enable": True,
        "flow": "xtls-rprx-vision",
        "subId": f"{client_inapp_id}414"
    }
    print("!!!!!!!!!!!!!!!!!!!!!",utils.utime(sub_period))
    payload = {
        "id": 1,
        "settings": json.dumps({"clients": [client_data]})
    }
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    addClientURL = ST_ADDCLIENT if tarif_type == "st" else FT_ADDCLIENT
    session.post(addClientURL, headers=headers, data=json.dumps(payload), verify=False)
    subUrl = ST_SUB if tarif_type == 'st' else FT_SUB
    subUrl = subUrl+f"/{client_inapp_id}414"
    await database.addClient(subUrl, expiryTime, tg_id)
    
    return str(subUrl)