import os
import time

import jinja2
import webapp2

from google.appengine.api import taskqueue
from google.appengine.ext import ndb


JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class Game(ndb.Model):
    round = ndb.IntegerProperty()
    cleared = ndb.BooleanProperty()
    headlines = ndb.JsonProperty()

    def nextRound(self):
        self.round += 1
        self.cleared = False
        for k in self.headlines:
            if self.headlines[k] > 0:
                self.headlines[k] *= -1

    def clearRound(self):
        self.cleared = True


    def getInfo(self):
        return {
            'round': self.round,
            'likes': self.headlines,
        }


class User(ndb.Model):
    team = ndb.IntegerProperty()
    headlines = ndb.JsonProperty()


class LoginHandler(webapp2.RequestHandler):
    def get(self):
        login_template = JINJA_ENV.get_template('index.html')
        self.response.out.write(login_template.render())


class UserHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(self.request.get('user'))


app = webapp2.WSGIApplication(
    [
        ('/', LoginHandler),
        ('/user', UserHandler),
    ], debug=True)
