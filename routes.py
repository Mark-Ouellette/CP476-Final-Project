from flask import Flask, render_template, request, session, redirect, url_for
from models import db, User, GPlace, Ingredient, Recipe
from forms import SignupForm, LoginForm, AddressForm, IngredientForm, AddArticleForm
from sqlalchemy import exc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/learningflask'
db.init_app(app)

app.secret_key = "development-key"

@app.before_first_request
def createDB():
	db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/post")
def post():
	return render_template("post.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
	if 'email' in session:
		redirect(url_for('index'))

	form = SignupForm()

	if request.method == 'POST':
		if not form.validate():
			return render_template("signup.html", form=form)
		else:
			# TODO: Handle the duplicate email "IntegrityError" the same way duplicate ingredients are handled
			newUser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
			db.session.add(newUser)
			db.session.commit()

			session['email'] = newUser.email
			return redirect(url_for('index'))
	elif request.method == 'GET':
		return render_template("signup.html", form=form)

@app.route("/login", methods=['GET','POST'])
def login():
	if 'email' in session:
		redirect(url_for('index'))

	form = LoginForm()

	if request.method == 'POST':
		if not form.validate():
			return render_template("login.html", form=form)
		else:
			email = form.email.data
			password = form.password.data

			user = User.query.filter_by(email=email).first()
			if user is not None and user.check_password(password):
				session['email'] = email
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
def addrecipe():
    if 'email' in session:
        return render_template("newrecipe.html")
    else:
        return redirect(url_for('login'))

    recForm = AddArticleForm()
    if request.method == 'POST':
        if not recForm.validate():
            return render_template('newrecipe.html', recForm=recForm)
        else:
            newRec = Recipe(recForm.recipeingreedients.data, recForm.recipetitle.data, recForm.recipedesc.data)
        
        try:
            db.session.add(newRec)
            db.session.commit()
            message = "Article added"
        except exc.IntegrityError as e:
            db.session.rollback()
        finally:
            return render_template("newrecipe.html", recForm=recForm)

    elif request.method == 'GET':
        return render_template('newrecipe.html', recForm=recForm)

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








