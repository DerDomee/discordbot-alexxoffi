from src.database import Base
from sqlalchemy import Column, String, Integer


class UserWarnings(Base):

    __tablename__ = 'user_warnings'
    __table_args__ = {
        'extend_existing': True
        }

    warn_id = Column(
        Integer(),
        primary_key=True,
        nullable=False)

    reason = Column(
        String(1024),
        nullable=False)

    issuer = Column(
        String(64),
        nullable=False)

    warned_user = Column(
        String(64),
        nullable=False)

    def __repr__(self):
        return "<Warn(warned_user='%s';reason='%s')>" % (
            self.user_discord_id,
            self.reason)
