import os
import requests


import dataGenerator as dg

token = os.environ.get("PAGE_ACCESS_TOKEN")

def sendTextMessage(sender, text): # to FacebookMessanger
    print("*** sendTextMessage(sender, text) ***")
    if len(text) <= 0:
        return
    url = 'https://graph.facebook.com/v2.6/me/messages'
    headers = {'content-type': 'application/json'}
    params = {"access_token":token}

    data = dg.packageData(sender, text)
    r = requests.post(url, params=params, data=json.dumps(data), headers=headers)
