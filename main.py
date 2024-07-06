
from app.database import init_db
from sqlalchemy.orm import Session
from app.models.models import Player, Character, Origin, Rule, Stat, CharacterStat, Skill, CharacterSkill, Attribute, CharacterSkillAttribute
from app.utils import get_db

def main():
    init_db()
    db: Session = next(get_db())

    new_player = Player(username="player1", password="password")
    db.add(new_player)
    db.commit()
    db.refresh(new_player)
    print(f"Created new player with ID: {new_player.id}")

    db.close()

if __name__ == "__main__":
    main()