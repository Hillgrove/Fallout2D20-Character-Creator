
from app import db, login_manager
from flask_login import UserMixin


# Load the user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)

    # Relationship with characters
    characters = db.relationship('Character', back_populates='user', lazy=True)

class Character(db.Model):
    __tablename__ = "character"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    current_xp = db.Column(db.Integer, default=0, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    origin_id = db.Column(db.Integer, db.ForeignKey("origin.id"), nullable=False)

    # Relationships to User and Origin
    user = db.relationship("User", back_populates='characters')
    origin = db.relationship("Origin", back_populates='characters')

class Stat(db.Model):
    __tablename__ = "stat"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)

class CharacterStat(db.Model):
    __tablename__ = "character_stat"
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"), primary_key=True)
    stat_id = db.Column(db.Integer, db.ForeignKey("stat.id"), primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    
    # Relationships to Character and Stat
    character = db.relationship("Character", backref='character_stats')
    stat = db.relationship("Stat", backref='character_stats')

class Skill(db.Model):
    __tablename__ = "skill"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)

class CharacterSkill(db.Model):
    __tablename__ = "character_skill"
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"), primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey("skill.id"), primary_key=True)
    value = db.Column(db.Integer, default=0, nullable=False)

    # Relationships to Character and Skill
    character = db.relationship("Character", backref='character_skills')
    skill = db.relationship("Skill", backref='character_skills')

class Attribute(db.Model):
    __tablename__ = "attribute"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)

class CharacterSkillAttribute(db.Model):
    __tablename__ = "character_skill_attribute"
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"), primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey("skill.id"), primary_key=True)
    attribute_id = db.Column(db.Integer, db.ForeignKey("attribute.id"), primary_key=True)
    
    # Relationships to Character, Skill, and Attribute
    character = db.relationship("Character", backref='character_skill_attributes')
    skill = db.relationship("Skill", backref='character_skill_attributes')
    attribute = db.relationship("Attribute", backref='character_skill_attributes')

class Origin(db.Model):
    __tablename__ = "origin"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name= db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    rule_id = db.Column(db.Integer, db.ForeignKey("rule.id"), nullable=False)

    # Relationship to Rulem Character
    rule = db.relationship("Rule", back_populates='origins')
    characters = db.relationship("Character", back_populates='origin')

class Rule(db.Model):
    __tablename__ = "rule"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    rule_data = db.Column(db.JSON, nullable=False)

    # Relationship to Origins
    origins = db.relationship("Origin", back_populates='rule')