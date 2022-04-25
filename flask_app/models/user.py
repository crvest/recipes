from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import flash
import re
from flask_app.models import recipe

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']

        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.recipes = []

    # validate registration; form_data passed from request.form in register route
    @staticmethod
    def validate_registration(form_data):
        is_valid = True
        if len(form_data['first_name']) < 2:
            flash('First name must be at least 2 characters')
            is_valid = False
        if len(form_data['last_name']) < 2:
            flash('Last name must be at least 2 characters')
            is_valid = False
        # test for correct email format ____@____.___
        if not EMAIL_REGEX.match(form_data['email']):
            flash("Email must be in valid email format")
            is_valid = False
        # test for already registered user
        user_in_db = User.get_by_email(form_data)
        if user_in_db:
            flash('Email already registered')
            is_valid = False
        # test for pw and conf_pw match
        if form_data['password'] != form_data['conf_pw']:
            flash("Password and password confirmation do not match.")
            is_valid = False
        return is_valid

    # validate login; form_data passed form request.form in login route
    @staticmethod
    def validate_login(form_data):
        is_valid = True
        # test if user is in db
        user_in_db = User.get_by_email(form_data)
        # test if user email is already registered in db
        if not user_in_db:
            flash('Invalid Email/Password')
            is_valid = False
        # check password if user is in db
        elif not bcrypt.check_password_hash(user_in_db.password, form_data['password']):
            flash('Invalid Email/Password')
            is_valid = False
        return is_valid
    
    # register user; data passed from register route query_data, includes hashed pw
    @classmethod
    def register_user(cls, data):
        # inserts into users table of recipes_db
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        result = connectToMySQL('recipes_db').query_db(query, data)
        return result
    
    # get by email, queries user info by email for login route
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('recipes_db').query_db(query, data)
        # tests for data presence
        if len(result) < 1:
            return False
        # returns email
        return cls(result[0])

    # get by id, queries user info by id for
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(user_id)s;"
        result = connectToMySQL('recipes_db').query_db(query, data)
        # tests for data presence
        if len(result) < 1:
            return False
        # returns user id
        return cls(result[0])