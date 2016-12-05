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

import send
import quiz
import dataGenerator as dg
import logDAO

verify_token = os.environ.get("VERIFY_TOKEN")

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

        messaging_events = data["entry"][0]["messaging"]
        text = ""
        time = ""
        for event in messaging_events:
            time = event["timestamp"]
            sender = event["sender"]["id"]
            if ("message" in event and "text" in event["message"]):
                text = event["message"]["text"]
            logDAO.writeLog(sender, text, time)
            # モード判定
            mode = logDAO.decideMode
            if mode == "quiz":
                quiz.quizHandler(data)
            else :
                send.sendTextMessage(sender, text)

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
