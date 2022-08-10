from flask import render_template, flash, redirect, request, session
from flask_app import app
from flask_app.models.message import Message
from flask_app.models.user import User

@app.route('/new/message')
def new_message():
    if 'user_id' not in session:
        return redirect('/homepage')
    data = {
        "id" : session['user_id']
    }
    user = User.get_one(data)
    return redirect('homepage.html', user = user)

@app.route('/create/message', methods=['POST'])
def create_message():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Message.validate_message(request.form):
        return redirect('/new/message')
    data = {
        "message" : request.form['message'],
        "user_id" : session['user_id']
    }
    Message.save(data)
    return redirect('/homepage')

@app.route('/destroy/message/<int:id>')
def destroy_message(id):
    if 'user_id' not in session:
        return redirect('/logout')

    data = {
        "id": id
    }
    Message.destroy(data)
    return redirect('/homepage')