import webapp2
import logging
import jinja2
import os
from google.appengine.ext import ndb


class WardrobeSave(ndb.Model):
    url = ndb.StringProperty()


jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


<<<<<<< HEAD
class MainPage(webapp2.RequestHandler):
    def get(self):
        response_html = jinja_env.get_template("templates/main_page.html")


class AddItem(webapp2.RequestHandler):
=======
class AddClothingHandler(webapp2.RequestHandler):
>>>>>>> 67ebbd70bf1eb9ff35188413a038decbed6d92c8
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
    ('/', MainPage),
    ('/Wardrobe', WardrobePage),
    ('/AddItem', AddItem),
    ('/Suggestions', Suggestions),
    ('/Outfits', Outfits),
=======
    ('/add_favorite', AddFavoriteHandler),
>>>>>>> 67ebbd70bf1eb9ff35188413a038decbed6d92c8
], debug=True)
