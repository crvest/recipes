from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app.models import user

class Recipe:
    def __init__(self, data):
        self.id  = data['id']

        self.name = data['name']
        self.description = data['description']
        self.under30 = data['under30']
        self.instructions = data['instructions']
        self.date_made = data['date_made']

        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

        self.user = {}

    # save a new recipe
    @classmethod
    def save_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, under30, instructions, date_made, user_id) VALUES (%(name)s, %(description)s, %(under30)s, %(instructions)s, %(date_made)s, %(user_id)s);"
        result = connectToMySQL('recipes_db').query_db(query, data)
        return result

    # get a single recipe
    @classmethod
    def get_one_recipe(cls, data):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(recipe_id)s;"
        result = connectToMySQL('recipes_db').query_db(query, data)
        recipe = cls(result[0])
        user_data = {
            'id' : result[0]['users.id'],
            'first_name' : result[0]['first_name'],
            'last_name' : result[0]['last_name'],
            'email' : result[0]['email'],
            'password' : result[0]['password'],
            'created_at' : result[0]['users.created_at'],
            'updated_at' : result[0]['users.updated_at']
        }
        recipe.user = user.User(user_data)
        return recipe

    # get all recipes with user data attached
    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id;"
        result = connectToMySQL('recipes_db').query_db(query)
        all_recipes_with_users = []
        for row in result:
            # creating instance of recipe
            recipe = cls(row)
            # gathering user data to create instance of user inside of instance of recipe
            user_data = {
                'id' : row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }
            # creating recipe instance with user instance attached
            recipe.user = user.User(user_data)
            # appending list of all reecipes with each recipe instance
            all_recipes_with_users.append(recipe)
        return all_recipes_with_users

    # validate recipe
    @staticmethod
    def validate_recipe(form_data):
        is_valid = True
        if len(form_data['name']) < 3:
            flash('Recipe name must be at least 3 characters')
            is_valid = False
        if len(form_data['description']) < 3:
            flash('Description must be at least 3 characters')
            is_valid = False
        if len(form_data['instructions']) < 3:
            flash('Instructions must be at least 3 characters')
            is_valid = False
        # test for correct email format ____@____.___
        if len(form_data['date_made']) == 0:
            flash('Date made must be selected')
            is_valid = False
        if form_data['under30'] == '':
            flash('Ready in 30 minutes field must be selected')
            is_valid = False
        return is_valid
    
    # update recipe
    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, under30 = %(under30)s, instructions = %(instructions)s, date_made = %(date_made)s WHERE id = %(user_id)s;"
        result = connectToMySQL('recipes_db').query_db(query, data)
        return result

    # delete recipe
    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(recipe_id)s;"
        result = connectToMySQL('recipes_db').query_db(query, data)
        return result