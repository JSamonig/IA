from app.models import User
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, FloatField, IntegerField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Regexp, Length, EqualTo, ValidationError, Optional
from app import handlefiles
import config as c


class uploadForm(FlaskForm):
    file = FileField(validators=[DataRequired(), FileAllowed(c.Config.ALLOWED_EXTENSIONS_IMAGES, 'Images only!')])
    submit = SubmitField('Submit')


class editOutput(FlaskForm):
    date = StringField('Date', validators=[DataRequired(), Regexp(c.Config.DATE_PATTERN, 0, "Invalid date pattern")])
    description = StringField('Description', validators=[DataRequired()])
    miles = FloatField('Miles', validators=[Optional()])
    accountCode = IntegerField('Account Code', validators=[DataRequired()])
    total = FloatField('Total', validators=[Optional()])
    submit = SubmitField('Submit')

#  --> Adapted from https://blog.miguelgrinberg.com/

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Surname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

# <--


class settings(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Surname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    accounting_email = StringField('Accounting email', validators=[DataRequired(), Email()])
    taggun = BooleanField('Use TAGGUN API for OCR', validators=[])
    submit = SubmitField('Apply')

    def __init__(self, user_id, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id

    def validate_email(self, email):
        current_user = User.query.filter_by(id=self.user_id).first()
        user = User.query.filter_by(email=email.data).first()
        if user is not None and current_user != user:
            raise ValidationError('Please use a different email address.')


class newReclaim(FlaskForm):
    filename = StringField('File name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
