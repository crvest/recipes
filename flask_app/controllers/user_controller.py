from crypt import methods
from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# index route
@app.route('/')
def index():
    return render_template('index.html')

# register route
@app.route('/register', methods=['POST'])
def register():
    # test for validations
    if not User.validate_registration(request.form):
        return redirect('/')
    # collect data for query, including hashing pw
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    query_data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }
    # add user data to db
    user_id = User.register_user(query_data)
    # log user in via session
    session['user_id'] = user_id
    # redirect to dashboard
    return redirect('/dashboard')


# login route
@app.route('/login', methods=['POST'])
def login():
    # test for validations
    if not User.validate_login(request.form):
        return redirect('/')
    # log user in via session
    logged_user = User.get_by_email(request.form)
    session['user_id'] = logged_user.id
    # redirect to dashboard
    return redirect('/dashboard')

# logout route, clears session data and returns to index
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect('/')

# dashboard route
@app.route('/dashboard')
def dashboard():
    # tests for logged in state before continuing to page
    if 'user_id' not in session:
        flash('Please login or register to continue')
        return redirect('/')
    # gets user id of logged in user and displays message in dashboard
    query_data = {
        'user_id' : session['user_id']
    }
    user = User.get_by_id(query_data)
    all_recipes = Recipe.get_all_recipes()
    # returns dashboard with user data for sinlgle user, which includes all recipes
    return render_template('dashboard.html', user = user, all_recipes = all_recipes)
