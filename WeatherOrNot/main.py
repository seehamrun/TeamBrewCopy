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

class FavoriteSave(ndb.Model):
    topUrl = ndb.StringProperty()
    bottomUrl = ndb.StringProperty()


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

        self.response.headers['Content-Type'] = 'text/html'
        return self.response.write(response_html.render())
        self.response.headers['Content-Type'] = 'text/html'
        top = self.request.get('tops')
        bottom= self.request.get('bottoms')

    def post(self):
        top = self.request.get('tops')
        bottom= self.request.get('bottoms')
        stored_clothing = FavoriteSave(topUrl=top, bottomUrl=bottom)
        stored_clothing.put()
        response_html = jinja_env.get_template("templates/addfavs_page.html")
        logging.info('server saw a request to add %s to list of favorites' % (requestUrl))


class ListFavoritesHandler(webapp2.RequestHandler):
    def get(self):
        response_html = jinja_env.get_template("templates/listfavs_page.html")
        values = {
            "favorites":FavoriteSave.query().fetch(),
        }
        self.response.write(response_html.render(values))



class GetWeather(webapp2.RequestHandler):
    def get(self):
        temp = self.request.get("temp")
        weather = self.request.get("condition")
        maxTemp=self.request.get("maxTemp")
        minTemp=self.request.get("minTemp")
        logging.info("It went through")

        response_html = jinja_env.get_template("templates/suggestions_page/suggestions.html")

        length_cloth=WardrobeSave.length=="length"
        material_cloth = WardrobeSave.materials=="cotton"
        if (weather=="sunny"):
            length_cloth=WardrobeSave.length=="short"
        if (temp>50):
            material_cloth=WardrobeSave.length=="wool"
        values={
            "topsWardrobe":WardrobeSave.query(WardrobeSave.type=="shirt", WardrobeSave.laundry==False, length_cloth, material_cloth).fetch(),
            "bottomWardrobe":WardrobeSave.query(WardrobeSave.type=="pants", WardrobeSave.laundry==False, length_cloth, material_cloth).fetch(),
            "skirtWardrobe":WardrobeSave.query(WardrobeSave.type=="skirt", WardrobeSave.laundry==False, length_cloth, material_cloth).fetch(),
            "dressWardrobe":WardrobeSave.query(WardrobeSave.type=="dress", WardrobeSave.laundry==False, length_cloth, material_cloth).fetch(),
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
    ("/testing", TesterHandler),
    ('/list_favorite', ListFavoritesHandler),
], debug=True)
