
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, NumberRange
from app.models import User, Origin, Perk
import logging

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
        self.origin_id.choices = [(origin.id, origin.name) for origin in Origin.query.all()]

class StatForm(FlaskForm):
    strength = IntegerField('Strength', validators=[DataRequired(), NumberRange(min=1, max=10)])
    perception = IntegerField('Perception', validators=[DataRequired(), NumberRange(min=1, max=10)])
    endurance = IntegerField('Endurance', validators=[DataRequired(), NumberRange(min=1, max=10)])
    charisma = IntegerField('Charisma', validators=[DataRequired(), NumberRange(min=1, max=10)])
    intelligence = IntegerField('Intelligence', validators=[DataRequired(), NumberRange(min=1, max=10)])
    agility = IntegerField('Agility', validators=[DataRequired(), NumberRange(min=1, max=10)])
    luck = IntegerField('Luck', validators=[DataRequired(), NumberRange(min=1, max=10)])
    submit = SubmitField("Next")

    def __init__(self, origin_id, *args, **kwargs):
        super(StatForm, self).__init__(*args, **kwargs)
        self.origin_id = origin_id
        self.origin = Origin.query.get(origin_id)

        # Create a dictionary of stat field names and their corresponding field objects
        stat_fields = {
            'Strength': self.strength,
            'Perception': self.perception,
            'Endurance': self.endurance,
            'Charisma': self.charisma,
            'Intelligence': self.intelligence,
            'Agility': self.agility,
            'Luck': self.luck
        }

        # Update validators based on traits
        for trait in self.origin.traits:
            logging.info(f"Processing trait: {trait.name}")
            if "stat" in trait.trait_data:
                stat_name = trait.trait_data["stat"]
                max_value = trait.trait_data["max"]
                logging.info(f"Setting max value for {stat_name} to {max_value}")
                if stat_name in stat_fields:
                    field = stat_fields[stat_name]
                    # Update the field validators
                    field.validators = [v for v in field.validators if not isinstance(v, NumberRange)]
                    field.validators.append(NumberRange(min=1, max=max_value))
                    logging.info(f"{stat_name} validators: {field.validators}")

        # Log the final validators for each stat
        for stat_name, field in stat_fields.items():
            logging.info(f"{stat_name} final validators: {field.validators}")


        # Print out the validators for debugging purposes
        for stat_name, field in stat_fields.items():
            print(f"{stat_name} validators: {field.validators}")

class PerkForm(FlaskForm):
    perks = SelectMultipleField("Perks", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Next")

    def __init__(self, *args, **kwargs):
        super(PerkForm, self).__init__(*args, **kwargs)
        self.perks.choices = [(perk.id, perk.name) for perk in Perk.query.all()]

class DeleteForm(FlaskForm):
    pass

class SkillForm(FlaskForm):
    skills = SelectMultipleField("Skills", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Next")