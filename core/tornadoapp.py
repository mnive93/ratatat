import datetime
import json
import time
import urllib
import tornadoredis
import tornado.web
import django.utils.importlib
import tornado
from tornado.options import options
import tornado.web
import tornado.ioloop
import sockjs.tornado
from django.conf import settings
import django.contrib.auth
from utils import *
c = tornadoredis.Client()
c.connect()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'text/plain')
        self.write('Hello. :)')
class MessagesHandler(sockjs.tornado.SockJSConnection):
     def __init__(self, *args, **kwargs):
        super(MessagesHandler, self).__init__(*args, **kwargs)
        self.client = tornadoredis.Client()
        self.client.connect()
        print "CLient"
     def get_django_session(self,info):
       if not hasattr(self, '_session'):
         engine = django.utils.importlib.import_module(django.conf.settings.SESSION_ENGINE)
         session_key = str(info.get_cookie(django.conf.settings.SESSION_COOKIE_NAME)).split('=')[1]
         self._session = engine.SessionStore(session_key)
         print self._session
         return self._session
     def get_current_user(self,info):
       print info
    # get_user needs a django request object, but only looks at the session
       class Dummy(object): pass
       django_request = Dummy()

       django_request.session = self.get_django_session(info=info)
       
       user = django.contrib.auth.get_user(django_request)
       print user
       if user.is_authenticated():
        return user
     def on_open(self, info):
        user = self.get_current_user(info=info)
        self.sender_name=user.username
        self.user_id=user.id
        print self.sender_name
        self.channel = 'feed'
        self.client.subscribe(self.channel)
        self.client.listen(self.on_message)
       

     def handle_request(self, response):
        print "in handle_request"

     def on_message(self, message):
        #....
        print "message received %s" % message

      #  c.publish('feed',message)
        '''
        c.publish('feed', json.dumps({
            "timestamp": int(time.time()),
            "sender": self.user,
            "text": message,
        }))
'''
        print self.sender_name
        print self.user_id
 
        self.send({
            "timestamp": int(time.time()),
            "sender": self.sender_name,
            "text": message,
        })
        decision = train(message)
        http_client = tornado.httpclient.AsyncHTTPClient()
        print http_client
        request = tornado.httpclient.HTTPRequest(
              'http://127.0.0.1/writedata/',
                method="POST",
                body=urllib.urlencode({
                "message": message.encode("utf-8"),
                "sender": self.user_id,
                "decision":decision.encode("utf-8"),
            })
        )
        print request   
        print "url sent"   
        http_client.fetch(request, self.handle_request)     
    
     def show_new_message(self, result):
        self.write_message(str(result.body))

     def on_close(self):
        if self.client.subscribed:
            self.client.unsubscribe('feed')
            self.client.disconnect()

class CommentsHandler(sockjs.tornado.SockJSConnection):
     def __init__(self, *args, **kwargs):
        super(CommentsHandler, self).__init__(*args, **kwargs)
        self.client = tornadoredis.Client()
        self.client.connect()

     def get_django_session(self,info):
       if not hasattr(self, '_session'):
         engine = django.utils.importlib.import_module(django.conf.settings.SESSION_ENGINE)
         session_key = str(info.get_cookie(django.conf.settings.SESSION_COOKIE_NAME)).split('=')[1]
         self._session = engine.SessionStore(session_key)
         print self._session
         return self._session
     def get_current_user(self,info):
       print info
    # get_user needs a django request object, but only looks at the session
       class Dummy(object): pass
       django_request = Dummy()

       django_request.session = self.get_django_session(info=info)
       
       user = django.contrib.auth.get_user(django_request)
       print user
       if user.is_authenticated():
        return user
     def on_open(self, info):
        user = self.get_current_user(info=info)
        self.sender_name=user.username
        self.user_id=user.id
        print self.sender_name
        self.channel = 'feed'
        self.client.subscribe(self.channel)
        self.client.listen(self.on_message)
     def handle_request(self, response):
        pass

     def on_message(self, message):
        t = json.loads(message)
        print "comment received"
        print (t['comment'])
        print "post"
        print(t['post_id'])
        c.publish('comment', json.dumps({
            "timestamp": int(time.time()),
            "sender": self.user_id,
            "text": t['comment'],
            "post":t['post_id'],
        }))
 
        self.send(json.dumps({
            "timestamp": int(time.time()),
            "sender": self.user_id,
            "text": t['comment'],
            "post":t['post_id'],
        }))
        #print self.sender_name
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
class OpinionsHandler(sockjs.tornado.SockJSConnection):
     def __init__(self, *args, **kwargs):
        super(OpinionsHandler, self).__init__(*args, **kwargs)
        self.client = tornadoredis.Client()
        self.client.connect()

     def get_django_session(self,info):
       if not hasattr(self, '_session'):
         engine = django.utils.importlib.import_module(django.conf.settings.SESSION_ENGINE)
         session_key = str(info.get_cookie(django.conf.settings.SESSION_COOKIE_NAME)).split('=')[1]
         self._session = engine.SessionStore(session_key)
         print self._session
         return self._session
     def get_current_user(self,info):
       print info
    # get_user needs a django request object, but only looks at the session
       class Dummy(object): pass
       django_request = Dummy()

       django_request.session = self.get_django_session(info=info)
       
       user = django.contrib.auth.get_user(django_request)
       print user
       if user.is_authenticated():
        return user
     def on_open(self, info):
        user = self.get_current_user(info=info)
        self.sender_name=user.username
        self.user_id=user.id
        print self.sender_name
        self.channel = 'feed'
        self.client.subscribe(self.channel)
        self.client.listen(self.on_message)
     def handle_request(self, response):
            pass
     def on_message(self, message):
        t = json.loads(message)
        http_client = tornado.httpclient.AsyncHTTPClient()
        print http_client
        request = tornado.httpclient.HTTPRequest(
              'http://127.0.0.1/opinionsdata/',
                method="POST",
                body=urllib.urlencode({
                "post_id":t['post_id'],
                "value":t['value'],
                "sender": self.user_id,
            })
        )
        http_client.fetch(request, self.handle_request)     
    
     def show_new_message(self, result):
        self.write_message(str(result.body))

     def on_close(self):
        if self.client.subscribed:
            self.client.disconnect()


Post = sockjs.tornado.SockJSRouter(MessagesHandler, '/track')
Comments=sockjs.tornado.SockJSRouter(CommentsHandler,'/comment')
Opinions= sockjs.tornado.SockJSRouter(OpinionsHandler,'/opinion')
application = tornado.web.Application([
    (r"/", MainHandler)]+ Post.urls + Comments.urls + Opinions.urls
    )
 
    
