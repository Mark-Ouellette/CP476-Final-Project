from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from models import Ingredient

class SignupForm(FlaskForm):
	first_name = StringField('First Name', validators=[DataRequired("Please enter your first name")])
	last_name = StringField('Last Name', validators=[DataRequired("Please enter your last name")])
	email = StringField('email', validators=[DataRequired("Please enter a valid email address"), Email("Please enter a valid email address.")])
	password = PasswordField('Password', validators=[DataRequired("Please enter your password"), Length(min=6, message="Please enter a password longer than 6 characters")])
	submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
	email = StringField('email', validators=[DataRequired("Please enter a valid email address"), Email("Please enter a valid email address.")])
	password = PasswordField('Password', validators=[DataRequired("Please enter your password")])
	submit = SubmitField('Sign in')	

class AddressForm(FlaskForm):
	address = StringField('address', validators=[DataRequired("Please enter an address")])
	submit = SubmitField('Search')

class IngredientForm(FlaskForm):
	ingredientname = StringField('Ingredient', validators=[DataRequired("Please enter an ingredient name"), Length(max=40, message="Names may not be longer than 40 characters")])
	submit = SubmitField('Add')

# Utility function returning a query object which can be fed to query_factory's
def getIngredients():
	return Ingredient.query

class AddArticleForm(FlaskForm):
	recipetitle = StringField('Title', validators=[DataRequired("Please enter an article title"), Length(max=100, message="Titles may not be longer than 100 characters")])
	recipeingredients = QuerySelectMultipleField(query_factory=getIngredients, get_label='ingredientname')
	recipedesc = TextAreaField('Article Text')
	submit = SubmitField('Add')

