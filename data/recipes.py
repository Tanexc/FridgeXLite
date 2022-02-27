import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Recipe(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "recipes"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    category_global = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    category_local = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    recipe_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    recipe = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    recipe_value = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    time = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    is_starred = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    actions = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    source = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    calories = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    proteins = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    fats = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    carboh = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    banned = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
