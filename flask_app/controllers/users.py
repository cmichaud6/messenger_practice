from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.user import User
from flask_app.models.message import Message
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    is_valid = User.validate_user(request.form)
    if not is_valid:
        return redirect('/')
    new_user = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "team_name" : request.form['team_name'],
        "email" : request.form['email'],
        "password" : bcrypt.generate_password_hash(request.form['password']),
    }
    id = User.save(new_user)
    if not id:
        flash('Email is already taken!', 'register')
        return redirect('/')
    session['user_id'] = id
    return redirect('/homepage')

@app.route('/login', methods=['POST'])
def login():
    data = {
        "email" : request.form['email']
    }
    user = User.get_user_by_email(data)

    if not user:
        flash('Invalid Email/Password', 'login')
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/homepage')

@app.route('/homepage')
def homepage():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id" : session['user_id']
    }
    user = User.get_one(data)
    users = User.get_all()
    messages = Message.get_all(data)
    # sender = User.get_sender(data)
    return render_template('homepage.html', user = user, users = users, messages = messages)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')