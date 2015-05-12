from .Base import Base
from flask.ext.security import UserMixin

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Boolean,
    DateTime,
    String,
    Table,
)


class Subscription(Base, UserMixin):
    __tablename__ = 'subscription'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)

