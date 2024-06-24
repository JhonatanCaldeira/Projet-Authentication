from flask import render_template, request, flash
import requests
from flask import redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import API_URL
from ..models.user import User, db
from . import auth

headers = {
    "Content-Type":'application/json'
}

@auth.route('/signup')
def signup():
    return render_template('auth/signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    
    response = requests.put(f"{API_URL}/users",
                            json={
                                "email": email,
                                "name": name,
                                "password": password
                            },
                            headers=headers)    
    
    if response.status_code == 400:
        error = response.json().get('error')
        flash(error)
        return redirect(url_for('auth.signup'))
        
    
    return redirect(url_for('auth.login'))

@auth.route('/login')
def login():
    return render_template('auth/login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')    
    password = request.form.get('password')    
    remember = request.form.get('remember')
    
    # is user exists

    response = requests.post(f"{API_URL}/users",
                        json={
                            "email": email,
                            "password": password
                        },
                        headers=headers)    

    if response.status_code == 400:
        error = response.json().get('error')
        flash(error)
        #flash(" Please check your login details and try again")
        return render_template('auth/login.html')
    
    login_user(User.from_dict(response.json()), remember=remember)
    return redirect(url_for('main.profile'))
        
    
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))