from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, PostForm
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User, Post

# ------------------------------------------
#                   User
# ------------------------------------------
@app.route('/',  methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
            page, app.config['POSTS_PER_PAGE'], False)
    return render_template('index.html', title='Home', posts=posts.items)
@app.route('/events')
def events():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('events.html', title='Events', posts=posts)
@app.route('/aboutUs')
def aboutUs():
    return render_template('aboutUs.html', title='About Us')
@app.route('/whatWeDo')
def whatWeDo():
    return render_template('whatWeDo.html', title='What We Do')
@app.route('/partners')
def partners():
    return render_template('partners.html', title='Partners')
@app.route('/contactUs')
def contactUs():
    return render_template('contactUs.html', title='Contact Us')
@app.route('/donate')
def donate():
    return render_template('donate.html', title='Donate')
# ------------------------------------------
#                   Admin
# ------------------------------------------
@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect('/index')
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.order_by(Post.timestamp.desc()).all()
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
