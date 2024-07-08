
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash


class Player(Base):
    __tablename__ = "player"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

class Character(Base):
    __tablename__ = "character"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    current_xp = Column(Integer, default=0, nullable=False)
    player_id = Column(Integer, ForeignKey("player.id"), nullable=False)
    origin_id = Column(Integer, ForeignKey("origin.id"), nullable=False)
    player = relationship("Player")
    origin = relationship("Origin")

class Stat(Base):
    __tablename__ = "stat"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=False)

class CharacterStat(Base):
    __tablename__ = "character_stat"
    character_id = Column(Integer, ForeignKey("character.id"), primary_key=True)
    stat_id = Column(Integer, ForeignKey("stat.id"), primary_key=True)
    value = Column(Integer, nullable=False)
    character = relationship("Character")
    stat = relationship("Stat")

class Skill(Base):
    __tablename__ = "skill"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=False)

class CharacterSkill(Base):
    __tablename__ = "character_skill"
    character_id = Column(Integer, ForeignKey("character.id"), primary_key=True)
    skill_id = Column(Integer, ForeignKey("skill.id"), primary_key=True)
    value = Column(Integer, default=0, nullable=False)
    character = relationship("Character")
    skill = relationship("Skill")

class Attribute(Base):
    __tablename__ = "attribute"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)

class CharacterSkillAttribute(Base):
    __tablename__ = "character_skill_attribute"
    character_id = Column(Integer, ForeignKey("character.id"), primary_key=True)
    skill_id = Column(Integer, ForeignKey("skill.id"), primary_key=True)
    attribute_id = Column(Integer, ForeignKey("attribute.id"), primary_key=True)
    character = relationship("Character")
    skill = relationship("Skill")
    attribute = relationship("Attribute")

class Origin(Base):
    __tablename__ = "origin"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name= Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=False)
    rule_id = Column(Integer, ForeignKey("rule.id"), nullable=False)
    rule = relationship("Rule")

class Rule(Base):
    __tablename__ = "rule"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=False)
    rule_data = Column(JSON, nullable=False)