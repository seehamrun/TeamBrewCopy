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
    def get(self):
        response_html = jinja_env.get_template("templates/upload-images/index.html")
        self.response.headers['Content-Type'] = 'text/html'
        return self.response.write(response_html.render())
        self.response.headers['Content-Type'] = 'text/html'
        response_html = jinja_env.get_template('templates/calc.html')
        length = self.request.get('length')
        type=self.request.get('type')
        material = self.request.get('materials')
        if type == 'dress':

        elif type=='skirt':

        elif type=='shirt':

        elif type=='pants':

        if length=='short':

        elif length=='long':

        elif length=='three_quarters':

        if material == 'Cotton':

        elif material=='Nylon':

        elif material=='Spandex':

        elif material=='Wool':

        elif material == 'Polyester':
            
        #result = int(number1) + int(number2)
        #self.response.write(response_html % (result, number1, number2))
        values = {
            "tempResult": result,
            "tempNumber1": number1,
            "tempNumber2": number2,
        }
        self.response.write(response_html.render(values))
    def post(self):
        requestUrl = self.request.get('url')
        logging.info('server saw a request to add %s to list of favorites' % (requestUrl))
        favoriteUrl = WardrobeSave(url=requestUrl)
        favoriteUrl.put()



class WardrobePage(webapp2.RequestHandler):
    def get(self):
        response_html = jinja_env.get_template("templates/wardrobe_page.html")
        values = {
            "allWardrobe": WardrobeSave.query().fetch()
        }
        self.response.write(response_html.render(values))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/wardrobe', WardrobePage),
    ('/add_item', AddClothingHandler)
], debug=True)
