import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Product(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "products"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    category = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    product = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_in_fridge = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    is_in_cart = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    amount = sqlalchemy.Column(sqlalchemy.REAL, nullable=True)
    is_starred = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    banned = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
