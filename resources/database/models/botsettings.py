from resources.database import Base
from sqlalchemy import Column, String

class BotSettings(Base):

    __tablename__ = 'bot_settings'

    setting_key = Column(
        String(64),
        primary_key=True)

    setting_value = Column(
        String
    )

    def __repr__(self):
        return "<BotSetting(key='%s', value='%s')>" % (self.setting_key, self.setting_value)
