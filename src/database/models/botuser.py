from src.database import Base
from sqlalchemy import Column, String, Integer


class BotUser(Base):

    __tablename__ = 'bot_user'
    __table_args__ = {
        'extend_existing': True
        }

    user_discord_id = Column(
        String(64),
        primary_key=True,
        nullable=False)

    user_pref_lang = Column(
        String(2),
        nullable=False)

    user_permission_level = Column(
        Integer(),
        nullable=False)

    def __repr__(self):
        return "<User(user_discord_id='%s')>" % (self.user_discord_id)
