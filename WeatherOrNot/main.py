import webapp2
import logging
import jinja2
import os
import json

from google.appengine.ext import ndb
from google.appengine.api import urlfetch


class WardrobeSave(ndb.Model):
    url = ndb.StringProperty()


jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class AddClothingHandler(webapp2.RequestHandler):
    def get(self):
        response_html = jinja_env.get_template("Imgur-Upload-master/index.html")
        self.response.headers['Content-Type'] = 'text/html'
        return self.response.write(response_html.render())
    def post(self):
        requestUrl = self.request.get('url')
        logging.info('server saw a request to add %s to list of favorites' % (requestUrl))
        favoriteUrl = AddClothing(url=requestUrl)
        favoriteUrl.put()



app = webapp2.WSGIApplication([
    ('/add_favorite', AddClothingHandler),
], debug=True)
