import webapp2
import logging
import jinja2
import os

from google.appengine.ext import ndb

class Item(ndb.Model):
    id = ndb.StringProperty()
    name = ndb.StringProperty()


jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(webapp2.RequestHandler):
    def get(self):
        response_html = jinja_env.get_template("templates/main-page.html")


class AddItem(webapp2.RequestHandler):
    def post(self):
        itemId = self.request.get('id')
        logging.info('server saw a request to add %s to list of favorites' % (itemId))
        newItem = Item(id=itemId)
        itemId.put

        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(response_html.render())


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/Wardrobe', Wardrobe),
    ('/AddItem', AddItem),
    ('/Suggestions', Suggestions),
    ('/Outfits', Outfits),
], debug=True)
