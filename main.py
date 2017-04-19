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
    headlines = ndb.StringProperty(repeated=True)
    likes = ndb.JsonProperty(default={})

    def nextRound(self):
        self.round += 1
        self.cleared = False
        for k in self.likes:
            if self.likes[k] > 0:
                self.likes[k] *= -1

    def clearRound(self):
        self.cleared = True
        self.headlines = []
        self.likes = {}

    def getInfo(self):
        return {
            'headlines': self.headlines,
            'likes': self.likes
        }

class User(ndb.Model):
    name = ndb.StringProperty()
    team = ndb.IntegerProperty()
    headlines = ndb.JsonProperty()

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


class AdminHandler(webapp2.RequestHandler):
    def get(self):
        admin_template = JINJA_ENV.get_template('admin.html')
        self.response.out.write(admin_template.render())


class ReadStateHandler(webapp2.RequestHandler):
    def post(self):
        username = self.request.body
        user = User.query(User.name == username).get()
        game = Game.query().get()
        print game.likes
        state = {
            'cleared': game.cleared,
            'round': str(game.round+1),
            'private_headlines': user.headlines[str(game.round+1)],
            'public_headlines': game.headlines
        }
        self.response.write(json.dumps(state))

class UnityReadHandler(webapp2.RequestHandler):
    def get(self):
        game = Game.query().get()
        state = {
            'public_headlines': game.headlines,
            'likes': game.likes
        }
        self.response.write(json.dumps(state))

class ResetHandler(webapp2.RequestHandler):
    def post(self):
        for i in range(1,9):
            User(name='axon'+i, team=1, headlines={
                1: ['', ''],
                2: ['1gogan_truth1', '1gogan_lie1'],
                3: ['', ''],
                4: ['', '']}).put()

        for i in range(9,17):
            User(name='axon'+i, team=1, headlines={
                1: ['', ''],
                2: ['1gogan_truth2', '1gogan_lie2'],
                3: ['', ''],
                4: ['', '']}).put()

        for i in range(17,25):
            User(name='axon'+i, team=1, headlines={
                1: ['', ''],
                2: ['', ''],
                3: ['2gogan_truth1', '2gogan_lie1'],
                4: ['', '']}).put()

        for i in range(25,33):
            User(name='axon'+i, team=1, headlines={
                1: ['', ''],
                2: ['', ''],
                3: ['2gogan_truth2', '2gogan_lie2'],
                4: ['', '']}).put()

        for i in range(33,41):
            User(name='axon'+i, team=1, headlines={
                1: ['', ''],
                2: ['', ''],
                3: ['', ''],
                4: ['3gogan_truth1', '3gogan_lie1']}).put()

        for i in range(41,49):
            User(name='axon'+i, team=1, headlines={
                1: ['', ''],
                2: ['', ''],
                3: ['', ''],
                4: ['3gogan_truth2', '3gogan_lie2']}).put()

        for i in range(49,57):
            User(name='axon'+i, team=1, headlines={
                1: ['', ''],
                2: ['1roosa_truth1', '1roosa_lie1'],
                3: ['', ''],
                4: ['', '']}).put()

        for i in range(57,65):
            User(name='axon'+i, team=1, headlines={
                1: ['', ''],
                2: ['1roosa_truth2', '1roosa_lie2'],
                3: ['', ''],
                4: ['', '']}).put()

        for i in range(65,73):
            User(name='axon'+i, team=1, headlines={
                1: ['', ''],
                2: ['', ''],
                3: ['2roosa_truth1', '2roosa_lie1'],
                4: ['', '']}).put()

        for i in range(73,81):
            User(name='axon'+i, team=1, headlines={
                1: ['', ''],
                2: ['', ''],
                3: ['2roosa_truth2', '2roosa_lie2'],
                4: ['', '']}).put()

        for i in range(81,89):
            User(name='axon'+i, team=1, headlines={
                1: ['', ''],
                2: ['', ''],
                3: ['', ''],
                4: ['3roosa_truth1', '3roosa_lie1']}).put()

        for i in range(89,97):
            User(name='axon'+i, team=1, headlines={
                1: ['', ''],
                2: ['', ''],
                3: ['', ''],
                4: ['3roosa_truth2', '3roosa_lie2']}).put()

        Game(round=0, cleared=False, likes={}, headlines=[]).put()

class IncrementHeadlineHandler(webapp2.RequestHandler):
    def post(self):
        headline = self.request.body
        q = taskqueue.Queue('headlines')
        q.add(taskqueue.Task(payload=headline, method='PULL'))

class IncrementRoundHandler(webapp2.RequestHandler):
    def post(self):
        q = taskqueue.Queue('headlines')
        q.add(taskqueue.Task(payload='increment-round', method='PULL'))

class ClearRoundHandler(webapp2.RequestHandler):
    def post(self):
        q = taskqueue.Queue('headlines')
        q.add(taskqueue.Task(payload='clear-round', method='PULL'))

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
                        if headline == 'increment-round':
                            game.nextRound()
                        elif headline == 'clear-round':
                            game.clearRound()
                        elif headline in game.headlines:
                            game.likes[headline] += 1
                        else:
                            game.likes[headline] = 1
                            game.headlines.append(headline)
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
        ('/admin', AdminHandler),
        ('/read-state', ReadStateHandler),
        ('/unity-read', UnityReadHandler),
        ('/reset', ResetHandler),
        ('/increment-headline', IncrementHeadlineHandler),
        ('/increment-round', IncrementRoundHandler),
        ('/clear-page', ClearRoundHandler),
        ('/_ah/start', HeadlinesWorker),
    ], debug=True)
