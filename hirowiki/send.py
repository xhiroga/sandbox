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
    url = 'https://graph.facebook.com/v2.6/me/messages'
    headers = {'content-type': 'application/json'}
    params = {"access_token":token}

    r = requests.post(url, params=params, data=json.dumps(data), headers=headers)

### packaging data into json
class DataGenerator():
    def setBasicMessage(self,sender, text):
        data = {
            "recipient": {
                "id":sender
            },
            "message":  {
              "text":text
            }
        }
        return data

    def setImage(self,sender, imgurl):
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

    def setMenu(self):
        return data
