from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from urllib.parse import urljoin
from urllib.request import urlopen
from googleplaces import GooglePlaces, types, lang


import geocoder
import json


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
		self.firstname = firstname.title()
		self.lastname = lastname.title()
		self.email = email.lower()
		self.set_password(password)
	 
	def set_password(self, password):
		self.pwdhash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)


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
	recipedesc = db.Column(db.Text)
	recipetitle = db.Column(db.String(100))
	ingredients = db.relationship('Ingredient', secondary=ingredientsPerRecipe, lazy='subquery', 
		backref=db.backref('ingredients', lazy=True))

class Ingredient(db.Model):
	__tablename__ = 'ingredients'
	ingredientid = db.Column(db.Integer, primary_key=True)
	ingredientname = db.Column(db.String(40), unique=True)

	def __init__(self, ingredientname):
		self.ingredientname = ingredientname.title()

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