import webapp2
import logging
import jinja2
import os
import json
import time
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import urlfetch

class ZipSave(ndb.Model):
    user=ndb.StringProperty()
    zip=ndb.IntegerProperty()

class CalendarSave(ndb.Model):
    user=ndb.StringProperty()
    date=ndb.StringProperty()
    urltop=ndb.StringProperty()
    urlbottom=ndb.StringProperty()
    # urlskirt=ndb.StringProperty()
    # urldress=ndb.StringProperty()
    # urljacket=ndb.StringProperty()
    # urlcoat=ndb.StringProperty()

class WardrobeSave(ndb.Model):
    url = ndb.StringProperty()
    type=ndb.StringProperty()
    materials=ndb.StringProperty()
    length=ndb.StringProperty()
    laundry=ndb.BooleanProperty()
    user = ndb.StringProperty()

class FavoriteSave(ndb.Model):
    topUrl = ndb.StringProperty()
    bottomUrl = ndb.StringProperty()

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        logging.info('current user is: %s' % (user.nickname()))
        response_html = jinja_env.get_template("templates/main_page.html")

        # temp = self.request.get("temp")
        # weather(temp)

        data = {
          'user_nickname': user.nickname(),
          'logoutUrl': users.create_logout_url('/')
        }
        return self.response.write(response_html.render(data))

    def post(self):
        logging.info(self.request.POST)
        zipCode = self.request.get('zip')
        user=users.get_current_user()
        stored_zip = ZipSave(zip=zipCode, user=user.nickname())
        stored_zip.put()
        #response_html = jinja_env.get_template("templates/addfavs_page.html")
        time.sleep(1)
        #logging.info('server saw a request to add %s to list of favorites' % (requestUrl))
        self.redirect('/')

class AddClothingHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        logging.info('current user is: %s' % (user.nickname()))
        self.response.headers['Content-Type'] = 'text/html'
        response_html = jinja_env.get_template("templates/upload-images/index.html")

        return self.response.write(response_html.render())
        length = self.request.get('length')
        type=self.request.get('type')
        material = self.request.get('materials')

    def post(self):
        user = users.get_current_user()
        requestUrl = self.request.get('url')
        requestType=self.request.get('type')
        requestLength=self.request.get('length')
        requestMaterial=self.request.get('materials')
        logging.info('current user is: %s' % (user.nickname()))
        requestUser = user.nickname()
        stored_clothing = WardrobeSave(type=requestType,
            url=requestUrl, length=requestLength, materials=requestMaterial, laundry=False, user=requestUser)
        stored_clothing.put()
        response_html = jinja_env.get_template('templates/upload-images/index.html')
        logging.info('server saw a request to add %s to list of favorites' % (requestUrl))

class WardrobePage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        logging.info('current user is: %s' % (user.nickname()))

        response_html = jinja_env.get_template("templates/wardrobe_page.html")
        values = {
            'user_nickname': user.nickname(),
            'logoutUrl': users.create_logout_url('/'),
            "topsWardrobe":WardrobeSave.query(WardrobeSave.type=="shirt", WardrobeSave.laundry==False, WardrobeSave.user==user.nickname()).fetch(),
            "bottomWardrobe":WardrobeSave.query(WardrobeSave.type=="pants", WardrobeSave.laundry==False, WardrobeSave.user==user.nickname()).fetch(),
            "skirtWardrobe":WardrobeSave.query(WardrobeSave.type=="skirt", WardrobeSave.laundry==False, WardrobeSave.user==user.nickname()).fetch(),
            "dressWardrobe":WardrobeSave.query(WardrobeSave.type=="dress", WardrobeSave.laundry==False, WardrobeSave.user==user.nickname()).fetch(),
            "laundry":WardrobeSave.query(WardrobeSave.laundry==True, WardrobeSave.user==user.nickname()).fetch(),
        }
        self.response.write(response_html.render(values))
    def post(self):
        button = None
        itemKeys = []
        logging.info(self.request.POST)
        for keys in self.request.POST.keys():
            if keys == "toWardrobe" or keys=="deleteClothing" or keys=="toLaundry":
                button = keys
            else:
                itemKeys.append(keys)

        for itemKey in itemKeys:
            DBKey = ndb.Key(urlsafe=itemKey)
            TheItem = DBKey.get()
            if button == "toWardrobe":
                TheItem.laundry = False
                TheItem.put()
            elif button=="deleteClothing":
                DBKey.delete()
            else:
                TheItem.laundry = True
                TheItem.put()
        time.sleep(1)
        self.redirect("/wardrobe")

class SuggestionsHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        logging.info('current user is: %s' %(user.nickname()))
        response_html=jinja_env.get_template("templates/main_page.html")
        response_html = jinja_env.get_template("templates/suggestions_page/suggestions.html")
        self.response.write(response_html.render())

