
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, NumberRange
from app.models import User, Origin

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is taken. Please choose a different one")
        
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

class BackgroundForm(FlaskForm):
    name = StringField("Character Name", validators=[DataRequired()])
    origin_id = SelectField("Origin", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Next")

    def __init__(self, *args, **kwargs):
        super(BackgroundForm, self).__init__(*args, **kwargs)
        # Populate origin choices from the database
        self.origin_id.choices = [(origin.id, Origin.name) for origin in Origin.query.all()]

class SpecialForm(FlaskForm):
    # Integer fields for each S.P.E.C.I.A.L. stat
    strength = IntegerField('Strength', validators=[DataRequired(), NumberRange(min=1, max=10)])
    perception = IntegerField('Perception', validators=[DataRequired(), NumberRange(min=1, max=10)])
    endurance = IntegerField('Endurance', validators=[DataRequired(), NumberRange(min=1, max=10)])
    charisma = IntegerField('Charisma', validators=[DataRequired(), NumberRange(min=1, max=10)])
    intelligence = IntegerField('Intelligence', validators=[DataRequired(), NumberRange(min=1, max=10)])
    agility = IntegerField('Agility', validators=[DataRequired(), NumberRange(min=1, max=10)])
    luck = IntegerField('Luck', validators=[DataRequired(), NumberRange(min=1, max=10)])
    submit = SubmitField("Next")
