from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,PasswordField,TextAreaField,FloatField,DateField
from wtforms.validators import InputRequired,EqualTo

class RegistrationForm(FlaskForm):
    user = StringField("Username:",validators=[InputRequired()])
    password = PasswordField("Password:",validators=[InputRequired()])
    password2 = PasswordField("Confirm password:",validators=[InputRequired(),EqualTo("password")])
    submit= SubmitField("Submit")

class LoginForm(FlaskForm):
    user = StringField("Username:",validators=[InputRequired()])
    password = PasswordField("Password:",validators=[InputRequired()])
    submit= SubmitField("Submit")

