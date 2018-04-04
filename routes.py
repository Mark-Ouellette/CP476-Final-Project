import os
from flask import Flask, render_template, request, session, redirect, url_for
from models import db, User, Ingredient, Recipe, Comment, GPlace
from forms import SignupForm, LoginForm, AddressForm, IngredientForm, AddArticleForm, AddCommentForm
from sqlalchemy import exc, desc
import wtforms.ext.sqlalchemy.fields as f 



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/learningflask'
db.init_app(app)

app.secret_key = "development-key"

# Override the wtforms.ext.sqlalchemy function as it was throwing a "ValueError" and has yet to be repaired.
# Ref: https://github.com/wtforms/wtforms-sqlalchemy/issues/9
def get_pk_from_identity(obj):
    cls, key = f.identity_key(instance=obj)[:2]
    return ':'.join(f.text_type(x) for x in key)                             

@app.before_first_request
def createDB():
	f.get_pk_from_identity = get_pk_from_identity
	db.create_all()

@app.route("/", methods=['GET', 'POST'])
def index():
	recipes = Recipe.query.order_by(desc(Recipe.recipedate)).all()
	ingredients = Ingredient.query.order_by(Ingredient.ingredientname).all()
	filters=[]
	if request.method == 'POST':
		for i in ingredients:
			f = request.form.get(str(i.ingredientid))
			if f:
				filters.append(i.ingredientid)
		if len(filters) > 0:
			recipes = Recipe.query.join(Recipe.ingredients).filter(Ingredient.ingredientid.in_(filters))

	return render_template("index.html", recipes=recipes, ingredients=ingredients, filters=filters)

@app.route("/recipes/<int:id>", methods=['GET', 'POST'])
def recipe(id):
	recipe = Recipe.query.get_or_404(id)
	enableComments = False
	commForm = AddCommentForm()

	if 'email' in session:
		enableComments = True
		if request.method == 'POST':
			if commForm.validate():
				newComment = Comment(commForm.commentdesc.data, session['email'])
				recipe.comments.append(newComment)
				db.session.commit()
	return render_template("recipe.html", recipe=recipe, enableComments=enableComments, form=commForm)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
	if 'email' in session:
		redirect(url_for('index'))

	form = SignupForm()
	existingUserError = []

	if request.method == 'POST':
		if not form.validate():
			return render_template("signup.html", form=form, existingUserError=existingUserError)
		else:
			# TODO: Handle the duplicate email "IntegrityError" the same way duplicate ingredients are handled
			newUser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
			try:
				db.session.add(newUser)
				db.session.commit()
				print("session commited")
				session['email'] = newUser.email
				session['name'] = newUser.getFullName()
				return redirect(url_for('index'))
			except exc.IntegrityError:
				db.session.rollback()
				existingUserError.append("User email already exists")
				return render_template("signup.html", form=form, existingUserError=existingUserError)

	elif request.method == 'GET':
		return render_template("signup.html", form=form, existingUserError=existingUserError)

@app.route("/login", methods=['GET','POST'])
def login():
	if 'email' in session:
		redirect(url_for('index'))

	form = LoginForm()
	if request.method == 'POST':
		if not form.validate():
			print("Can't validate")
			return render_template("login.html", form=form)
		else:
			print("here3")
			email = form.email.data
			password = form.password.data

			user = User.query.filter_by(email=email).first()
			if user is not None and user.check_password(password):
				session['email'] = email
				session['name'] = user.getFullName()
				return redirect(url_for('index'))
			else:
				# TODO: Expand to say whether the email or password failed
				form.email.errors.append("The user could not be validated")
				return render_template('login.html', form=form, method='GET')
	elif request.method == 'GET':
		return render_template("login.html", form=form)

@app.route("/logout")
def logout():
	session.pop('email', None)
	session.pop('name', None)
	return redirect(url_for('index'))


@app.route("/maps", methods=['GET','POST'])
def maps():
	#if 'email' not in session:
	#	return redirect(url_for('login'))

	form = AddressForm()
	places = []
	my_coordinates = {}

	if request.method == 'POST':
		if not form.validate():
			return render_template('maps.html', form=form)
		else:
			address = form.address.data

			p = GPlace()
			# geocoder.google(address) isn't doing a great job of getting lat/lng's, often misses
			# Default is WLU
			lat, lng = p.address_to_latlng(address)
			my_coordinates = {"lat": lat, "lng": lng}
			places = p.query(lat, lng)
			print (places)

			return render_template('maps.html', form=form, my_coordinates=my_coordinates, places=places)
			
	elif request.method == 'GET':
		return render_template("maps.html", form=form, my_coordinates=my_coordinates, places=places)

@app.route("/add/recipe", methods=['GET','POST'])
def addRecipe():
	if 'email' not in session:
		return redirect(url_for('login'))

	recForm = AddArticleForm()
	# Temporarily passing this message object in order to display an added message under the form.
	message = ""

	if request.method == 'POST':
		if not recForm.validate():
			return render_template('newrecipe.html', recForm=recForm, message=message)
		else:

			# The Recipe constructor adds each ingredient in this tuple as a child which handles the many-to-many relationship
			ingredients = recForm.recipeingredients.data
			newRec = Recipe(recForm.recipetitle.data, recForm.recipedesc.data, ingredients, session['email'])

			# No Try/Catch here because the db is not configured to require unique titles
			db.session.add(newRec)
			db.session.commit()
			message = "Recipe added: " + newRec.recipetitle
			return redirect(url_for('index'))

	elif request.method == 'GET':
		return render_template('newrecipe.html', recForm=recForm, message=message)


@app.route("/add/ingredient", methods=['GET','POST'])
def addIngredient():
	if 'email' not in session:
		return redirect(url_for('login'))

	ingForm = IngredientForm()
	# Temporarily passing this message object in order to display an added message under the form.
	message = ""

	if request.method == 'POST':
		if not ingForm.validate():
			return render_template('addIngredient.html', ingForm=ingForm, message=message)
		else:
			newIng = Ingredient(ingForm.ingredientname.data)
			#An IntegrityError here indicates a duplicate was found. The id in the db is still
			#generated for some reason but the entry isn't added, so there will be skipped id's (not a problem)
			try:
				db.session.add(newIng)
				db.session.commit()
				message = "Ingredient added: " + newIng.ingredientname
			except exc.IntegrityError as e:
				db.session.rollback()
				ingForm.ingredientname.errors.append("The specified Ingredient Name already exists!")
			finally:
				return render_template('addIngredient.html', ingForm=ingForm, message=message)

	elif request.method == 'GET':
		return render_template('addIngredient.html', ingForm=ingForm, message=message)

if __name__ == "__main__":
    app.run(debug=True)








