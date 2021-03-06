from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
try:
    from urllib.parse import urljoin
except ImportError:
     from urlparse import urljoin    
try:
	from urllib.request import urlopen
except ImportError:
	from urllib2 import urlopen

from googleplaces import GooglePlaces, types, lang

import geocoder
import json
import datetime
import string


WATERLOO_COORDINATES = {"lat": 43.4719, "lng": -80.5230}
GG_API_KEY = "AIzaSyCRIy9x98hVqHF0SWu-K-6AXxTCe-uJ4Dw"
gp = GooglePlaces(GG_API_KEY)

db = SQLAlchemy()

class User(db.Model):
	__tablename__ = 'users'
	uid = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String(100))
	lastname = db.Column(db.String(100))
	email = db.Column(db.String(120), unique=True)
	pwdhash = db.Column(db.String(100))
	recipes = db.relationship("Recipe")

	def __init__(self, firstname, lastname, email, password):
		self.firstname = string.capwords(firstname)
		self.lastname = string.capwords(lastname)
		self.email = email.lower()
		self.set_password(password)
	 
	def set_password(self, password):
		self.pwdhash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)

	def getFullName(self):
		return self.firstname + " " + self.lastname


#The db.Table defined here is the bridging table to create a many-to-many relationship here.
ingredientsPerRecipe = db.Table('ingredientsPerRecipe',
	db.Column('recipeid', db.Integer, db.ForeignKey('recipes.recipeid'), primary_key=True),
	db.Column('ingredientid', db.Integer, db.ForeignKey('ingredients.ingredientid'), primary_key=True)
	)

class Recipe(db.Model):
	__tablename__ = 'recipes'
	recipeid = db.Column(db.Integer, primary_key=True)
	authorid = db.Column(db.Integer, db.ForeignKey('users.uid'))
	recipedate = db.Column(db.DateTime)
	recipetitle = db.Column(db.String(100))
	recipedesc = db.Column(db.Text)
	ingredients = db.relationship('Ingredient', secondary=ingredientsPerRecipe, lazy='subquery', 
		backref=db.backref('ingredients', lazy=True))
	comments = db.relationship('Comment', order_by="desc(Comment.commentdate)")

	# No comments in the constructor as a recipe is initialized without comments
	def __init__(self, recipetitle, recipedesc, ingredients, email):
		author = User.query.filter_by(email = email).first()
		self.authorid = author.uid
		self.recipedate = datetime.datetime.now()
		self.recipetitle = string.capwords(recipetitle)
		self.recipedesc = recipedesc
		for i in ingredients:
			self.ingredients.append(i)

	def getAuthorName(self, authorid):
		author = User.query.get(authorid)
		authorName = "Author not found"
		if author is not None:
			authorName = author.getFullName()
		return authorName

	def countComments(self):
		return len(self.comments)

	# TODO: DOUBLE CHECK THIS FUNCTION. results don't look right.
	def getDaysSinceString(self):
	    today = datetime.datetime.now()
	    timeSince = today - self.recipedate
	    hours = timeSince.seconds//3600

	    # Determine correct phrasing
	    hourString = "hour" if hours == 1 else "hours"
	    dayString = "day" if timeSince.days == 1 else "days"
	    if timeSince.days == 0:
	    	return "{} {}".format(hours, hourString)
	    else:
	    	return "{} {}, {} {}".format(timeSince.days, dayString, hours, hourString)
	    	
class Ingredient(db.Model):
	__tablename__ = 'ingredients'
	ingredientid = db.Column(db.Integer, primary_key=True)
	ingredientname = db.Column(db.String(40), unique=True)

	def __init__(self, ingredientname):
		self.ingredientname = string.capwords(ingredientname)

class Comment(db.Model):
	__tablename__ = 'comments'
	commentid = db.Column(db.Integer, primary_key=True)
	recipeid = db.Column(db.Integer, db.ForeignKey('recipes.recipeid'))
	authorid = db.Column(db.Integer, db.ForeignKey('users.uid'))
	commentdate = db.Column(db.DateTime)
	commentdesc = db.Column(db.Text)
	
	def __init__(self, commentdesc, email):
		author = User.query.filter_by(email = email).first()
		self.authorid = author.uid
		self.commentdate = datetime.datetime.now()
		self.commentdesc = commentdesc
	
	def getAuthorName(self, authorid):
		author = User.query.get(authorid)
		authorName = "Author not found"
		if author is not None:
			authorName = author.getFullName()
		return authorName

class GPlace(object):
	def address_to_latlng(self, address):
		g = geocoder.google(address)
		if g.ok:
			return (g.lat, g.lng)
		else:
			return (WATERLOO_COORDINATES["lat"], WATERLOO_COORDINATES["lng"])

	def query(self, lat, lng):
		latlng = {"lat":lat, "lng":lng}
		query_result = gp.nearby_search(lat_lng=latlng, radius=500, type=types.TYPE_BAR)

		#place.get_details has to be run for each place in order for the html page to access its "url" field.
		for place in query_result.places:
			place.get_details()
			#Available Options: icon, types, geo_location, name, vicinity, rating, details, formatted_address
			#, local_phone_number, website, url

		return query_result.places