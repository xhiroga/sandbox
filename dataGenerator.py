# coding: UTF-8

import re
import random
import seDAO

"""
すること
A. 分岐ちゃん。sender, textごとに適切なB.を呼び出し、dataを受け取る
B. ロジックちゃん。適切な文言,URLをgenerateする。
C. json職人ちゃん。

"""

### A.
def packageData(sender, text):
    print ("packageData.py is working")
    ### 初期値
    data = setBasicMessage(sender, text + "...よく分かりませんでした。ごめんなさい。")

    if re.compile("竹書房|takeshobo|ポプテピピック|pptp|PPTP").match(text):
        data = setPPTP(sender)
    elif text == "dev":
        data = devMenu(sender)
    elif text == "sender":
        data = setBasicMessage(sender, sender)
    else :
        note = seDAO.returnNote(text)
        data = setBasicMessage(sender, note)
    return data

### B.
def setPPTP(sender):
    print("Start PPTP...")
    kibun = random.randint(1,4)
    if kibun == 1:  imgurl ="http://image.itmedia.co.jp/nl/articles/1609/02/kontake_160902takesyobo03.jpg"
    elif kibun == 2:  imgurl ="http://cdn2.natalie.mu/media/comic/1512/1205/extra/news_header_poptepipik-new001.jpg"
    elif kibun ==3: imgurl ="http://pbs.twimg.com/media/CVoPQ-1VAAA0btq.jpg"
    else: url ="http://pbs.twimg.com/media/CVn6FG_UEAENuo3.jpg"
    return setImageUrl(sender,imgurl)

### C. dataを詰め込む
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

def setImageUrl(sender, imgurl):
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
