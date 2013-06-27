import datetime
import json
import time
import urllib
import tornadoredis
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.httpclient

from django.conf import settings
from django.utils.importlib import import_module

session_engine = import_module(settings.SESSION_ENGINE)

from django.contrib.auth.models import User


c = tornadoredis.Client()
c.connect()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'text/plain')
        self.write('Hello. :)')
class MessagesHandler(tornado.websocket.WebSocketHandler):
     def __init__(self, *args, **kwargs):
        super(MessagesHandler, self).__init__(*args, **kwargs)
        self.client = tornadoredis.Client()
        self.client.connect()
        print "CLient"
     
     def open(self):
        session_key = self.get_cookie(settings.SESSION_COOKIE_NAME)
        session = session_engine.SessionStore(session_key)
        try:
            self.user_id = session["_auth_user_id"]
            self.sender_name = User.objects.get(id=self.user_id).username
        except (KeyError, User.DoesNotExist):
            self.close()
            return
        self.channel = 'feed'
        self.client.subscribe(self.channel)
        self.client.listen(self.on_message)


     def handle_request(self, response):
        print "in handle_request"

     def on_message(self, message):
        #....
        print "message received %s" % message
      #  c.publish('feed',message)
        c.publish('feed', json.dumps({
            "timestamp": int(time.time()),
            "sender": self.sender_name,
            "text": message,
        }))
 
        self.write_message(json.dumps({
            "timestamp": int(time.time()),
            "sender": self.sender_name,
            "text": message,
        }))
        print self.sender_name
        http_client = tornado.httpclient.AsyncHTTPClient()
        print http_client
        request = tornado.httpclient.HTTPRequest(
              'http://127.0.0.1/writedata/',
                method="POST",
                body=urllib.urlencode({
                "message": message.encode("utf-8"),
                "sender": self.user_id,
            })
        )
        print request   
        print "url sent"   
        http_client.fetch(request, self.handle_request)     
    
     def show_new_message(self, result):
        print "in show message"
        self.write_message(str(result.body))

     def on_close(self):
        if self.client.subscribed:
            self.client.unsubscribe('feed')
            self.client.disconnect()

class CommentsHandler(tornado.websocket.WebSocketHandler):
     def __init__(self, *args, **kwargs):
        super(CommentsHandler, self).__init__(*args, **kwargs)
        self.client = tornadoredis.Client()
        self.client.connect()
     
     
     def open(self):
        session_key = self.get_cookie(settings.SESSION_COOKIE_NAME)
        session = session_engine.SessionStore(session_key)
        try:
            self.user_id = session["_auth_user_id"]
            self.sender_name = User.objects.get(id=self.user_id).username
        except (KeyError, User.DoesNotExist):
            self.close()
            return
        self.channel = 'comment'
        self.client.subscribe(self.channel)
        self.client.listen(self.on_message)

     def handle_request(self, response):
        print "in handle_request"

     def on_message(self, message):
        #....
        t = json.loads(message)
        print "comment received"
        print (t['comment'])
        print "post"
        print(t['post_id'])
     #  c.publish('feed',message)
        c.publish('comment', json.dumps({
            "timestamp": int(time.time()),
            "sender": self.sender_name,
            "text": t['comment'],
            "post":t['post_id'],
        }))
 
        self.write_message(json.dumps({
            "timestamp": int(time.time()),
            "sender": self.sender_name,
            "text": t['comment'],
            "post":t['post_id'],
        }))
        print self.sender_name
        http_client = tornado.httpclient.AsyncHTTPClient()
        print http_client
        request = tornado.httpclient.HTTPRequest(
              'http://127.0.0.1/writecomment/',
                method="POST",
                body=urllib.urlencode({
                "message": t['comment'],
                "post_id":t['post_id'],
                "sender": self.user_id,
            })
        )
        print request   
        print "url sent"   
        http_client.fetch(request, self.handle_request)     
    
     def show_new_message(self, result):
        print "in show message"
        self.write_message(str(result.body))

     def on_close(self):
        if self.client.subscribed:
            self.client.unsubscribe('comment')
            self.client.disconnect()

application = tornado.web.Application([
    (r"/", MainHandler),
    (r'/track/', MessagesHandler),
    (r'/comment/',CommentsHandler),

    
])
