from flask import render_template
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.user import User, db
from . import auth

@auth.route('/signup')
def signup():
    return render_template('auth/signup.html')

@auth.route('/login')
def login():
    return render_template('auth/login.html')

@auth.route('/logout')
def logout():
    return render_template('auth/logout.html')