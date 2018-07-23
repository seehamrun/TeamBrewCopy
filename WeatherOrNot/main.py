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



class MainPage(webapp2.RequestHandler):
    def get(self):
        response_html = jinja_env.get_template("templates/main_page.html")


#class AddItem(webapp2.RequestHandler):

class AddClothingHandler(webapp2.RequestHandler):
<<<<<<< HEAD
<<<<<<< HEAD
    def get(self):
        response_html = jinja_env.get_template("Imgur-Upload-master/index.html")
        self.response.headers['Content-Type'] = 'text/html'
        return self.response.write(response_html.render())
=======
>>>>>>> 67ebbd70bf1eb9ff35188413a038decbed6d92c8
>>>>>>> cd0aa75d9d3333282de8ca6c5f8bef2f152c39da
=======
>>>>>>> 26db95ca41e949341af5a46b0f6e6aa5813f2288
    def post(self):
        requestUrl = self.request.get('url')
        logging.info('server saw a request to add %s to list of favorites' % (requestUrl))
        favoriteUrl = AddClothing(url=requestUrl)
        favoriteUrl.put()


class WardrobePage(webapp2.RequestHandler):
    def get(self):
        response_html = jinja_env.get_template("templates/wardrobe_page.html")


app = webapp2.WSGIApplication([
<<<<<<< HEAD
<<<<<<< HEAD
    ('/add_favorite', AddClothingHandler),
=======
<<<<<<< HEAD
=======
>>>>>>> 26db95ca41e949341af5a46b0f6e6aa5813f2288
    ('/', MainPage),
    ('/Wardrobe', WardrobePage),
    ('/AddItem', AddItem),
    ('/Suggestions', Suggestions),
    ('/Outfits', Outfits),
    ('/add_favorite', AddFavoriteHandler),
<<<<<<< HEAD
>>>>>>> 67ebbd70bf1eb9ff35188413a038decbed6d92c8
>>>>>>> cd0aa75d9d3333282de8ca6c5f8bef2f152c39da
=======
>>>>>>> 26db95ca41e949341af5a46b0f6e6aa5813f2288
], debug=True)
