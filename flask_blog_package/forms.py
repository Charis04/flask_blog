from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_blog_package import bcrypt
from flask_blog_package.models import User
from flask_login import current_user

class ResgistrationForm(FlaskForm):
    username = StringField(
        'Username', validators=[DataRequired(), Length(min=2, max=20)]
        )
    email = StringField(
        'Email', validators=[DataRequired(), Email()]
        )
    password = PasswordField(
        'Password', validators=[DataRequired()]
        )
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')]
        )
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already exists! Please choose a different one")
        
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("Email already exists! Please use a different one")


class LoginForm(FlaskForm):
    email = StringField(
        'Email', validators=[DataRequired(), Email()]
        )
    password = PasswordField(
        'Password', validators=[DataRequired()]
        )
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    """
    A Login validator that I created as an alternative to using the flask_login package

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("Account doesn't exist! Please check email")

    def validate_password(self, password):
        user = User.query.filter_by(email=self.email.data).first()
        if not bcrypt.check_password_hash(user.password, password.data):
            raise ValidationError("Incorrect password! Please check password")
    """


class UpdateProfileForm(FlaskForm):
    username = StringField(
        'Username', validators=[DataRequired(), Length(min=2, max=20)]
        )
    email = StringField(
        'Email', validators=[DataRequired(), Email()]
        )
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username already exists! Please choose a different one")
        
    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError("Email already exists! Please use a different one")
