from .Base import Base
from flask.ext.security import RoleMixin
from .User import roles_users

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)
from sqlalchemy.orm import relationship
import datetime

class Sighting(Base):
    __tablename__ = 'sighting'

    id = Column(Integer(), primary_key=True)
    location = Column(String(255))
    username = Column(String(80), default='Anonymous')
    date = Column(DateTime, default=datetime.datetime.now)