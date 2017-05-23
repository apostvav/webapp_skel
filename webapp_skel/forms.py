from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError
from .models import User

class ArticleForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    article = StringField('article', validators=[DataRequired()])
    tags = StringField('Tags', validators=[Regexp(r'^[a-zA-Z0-9, ]*$',
        message="Tags can only contain letters and numbers")])

    def validate(self):
        if not FlaskForm.validate(self):
            return False

        # filter out empty and dupliocate tag names
        stripped = [t.strip() for t in self.tags.data.split(',')]
        not_empty = [tag for tag in stripped if tag]
        tagset = set(not_empty)
        self.tags.data = ",".join(tagset)

        return True

class LoginForm(FlaskForm):
    username = StringField('Your username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(4, 20),
            Regexp('^[A-Za-z0-0_]{3,}$', message='Usernames consist of numbers, letters and underscores')])
    password = PasswordField('Password', validators=[DataRequired(),
            EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Length(5,40), Email()])

    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError('There already is a user with this email address.')

    def validate_username(self, username_field):
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError('This username is already taken.')
