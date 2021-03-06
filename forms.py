from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()], description="username")
    password = PasswordField('Password', validators=[DataRequired()], description="password")


class RegisterForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired()], description="name")
    username = StringField('Username', validators=[DataRequired()], description="username")
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message="Password must be at least 6 characters.")], description="password")
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password', message="Passwords must match.")], description="confirm password")


class GroupForm(FlaskForm):

    name = StringField("Title", validators=[DataRequired()], description="name")
    description = TextAreaField("Description", description="description")


class PostForm(FlaskForm):

    content = TextAreaField("Content", description="content")


class SpotifySearchForm(FlaskForm):

    query = StringField('Query', validators=[DataRequired()], description="search for songs")


class EditUserForm(FlaskForm):

    full_name = StringField('Name', validators=[DataRequired()], description="name")
    username = StringField('Username', validators=[DataRequired()], description="username")
    introduction = TextAreaField('Introduction', description="introduction")