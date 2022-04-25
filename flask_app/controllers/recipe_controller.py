from crypt import methods
from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# show recipe route, aceppts variable in url and passes to function
@app.route('/recipe/<int:recipe_id>')
def show_recipe(recipe_id):
    query_data = {
        'recipe_id' : recipe_id
    }
    one_recipe = Recipe.get_one_recipe(query_data)
    return render_template('show_instructions.html', one_recipe = one_recipe)

# renders new recipe page
@app.route('/recipes/new')
def new():
    # tests for logged in state before continuing to page
    if 'user_id' not in session:
        flash('Please login or register to continue')
        return redirect('/')
    return render_template('new.html')

# create recipe route
@app.route('/create_recipe', methods=['POST'])
def create_recipe():
    # test for failure of basic validations
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    # collect query data, all things not auto generated
    query_data = {
        'name' : request.form['name'],
        'description' : request.form['description'],
        'under30' : request.form['under30'],
        'instructions' : request.form['instructions'],
        'date_made' : request.form['date_made'],
        # does not come from form, need to pull from current user
        'user_id' : session['user_id']
    }
    # send query_data to query method
    Recipe.save_recipe(query_data)
    return redirect('/dashboard')

# renders edit recipe page
@app.route('/recipe/edit/<int:recipe_id>')
def edit(recipe_id):
    # tests for logged in state before continuing to page
    if 'user_id' not in session:
        flash('Please login or register to continue')
        return redirect('/')
    query_data = {
        'recipe_id' : recipe_id
    }
    one_recipe = Recipe.get_one_recipe(query_data)
    return render_template('edit.html', one_recipe = one_recipe)

# update recipe route
@app.route('/update_recipe', methods=['POST'])
def update_recipe():
    # test for failure of basic validations
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    Recipe.update_recipe(request.form)
    return redirect('/dashboard')

# delete recipe route
@app.route('/recipe/delete/<int:recipe_id>', methods=['GET', 'POST'])
def delete_recipe(recipe_id):
    query_data = {
        'recipe_id' : recipe_id
    }
    Recipe.delete_recipe(query_data)
    return redirect('/dashboard')