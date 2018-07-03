from flask import render_template, redirect, url_for
from app import app, db
from app.forms import LoginForm, RegistrationForm, PostForm
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User, Post

@app.route('/',  methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
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
@app.route('/user/<username>')
@login_required
def user(username):
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    user = User.query.filter_by(username=username).first_or_404()
    posts = [ 
            {'author': user, 'body': 'Test post #1'},
            {'author': user, 'body': 'Test post #2'},
            {'author': user, 'body': 'Test post #3'},
            {'author': user, 'body': 'Test post #4'}
            ]
    return render_template('user.html',form=form, user=user, posts=posts)
# ------------------------------------------
#       Login/Logout/Register
# ------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
