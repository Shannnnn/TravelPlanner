from flask_wtf import Form
from wtforms import StringField, PasswordField, ValidationError, DateField, IntegerField, SubmitField, FileField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from model import User


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegisterForm(Form):
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=3, max=25)]
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(), EqualTo('password', message='Passwords must match.')
        ]
    )

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

class EditForm(Form):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    birth_date = DateField('Birth Date(mm/dd/yyyy)', format='%m/%d/%Y', validators=[DataRequired()])
    contact_num = IntegerField('Contact Number', validators=[DataRequired()])
    description = StringField('Description')
    gender = RadioField('Label', choices=[('male','Male'),('female','Female')])
    file = FileField('Choose Profile Picture')

class PasswordSettingsForm(Form):
    currpassword = PasswordField('Current Password', validators=[DataRequired()])
    newpassword = PasswordField('New Password', validators=[DataRequired(), Length(min=6, max=25)])
    confirm = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('newpassword', message='Passwords must match.')])

class TrialForm(Form):
	trial = StringField('Trial')

class SearchForm(Form):
    search = StringField('',validators=[DataRequired()])

class EmailResetForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email(message=None), Length(min=6, max=40)])

class PasswordResetForm(Form):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=25)])
    confirm = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])



