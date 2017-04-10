import os
import time
import json
import logging

import jinja2
import webapp2

from google.appengine.api import taskqueue
from google.appengine.ext import ndb


JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class Game(ndb.Model):
    round = ndb.IntegerProperty(default=0)
    cleared = ndb.BooleanProperty(default=False)
    headlines = ndb.JsonProperty(default={})

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

    @staticmethod
    def startGame():
        game = Game(round=0, cleared=False, headlines={})
        game.put()


class User(ndb.Model):
    name = ndb.StringProperty()
    team = ndb.IntegerProperty()
    headlines = ndb.JsonProperty()

    @staticmethod
    def makeDummies():
        User(name='nitsan', team=1, headlines={
            1: ['nitsans headline 1', 'nitsans second headline'],
            2: ['headline 2', 'headline 2 part twooooo'],
            3: ['headline 3', ''],
            4: ['headline 4', ''],
        }).put()
        User(name='brad', team=1, headlines={
            1: ['brads terrible headline', 'other headline'],
            2: ['headline 2', 'headline 2 part twooooo'],
            3: ['headline 3', ''],
            4: ['headline 4', ''],
        }).put()
        User(name='roman', team=2, headlines={
            1: ['headline 1', ''],
            2: ['headline 2', 'headline 2 part twooooo'],
            3: ['headline 3', ''],
            4: ['headline 4', ''],
        }).put()


class LoginHandler(webapp2.RequestHandler):
    def get(self):
        login_template = JINJA_ENV.get_template('index.html')
        self.response.out.write(login_template.render())


class UserHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('user')
        user = User.query(User.name == username).get()
        private_headlines = user.headlines[str(1)]
        user_template = JINJA_ENV.get_template('game.html')
        self.response.out.write(user_template.render({
            'username': username,
            'private_headlines': private_headlines,
        }))


class ReadStateHandler(webapp2.RequestHandler):
    def post(self):
        username = self.request.body
        user = User.query(User.name == username).get()
        game = Game.query().get()
        public_headlines = []
        for k in game.headlines:
            if game.headlines[k] > 0:
                public_headlines.append(k)
        state = {
            'round': str(game.round+1),
            'private_headlines': user.headlines[str(game.round+1)],
            'public_headlines': public_headlines
        }
        self.response.write(json.dumps(json.dumps(state)))


class IncrementHeadlineHandler(webapp2.RequestHandler):
    def post(self):
        headline = self.request.body
        print headline
        q = taskqueue.Queue('headlines')
        q.add(taskqueue.Task(payload=headline, method='PULL'))

class IncrementRoundHandler(webapp2.RequestHandler):
    def post(self):
        game.nextRound();
        game.put();

class ClearRoundHandler(webapp2.RequestHandler):
    def post(self):
        game.clearRound();
        game.put();

class HeadlinesWorker(webapp2.RequestHandler):
    def get(self):
        q = taskqueue.Queue('headlines')
        while True:
            try:
                tasks = q.lease_tasks(3600, 100)
            except:
                time.sleep(1)
                continue
            if tasks:
                #@ndb.transactional
                def update_counts():
                    game = Game.query().get()
                    for t in tasks:
                        headline = t.payload
                        if headline in game.headlines:
                            game.headlines[headline] += 1
                        else:
                            game.headlines[headline] = 1
                    game.put()
                try:
                    update_counts()
                except Exception as e:
                    logging.exception(e)
                else:
                    q.delete_tasks(tasks)
            time.sleep(1)


app = webapp2.WSGIApplication(
    [
        ('/', LoginHandler),
        ('/user', UserHandler),
        ('/read-state', ReadStateHandler),
        ('/increment-headline', IncrementHeadlineHandler),
        ('/increment-round', IncrementRoundHandler),
        ('/clear-page', ClearRoundHandler),
        ('/_ah/start', HeadlinesWorker),
    ], debug=True)
