from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(3, 150)])
    remember = BooleanField('Remember me')
    submit = SubmitField()

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(3, 150)])
    submit = SubmitField()

class CommentForm(FlaskForm):
    Content = TextAreaField(id='content',label='')
    submit = SubmitField(id='submit_review')
    

class SearchForm(FlaskForm):
    keyword = StringField('Keyword', validators=[DataRequired()])
    submit = SubmitField()
    
class UploadMusicForm(FlaskForm):
    file = FileField('MusicFile', validators=[DataRequired()])

class SettingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField()
   
    