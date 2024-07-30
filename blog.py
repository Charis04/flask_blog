from flask import Flask, render_template, url_for
from forms import ResgistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '11856faf2f17f6c58cc2fc52e1d53a5d'

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

@app.route("/register")
def register():
    form = ResgistrationForm()
    return render_template('register.html', title='Register', form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

if __name__ == "__main__":
    app.run(debug=True)
