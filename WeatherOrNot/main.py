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
            url=requestUrl, length=requestLength, materials=requestMaterial, laundry=False)
        stored_clothing.put()
        response_html = jinja_env.get_template('templates/upload-images/index.html')
        logging.info('server saw a request to add %s to list of favorites' % (requestUrl))


class SuggestionsHandler(webapp2.RequestHandler):
    def get(self):
        response_html = jinja_env.get_template("templates/suggestions_page/suggestions.html")
        self.response.write(response_html.render())


class WardrobePage(webapp2.RequestHandler):
    def get(self):
        response_html = jinja_env.get_template("templates/wardrobe_page.html")
        values = {
            "topsWardrobe":WardrobeSave.query(WardrobeSave.type=="shirt", WardrobeSave.laundry==False).fetch(),
            "bottomWardrobe":WardrobeSave.query(WardrobeSave.type=="pants", WardrobeSave.laundry==False).fetch(),
            "skirtWardrobe":WardrobeSave.query(WardrobeSave.type=="skirt", WardrobeSave.laundry==False).fetch(),
            "dressWardrobe":WardrobeSave.query(WardrobeSave.type=="dress", WardrobeSave.laundry==False).fetch(),
        }
        self.response.write(response_html.render(values))

class FavoritesHandler(webapp2.RequestHandler):
    def get(self):
        response_html = jinja_env.get_template("templates/addfavs_page.html")
        values = {
            "topsWardrobe":WardrobeSave.query(WardrobeSave.type=="shirt", WardrobeSave.laundry==False).fetch(),
            "bottomWardrobe":WardrobeSave.query(WardrobeSave.type=="pants", WardrobeSave.laundry==False).fetch(),
            "skirtWardrobe":WardrobeSave.query(WardrobeSave.type=="skirt", WardrobeSave.laundry==False).fetch(),
            "dressWardrobe":WardrobeSave.query(WardrobeSave.type=="dress", WardrobeSave.laundry==False).fetch(),
        }
        self.response.write(response_html.render(values))


class GetWeather(webapp2.RequestHandler):
    def get(self):
        temp = self.request.get("temp")
        maxTemp=self.request.get("maxTemp")
        minTemp=self.request.get("minTemp")
        logging.info("It went through")

        response_html = jinja_env.get_template("templates/suggestions_page/suggestions.html")

        length_cloth=WardrobeSave.length=="length"
        material_cloth = WardrobeSave.materials=="cotton"
        if (temp<35):
            values={
                "topsWardrobe":WardrobeSave.query(WardrobeSave.type=="shirt", WardrobeSave.laundry==False).fetch(),
                "bottomWardrobe":WardrobeSave.query(WardrobeSave.type=="pants", WardrobeSave.laundry==False, WardrobeSave.materials=="wool", WardrobeSave.materials=="denim", WardrobeSave.materials=="cotton", WardrobeSave.length=="long").fetch(),
                "coatWardrobe":WardrobeSave.query(WardrobeSave.type=="coat", WardrobeSave.laundry==False).fetch(),
                "jacketWardrobe":WardrobeSave.query(WadrobeSave.type=="jacket", WardrobeSave.laundry==False).fetch()
            }
        elif(temp>35 and temp<=50):
            values={
                "topsWardrobe":WardrobeSave.query(WardrobeSave.type=="shirt", WardrobeSave.laundry==False).fetch(),
                "bottomWardrobe":WardrobeSave.query(WardrobeSave.type=="pants", WardrobeSave.laundry==False, WardrobeSave.length=="long").fetch(),
                "sweaterWardrobe":WardrobeSave.query(WardrobeSave.type=="sweater", WardrobeSave.laundry==False).fetch(),
                "jacketWardrobe":WardrobeSave.query(WadrobeSave.type=="jacket", WardrobeSave.laundry==False).fetch()
            }
        elif(temp>50 and temp<=60):
            values={
                "topsWardrobe":WardrobeSave.query(WardrobeSave.type=="shirt", WardrobeSave.laundry==False).fetch(),
                "bottomWardrobe":WardrobeSave.query(WardrobeSave.type=="pants", WardrobeSave.laundry==False, WardrobeSave.length=="long").fetch(),
                "sweaterWardrobe":WardrobeSave.query(WardrobeSave.type=="sweater", WardrobeSave.laundry==False).fetch()
            }
        elif(temp>60 and temp<=70):
            values={
                "topsWardrobe":WardrobeSave.query(WardrobeSave.type=="shirt", WardrobeSave.laundry==False, WardrobeSave.length=="short").fetch(),
                "bottomWardrobe":WardrobeSave.query(WardrobeSave.type=="pants", WardrobeSave.laundry==False, WardrobeSave.length=="long").fetch(),
            }
        else:
            values={
                "topsWardrobe":WardrobeSave.query(WardrobeSave.type=="shirt", WardrobeSave.laundry==False, WardrobeSave.length=="short").fetch(),
                "bottomWardrobe":WardrobeSave.query(WardrobeSave.type=="pants", WardrobeSave.laundry==False, WardrobeSave.length=="short").fetch(),
                "skirtWardrobe":WardrobeSave.query(WardrobeSave.type=="skirt", WardrobeSave.laundry==False).fetch(),
                "dressWardrobe":WardrobeSave.query(WadrobeSave.type=="dress", WardrobeSave.laundry==False).fetch()
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
    ('/add_favorite', FavoritesHandler),
    ('/get_weather', GetWeather),
    ("/testing", TesterHandler)
], debug=True)
