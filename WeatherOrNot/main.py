import webapp2
import logging
import jinja2
import os
import json

from google.appengine.ext import ndb
from google.appengine.api import urlfetch

class WardrobeSave(ndb.Model):
    url = ndb.StringProperty()
    type=ndb.StringProperty()
    materials=ndb.StringProperty()
    length=ndb.StringProperty()
    laundry=ndb.BooleanProperty()


jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(webapp2.RequestHandler):
    def get(self):
        response_html = jinja_env.get_template("templates/main_page.html")

        temp = self.request.get("temp")
        weather(temp)


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
    def post(self):
        requestUrl = self.request.get('url')
        requestType=self.request.get('type')
        requestLength=self.request.get('length')
        requestMaterial=self.request.get('materials')
        stored_clothing = WardrobeSave(type=requestType,
            url=requestUrl, length=requestLength, materials=requestMaterial)
        stored_clothing.put()
        response_html = jinja_env.get_template('templates/upload-images/index.html')
        logging.info('server saw a request to add %s to list of favorites' % (requestUrl))


class SuggestionsHandler(webapp2.RequestHandler):
    def get(self):
        response_html = jinja_env.get_template("templates/suggestions_page/suggestions.html")
        weather_response_html = jinja_env.get_template("templates/weather-test.html")
        temp = self.request.get("temp")
        weather = self.request.get("condition")
        logging.info("The weather is: " + weather)
        length_cloth=WardrobeSave.length=="length"
        if (weather=="sunny"):
            length_cloth=WardrobeSave.length=="short"
        values={
            "topsWardrobe":WardrobeSave.query(WardrobeSave.type=="shirt", length_cloth).fetch(),
            "bottomWardrobe":WardrobeSave.query(WardrobeSave.type=="pants", length_cloth).fetch(),
            "skirtWardrobe":WardrobeSave.query(WardrobeSave.type=="skirt", length_cloth).fetch(),
            "dressWardrobe":WardrobeSave.query(WardrobeSave.type=="dress", length_cloth).fetch(),
        }
        self.response.write(weather_response_html.render())
        self.response.write(response_html.render(values))


class WardrobePage(webapp2.RequestHandler):
    def get(self):
        response_html = jinja_env.get_template("templates/wardrobe_page.html")
        values = {
            "topsWardrobe":WardrobeSave.query(WardrobeSave.type=="shirt").fetch(),
            "bottomWardrobe":WardrobeSave.query(WardrobeSave.type=="pants").fetch(),
            "skirtWardrobe":WardrobeSave.query(WardrobeSave.type=="skirt").fetch(),
            "dressWardrobe":WardrobeSave.query(WardrobeSave.type=="dress").fetch(),
        }
        self.response.write(response_html.render(values))


class TesterHandler(webapp2.RequestHandler):
    def get(self):

        response_html = jinja_env.get_template("templates/weather-test.html")
        self.response.write(response_html.render())
        temp = self.request.get("temp")
        weather(temp)


def weather(temp):
    logging.info("This is temp")
    logging.info(temp)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/wardrobe', WardrobePage),
    ('/add_item', AddClothingHandler),
    ('/suggestion', SuggestionsHandler),
    ("/testing", TesterHandler)
], debug=True)
