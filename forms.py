from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class EditProfileForm(FlaskForm):
    id_card = StringField('ID Card', validators=[DataRequired(), Length(max=20)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=100)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    profile_image = FileField('Profile Image')
    submit = SubmitField('Update Profile')
