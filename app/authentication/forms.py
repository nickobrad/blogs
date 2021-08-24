from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, ValidationError, SubmitField
from wtforms.validators import Required, Email, EqualTo
from ..models.user import User

class LoginForm(FlaskForm):
    username = StringField('Your Username', validators=[Required()])
    password = PasswordField('Password', validators = [Required()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In') 

class RegistrationForm(FlaskForm):
    firstname = StringField('Enter your first name', validators = [Required()])
    lastname = StringField('Enter your last name', validators = [Required()])
    username = StringField('Enter your username', validators = [Required()])
    email = StringField('Your email address', validators=[Required(), Email()])
    password = PasswordField('Password', validators = [Required(), EqualTo('password_confirm', message = 'Passwords must match')])
    password_confirm = PasswordField('Confirm Password', validators = [Required()])
    submit = SubmitField('Sign Up')

    def validate_email(self, data_field):
        if User.query.filter_by(email = data_field.data).first():
            raise ValidationError('There is an account with that email!')

    def validate_username(self, data_field):
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError('That username is taken!')