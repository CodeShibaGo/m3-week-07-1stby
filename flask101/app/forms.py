from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
import sqlalchemy as sa
from app import db
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('使用者名稱', validators=[DataRequired()])
    password = PasswordField('密碼', validators=[DataRequired()])
    remember_me = BooleanField('記住我')
    submit = SubmitField('登入')

class RegistrationForm(FlaskForm):
    username = StringField('使用者名稱', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('密碼', validators=[DataRequired()])
    password2 = PasswordField(
        '確認密碼', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('註冊')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('請求重設密碼')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class EditProfileForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    about_me = TextAreaField('About_me',validators=[Length(min=0,max=200)])
    submit = SubmitField('提交')
    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(User).where(
                User.username == self.username.data))
            if user is not None:
                raise ValidationError('Please use a different username.')
            
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')
 
class PostForm(FlaskForm):
    post = TextAreaField('說點什麼', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('提交')