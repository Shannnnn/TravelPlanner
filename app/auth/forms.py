from flask_wtf import Form
from wtforms import StringField, PasswordField, ValidationError, DateField, IntegerField, SubmitField, FileField
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
    file = FileField('Choose Profile Picture', validators=[DataRequired()])

class AdminEditForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    role_id = StringField('Role ID', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired(), Length(min=6, max=25)])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    birth_date = DateField('Birth Date(mm/dd/yyyy)', format='%m/%d/%Y', validators=[DataRequired()])
    contact_num = IntegerField('Contact Number', validators=[DataRequired()])
    description = StringField('Description')
    file = FileField('Choose Profile Picture', validators=[DataRequired()])
    
class TripForm(Form):
    tripID = StringField('Trip ID', validators=[DataRequired])
    tripName = StringField('Trip Name', validators=[DataRequired()])
    tripDateFrom = DateField('Date From(mm/dd/yyyy', format='%m/%d/%Y', validators=[DataRequired()])
    tripDateTo = DateField('Date To(mm/dd/yyyy', format='%m/%d/%Y', validators=[DataRequired()])
    id = StringField('User ID', validators=[DataRequired()])
    viewsNumber = IntegerField('Number of Views', validators=[DataRequired()])
    img_thumbnail = StringField('Image Thumbnail', validators=[DataRequired()])


class SearchForm(Form):
    search = StringField('',validators=[DataRequired()])

class EmailResetForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email(message=None), Length(min=6, max=40)])

class PasswordResetForm(Form):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=25)])
    confirm = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])



