
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
    starting_stat_points = db.Column(db.Integer, nullable=False, default=40)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    origin_id = db.Column(db.Integer, db.ForeignKey("origin.id"), nullable=False)

    # Relationships to User and Origin
    user = db.relationship("User", back_populates='characters')
    origin = db.relationship("Origin", back_populates='characters')

    # Relationships to Stats, Skills, Attributes, and Perks with cascading deletes
    character_stats = db.relationship("CharacterStat", back_populates='character', cascade='all, delete-orphan')
    character_skill_attributes = db.relationship("CharacterSkillAttribute", back_populates='character', cascade='all, delete-orphan')
    character_perks = db.relationship("CharacterPerk", back_populates='character', cascade='all, delete-orphan')
    character_traits = db.relationship("CharacterTrait", back_populates='character', cascade='all, delete-orphan', lazy='dynamic')


class Stat(db.Model):
    __tablename__ = "stat"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    
    # Relationships
    character_stats = db.relationship("CharacterStat", back_populates='stat')
    perk_stat_1 = db.relationship("Perk", foreign_keys="[Perk.stat_1_id]", back_populates='stat_1')
    perk_stat_2 = db.relationship("Perk", foreign_keys="[Perk.stat_2_id]", back_populates='stat_2')


class CharacterStat(db.Model):
    __tablename__ = "character_stat"
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"), primary_key=True)
    stat_id = db.Column(db.Integer, db.ForeignKey("stat.id"), primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    
    # Relationships to Character and Stat
    character = db.relationship("Character", back_populates='character_stats')
    stat = db.relationship("Stat", back_populates='character_stats')


class CharacterTrait(db.Model):
    __tablename__ = "character_trait"
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"), primary_key=True)
    trait_id = db.Column(db.Integer, db.ForeignKey("trait.id"), primary_key=True)
    
    # Relationships to Character and Trait
    character = db.relationship("Character", back_populates='character_traits')
    trait = db.relationship("Trait", back_populates='character_traits')

    __table_args__ = (db.UniqueConstraint('character_id', 'trait_id', name='_character_trait_uc'),)


class Skill(db.Model):
    __tablename__ = "skill"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    
    # Relationship to CharacterSkillAttribute
    character_skill_attributes = db.relationship("CharacterSkillAttribute", back_populates='skill')


class Attribute(db.Model):
    __tablename__ = "attribute"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    # Relationship to CharacterSkillAttribute
    character_skill_attributes = db.relationship("CharacterSkillAttribute", back_populates='attribute')


class CharacterSkillAttribute(db.Model):
    __tablename__ = "character_skill_attribute"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey("skill.id"), nullable=False)
    attribute_id = db.Column(db.Integer, db.ForeignKey("attribute.id"), nullable=True)
    value = db.Column(db.Integer, nullable=False)
    
    # Relationships to Character, Skill, and Attribute
    character = db.relationship("Character", back_populates='character_skill_attributes')
    skill = db.relationship("Skill", back_populates='character_skill_attributes')
    attribute = db.relationship("Attribute", back_populates='character_skill_attributes', foreign_keys=[attribute_id])

    __table_args__ = (db.UniqueConstraint('character_id', 'skill_id', name='_character_skill_uc'),)


class Origin(db.Model):
    __tablename__ = "origin"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    selectable_traits_limit = db.Column(db.Integer, nullable=False, default=0)

    # Relationship to Character
    characters = db.relationship("Character", back_populates='origin')

    # Relationship to OriginTrait
    origin_traits = db.relationship("OriginTrait", back_populates='origin', cascade='all, delete-orphan')


class Trait(db.Model):
    __tablename__ = "trait"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    trait_data = db.Column(db.JSON, nullable=False)
    is_selectable = db.Column(db.Boolean, default=False)

    # Relationship to OriginTrait and CharacterTrait
    origin_traits = db.relationship("OriginTrait", back_populates='trait', cascade='all, delete-orphan')
    character_traits = db.relationship("CharacterTrait", back_populates='trait', cascade='all, delete-orphan')


class OriginTrait(db.Model):
    __tablename__ = "origin_trait"
    origin_id = db.Column(db.Integer, db.ForeignKey("origin.id"), primary_key=True)
    trait_id = db.Column(db.Integer, db.ForeignKey("trait.id"), primary_key=True)
    
    # Relationships to Origin and Trait
    origin = db.relationship("Origin", back_populates='origin_traits')
    trait = db.relationship("Trait", back_populates='origin_traits')

    __table_args__ = (db.UniqueConstraint('origin_id', 'trait_id', name='_origin_trait_uc'),)


class Perk(db.Model):
    __tablename__ = "perk"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)
    stat_1_id = db.Column(db.Integer, db.ForeignKey('stat.id'), nullable=True)
    amount_1 = db.Column(db.Integer, nullable=True)
    stat_2_id = db.Column(db.Integer, db.ForeignKey('stat.id'), nullable=True)
    amount_2 = db.Column(db.Integer, nullable=True)
    mutual_exclusive = db.Column(db.String, nullable=True)
    description = db.Column(db.Text, nullable=False)
    
    # Relationships
    stat_1 = db.relationship("Stat", foreign_keys=[stat_1_id])
    stat_2 = db.relationship("Stat", foreign_keys=[stat_2_id])
    character_perks = db.relationship("CharacterPerk", back_populates='perk')


class CharacterPerk(db.Model):
    __tablename__ = "character_perk"
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"), primary_key=True)
    perk_id = db.Column(db.Integer, db.ForeignKey("perk.id"), primary_key=True) 
    
    # Relationships to Character and Perk
    character = db.relationship("Character", back_populates='character_perks')
    perk = db.relationship("Perk", back_populates='character_perks')

    __table_args__ = (db.UniqueConstraint('character_id', 'perk_id', name='_character_perk_uc'),)
