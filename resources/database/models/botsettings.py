from resources.database import Base
from sqlalchemy import Column, String


class BotSettings(Base):

    __tablename__ = 'bot_settings'
    __table_args__ = {
        'extend_existing': True
        }

    setting_key = Column(
        String(64),
        primary_key=True)

    setting_value = Column(
        String(2048))

    def __repr__(self):
        return "<BotSetting(key='%s', value='%s')>" % \
            (self.setting_key, self.setting_value)
