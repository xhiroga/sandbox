# coding: UTF-8

import re
import random
import seDAO
import send

"""
modeが"init"か"wiki"の時に呼ばれる。
dataを作成し、sendMessageに渡す。

"""

def initHandler(data):
    return data

def wikiHandler(text,time,sender):
    ### 初期値
    dg = send.DataGenerator()
    data = dg.setBasicMessage(sender, text + "...よく分かりませんでした。ごめんなさい。")

    if text == "menu":
        data = dg.setMenu(sender)
    elif text == "sender":
        data = dg.setBasicMessage(sender, sender)
    elif re.compile("竹書房|takeshobo|ポプテピピック|pptp|PPTP").match(text):
        data = setPPTP(sender)
    else : #neo4jに問い合わせ
        note = seDAO.returnNote(text)
        data = dg.setBasicMessage(sender, note)
    send.sendMessage(data)

### B.
def setPPTP(sender):
    print("Start PPTP...")
    dg = send.DataGenerator()
    kibun = random.randint(1,4)
    if kibun == 1:  imgurl ="http://image.itmedia.co.jp/nl/articles/1609/02/kontake_160902takesyobo03.jpg"
    elif kibun == 2:  imgurl ="http://cdn2.natalie.mu/media/comic/1512/1205/extra/news_header_poptepipik-new001.jpg"
    elif kibun ==3: imgurl ="http://pbs.twimg.com/media/CVoPQ-1VAAA0btq.jpg"
    else: imgurl ="http://pbs.twimg.com/media/CVn6FG_UEAENuo3.jpg"
    return dg.setImage(sender,imgurl)