class GetWeather(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        logging.info('current user is: %s' % (user.nickname()))
        # response_html = jinja_env.get_template("templates/main_page.html")

        temp = self.request.get("temp")
        maxTemp=self.request.get("maxTemp")
        minTemp=self.request.get("minTemp")
        logging.info("It went through")

        response_html = jinja_env.get_template("templates/suggestions_page/suggestions.html")
        if (temp<35):
            values={
                'user_nickname': user.nickname(),
                'logoutUrl': users.create_logout_url('/'),
                "topsWardrobe":WardrobeSave.query(WardrobeSave.type=="shirt", WardrobeSave.laundry==False, WardrobeSave.user==user.nickname()).fetch(),
                "bottomWardrobe":WardrobeSave.query(WardrobeSave.type=="pants", WardrobeSave.laundry==False, WardrobeSave.materials=="wool", WardrobeSave.materials=="denim", WardrobeSave.materials=="cotton", WardrobeSave.length=="long", WardrobeSave.user==user.nickname().nickname).fetch(),
                "coatWardrobe":WardrobeSave.query(WardrobeSave.type=="coat", WardrobeSave.laundry==False, WardrobeSave.user==user.nickname()).fetch(),
                "jacketWardrobe":WardrobeSave.query(WardrobeSave.type=="jacket", WardrobeSave.laundry==False, WardrobeSave.user==user.nickname()).fetch()
            }
        elif(temp<=50):
            values={
                'user_nickname': user.nickname(),
                'logoutUrl': users.create_logout_url('/'),
                "topsWardrobe":WardrobeSave.query(WardrobeSave.type=="shirt", WardrobeSave.laundry==False, WardrobeSave.user==user.nickname()).fetch(),
                "bottomWardrobe":WardrobeSave.query(WardrobeSave.type=="pants", WardrobeSave.laundry==False, WardrobeSave.length=="long", WardrobeSave.user==user.nickname()).fetch(),
                "sweaterWardrobe":WardrobeSave.query(WardrobeSave.type=="sweater", WardrobeSave.laundry==False, WardrobeSave.user==user.nickname()).fetch(),
                "jacketWardrobe":WardrobeSave.query(WardrobeSave.type=="jacket", WardrobeSave.laundry==False, WardrobeSave.user==user.nickname()).fetch()
            }
        elif(temp<=60):
            values={
                'user_nickname': user.nickname(),
                'logoutUrl': users.create_logout_url('/'),
                "topsWardrobe":WardrobeSave.query(WardrobeSave.type=="shirt", WardrobeSave.laundry==False, WardrobeSave.user==user.nickname()).fetch(),
                "bottomWardrobe":WardrobeSave.query(WardrobeSave.type=="pants", WardrobeSave.laundry==False, WardrobeSave.length=="long", WardrobeSave.user==user.nickname()).fetch(),
                "sweaterWardrobe":WardrobeSave.query(WardrobeSave.type=="sweater", WardrobeSave.laundry==False, WardrobeSave.user==user.nickname()).fetch()
            }
        elif(temp<=70):
            values={
                'user_nickname': user.nickname(),
                'logoutUrl': users.create_logout_url('/'),
                "topsWardrobe":WardrobeSave.query(WardrobeSave.type=="shirt", WardrobeSave.laundry==False, WardrobeSave.length=="short", WardrobeSave.user==user.nickname()).fetch(),
                "bottomWardrobe":WardrobeSave.query(WardrobeSave.type=="pants", WardrobeSave.laundry==False, WardrobeSave.length=="long", WardrobeSave.user==user.nickname()).fetch()
            }
        else:
            values={
                'user_nickname': user.nickname(),
                'logoutUrl': users.create_logout_url('/'),
                "topsWardrobe":WardrobeSave.query(WardrobeSave.type=="shirt", WardrobeSave.laundry==False, WardrobeSave.length=="short", WardrobeSave.user==user.nickname()).fetch(),
                "bottomWardrobe":WardrobeSave.query(WardrobeSave.type=="pants", WardrobeSave.laundry==False, WardrobeSave.length=="short", WardrobeSave.user==user.nickname()).fetch(),
                "skirtWardrobe":WardrobeSave.query(WardrobeSave.type=="skirt", WardrobeSave.laundry==False, WardrobeSave.user==user.nickname()).fetch(),
                "dressWardrobe":WardrobeSave.query(WardrobeSave.type=="dress", WardrobeSave.laundry==False, WardrobeSave.user==user.nickname()).fetch()
            }

        return self.response.write(response_html.render(values))

class FavoritesHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        logging.info('current user is: %s' % (user.nickname()))
        response_html = jinja_env.get_template("templates/main_page.html")

        response_html = jinja_env.get_template("templates/addfavs_page.html")
        values = {
            'user_nickname': user.nickname(),
            'logoutUrl': users.create_logout_url('/'),
            "topsWardrobe":WardrobeSave.query(WardrobeSave.type=="shirt", WardrobeSave.laundry==False, WardrobeSave.user==user.nickname()).fetch(),
            "pantsWardrobe":WardrobeSave.query(WardrobeSave.type=="pants", WardrobeSave.laundry==False, WardrobeSave.user==user.nickname()).fetch(),
            "skirtWardrobe":WardrobeSave.query(WardrobeSave.type=="skirt", WardrobeSave.laundry==False, WardrobeSave.user==user.nickname()).fetch(),
            "sweaterWardrobe":WardrobeSave.query(WardrobeSave.type=="sweater", WardrobeSave.laundry==False, WardrobeSave.user==user.nickname()).fetch(),
            "coatWardrobe":WardrobeSave.query(WardrobeSave.type=="coat", WardrobeSave.laundry==False, WardrobeSave.user==user.nickname()).fetch(),
            "jacketWardrobe":WardrobeSave.query(WardrobeSave.type=="jacket", WardrobeSave.laundry==False, WardrobeSave.user==user.nickname()).fetch(),
            "dressWardrobe":WardrobeSave.query(WardrobeSave.type=="dress", WardrobeSave.laundry==False, WardrobeSave.user==user.nickname()).fetch()
        }
        self.response.write(response_html.render(values))

    def post(self):
        logging.info(self.request.POST)
        top = self.request.get('topForm')
        bottom= self.request.get('bottomForm')
        skirt = self.request.get('skirtForm')
        dress = self.request.get('dressForm')
        coat = self.request.get('coatForm')
        jacket = self.request.get('jacketForm')
        sweater = self.request.get('sweaterForm')

        if(top!="" and bottom!=""):
            stored_clothing = FavoriteSave(topUrl=top, bottomUrl=bottom)
            stored_clothing1 = CalendarSave(urltop=top, urlbottom=bottom)
            stored_clothing1.put()
            stored_clothing.put()
        elif(top!="" and skirt!=""):
            stored_clothing = FavoriteSave(topUrl=top, bottomUrl=skirt)
            stored_clothing1 = CalendarSave(urltop=top, urlbottom=skirt)
            stored_clothing1.put()
            stored_clothing.put()
        elif(sweater!="" and bottom!=""):
            stored_clothing = FavoriteSave(topUrl=sweater, bottomUrl=bottom)
            stored_clothing1 = CalendarSave(urltop=sweater, urlbottom=bottom)
            stored_clothing1.put()
            stored_clothing.put()
        elif(sweater!="" and skirt!=""):
            stored_clothing = FavoriteSave(topUrl=sweater, bottomUrl=skirt)
            stored_clothing1 = CalendarSave(urltop=sweater, urlbottom=skirt)
            stored_clothing1.put()
            stored_clothing.put()
        elif(coat!="" and bottom!=""):
            stored_clothing = FavoriteSave(topUrl=coat, bottomUrl=bottom)
            stored_clothing1 = CalendarSave(urltop=coat, urlbottom=bottom)
            stored_clothing1.put()
            stored_clothing.put()
        elif(jacket!="" and bottom!=""):
            stored_clothing = FavoriteSave(topUrl=jacket, bottomUrl=bottom)
            stored_clothing1 = CalendarSave(urltop=jacket, urlbottom=bottom)
            stored_clothing1.put()
            stored_clothing.put()
        else:
            response = """
            <html>
                <head>
                    <link rel="stylesheet" href="/static/style.css"></link>
                </head>
                <body class = "img" background="https://emojipedia-us.s3.amazonaws.com/socialmedia/apple/129/crying-face_1f622.png">
                    <h1 id="head">This outfit combination does not work</h1>
                </body>
            </html>"""
            return self.response.write(response)

        time.sleep(1)
        #logging.info('server saw a request to add %s to list of favorites' % (requestUrl))
        self.redirect('/add_favorite')

class ListFavoritesHandler(webapp2.RequestHandler):
    def get(self):
        response_html = jinja_env.get_template("templates/listfavs_page.html")
        values = {
            "favorites":FavoriteSave.query().fetch(),
        }
        self.response.write(response_html.render(values))

class CalendarHandler(webapp2.RequestHandler):
    def get(self):
        response_html = jinja_env.get_template("templates/calendar.html")
        values = {
            "favorites":CalendarSave.query().fetch(),
        }
        self.response.write(response_html.render(values))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/wardrobe', WardrobePage),
    ('/add_item', AddClothingHandler),
    ('/suggestion', SuggestionsHandler),
    ('/add_favorite', FavoritesHandler),
    ('/get_weather', GetWeather),
    ('/calendar', CalendarHandler),
    ('/list_favorite', ListFavoritesHandler)
], debug=True)
