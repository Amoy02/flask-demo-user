from flask_wtf import FlaskForm
#from wtforms import StringField,Form,validators,SubmitField
from wtforms.validators import DataRequired,Email
from wtforms import StringField,TextField, validators, TextAreaField, PasswordField
from wtforms import StringField, IntegerField, FileField, SelectField
from wtforms.validators import InputRequired
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileField, FileAllowed, FileRequired

#Registration form to allow users to sign up
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    location = StringField('Location', validators=[DataRequired()])
    biography = TextAreaField('Biography', validators=[DataRequired()])
    photo = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    register = SubmitField("Register")


#Posts Form for the Photogram 
class PostsForm(FlaskForm):
    caption = TextAreaField('Caption', validators=[DataRequired()])
    photo = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    #submit = SubmitField("Submit")
    
#Login form to allow users to login
class LoginForm(FlaskForm):
    username=TextField('Username',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
