# coding: UTF-8

#    Sample main.py Tornado file
#    (for Tornado on Heroku)
#
#    Author: Mike Dory | dory.me
#    Created: 11.12.11 | Updated: 06.02.13
#    Contributions by Tedb0t, gregory80
#
# ------------------------------------------

#!/usr/bin/env python
import os.path
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

# import and define tornado-y things
from tornado.options import define
define("port", default=5000, help="run on the given port", type=int)

import json
import requests
import re
import random

import dataGenerator as dg
import logDAO

verify_token = os.environ.get("VERIFY_TOKEN")
token = os.environ.get("PAGE_ACCESS_TOKEN")

# application settings and handle mapping info
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/webhook?", WebHookHandler),
            (r"/csv", CSVHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

# the main page
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        if 'GOOGLEANALYTICSID' in os.environ:
            google_analytics_id = os.environ['GOOGLEANALYTICSID']
        else:
            google_analytics_id = False
        self.render(
            "main.html",
            page_title='Heroku Funtimes',
            page_heading='Hi! This is Heroku!',
            google_analytics_id=google_analytics_id,
        )

# Webhook Handler
class WebHookHandler(tornado.web.RequestHandler):
    def get(self):
        if self.get_argument("hub.verify_token", "") == verify_token:
            self.write(self.get_argument("hub.challenge", ""));
        else:
            self.write('Error, wrong validation token');
    def post(self):
        data = json.loads(self.request.body.decode())
        print ("*** received data ***")
        # logDAO側でも値を取り出しているので非効率だが、勉強用にやっている。
        logDAO.writeLog(date)
        messaging_events = data["entry"][0]["messaging"]
        text = ""
        for event in messaging_events:
            sender = event["sender"]["id"];
            if ("message" in event and "text" in event["message"]):
                text = event["message"]["text"];
                # モード判定
                sendTextMessage(sender, text)

def decideMode(sender, text):
    # PostgreSQLに格納中のステータスを参照する。将来的にはRedisを参照したい。
    mode = None
    return mode

def sendTextMessage(sender, text): # to FacebookMessanger
    print("*** sendTextMessage(sender, text) ***")
    if len(text) <= 0:
        return
    url = 'https://graph.facebook.com/v2.6/me/messages'
    headers = {'content-type': 'application/json'}
    params = {"access_token":token}

    data = dg.packageData(sender, text)
    r = requests.post(url, params=params, data=json.dumps(data), headers=headers)

# res CSV
class CSVHandler(tornado.web.RequestHandler):
    def get(self):
        path = "csv/SW.csv"
        try:
            with open(os.path.abspath(path), 'rb') as f:
                data = f.read()
                self.write(data)
            self.finish
        except IOError:
            raise tornado.web.HTTPError(404, 'Invalid archive')

# RAMMING SPEEEEEEED!
def main():
    print('main started nyan nyan')
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(tornado.options.options.port)

    # start it up
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
