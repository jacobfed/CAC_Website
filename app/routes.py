from flask import render_template
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Jacob'}
    posts = [
            {
                'author' : { 'username': 'Natalie'},
                'body' : ' Fundraiser Event September 12th, 2018'
            },
            {
                'author' : { 'username': 'Nat'},
                'body' : ' Closed Christmas day'
            }
        ]
    return render_template('index.html', title='Home', posts=posts)
@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)
