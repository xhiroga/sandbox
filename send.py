import json
import os
import requests


"""
すること
要素を受け取り、jsonに詰め込んで送出する。
text, image, option等の要素ごとのgeneratorと、dataをsendするものに分けられる。
"""

token = os.environ.get("PAGE_ACCESS_TOKEN")

# send message
def sendMessage(data): # to FacebookMessanger
    if len(text) <= 0:
        return
    url = 'https://graph.facebook.com/v2.6/me/messages'
    headers = {'content-type': 'application/json'}
    params = {"access_token":token}

    r = requests.post(url, params=params, data=json.dumps(data), headers=headers)

### packaging data into json
class DataGenerator():
    def setBasicMessage(sender, reply):
        data = {
            "recipient": {
                "id":sender
            },
            "message":  {
              "text":reply
            }
        }
        return data

    def setImage(sender, imgurl):
        data = {
            "recipient":{
                "id":sender
            },
            "message":{
                "attachment":{
                    "type":"image",
                        "payload":{
                            "url":imgurl
                            }
                        }
                    }
                }
        return data

    def setMenu():
        return data
