from flask import render_template, url_for, flash, redirect, request
from flask_blog_package import app, db, bcrypt
from flask_blog_package.models import User, Post
from flask_blog_package.forms import ResgistrationForm, LoginForm, UpdateProfileForm
from flask_login import login_user, current_user, logout_user, login_required


posts = [
    {
        'author': 'Charis Adu',
        'title': 'Blog post 1',
        'content': 'This is my first blog post',
        'date_posted': 'July 27th, 2024'
    },
    {
        'author': 'Olaoluwa Adu',
        'title': 'Blog post 2',
        'content': 'Korewa watashi no ichi blogu posto desu',
        'date_posted': 'July 27th, 2024'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ResgistrationForm()
    if form.validate_on_submit():
        hashed_pword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pword)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login unsuccessful! Please check email or password", 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    form = UpdateProfileForm()
    display_pic = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', display_pic=display_pic, form=form)
