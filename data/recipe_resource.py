import base64

from PIL.Image import Image
from flask import jsonify
from flask_restful import Resource, abort

from .daily_recipes import getDailyRecipes
from .recipes import Recipe
from . import db_session


class RecipeResource(Resource):
    def get(self, id):
        abort_if_user_not_found(id)
        session = db_session.create_session()
        recipe = session.query(Recipe).get(id)
        return jsonify({'recipe': recipe.to_dict(), "image_code": getByteStringFromIamge(id)})


class RecipeDailyResource(Resource):
    def get(self):
        session = db_session.create_session()
        recipes = getDailyRecipes()
        return jsonify({'recipes': [item.to_dict() for item in recipes], "images_codes": [getByteStringFromIamge(recipe.id) for recipe in recipes]})


class RecipeCategoryResource(Resource):
    def get(self, category: str):
        session = db_session.create_session()
        recipes = session.query(Recipe).filter(Recipe.category_global == category).all()
        return jsonify({'recipes': [item.to_dict() for item in recipes], "images_codes": [getByteStringFromIamge(recipe.id) for recipe in recipes]})


class RecipeListResource(Resource):
    def get(self):
        session = db_session.create_session()
        recipe = session.query(Recipe).all()
        return jsonify({'recipes': [item.to_dict() for item in recipe], "images_codes": [getByteStringFromIamge(recipe.id) for recipe in recipes]})


def abort_if_user_not_found(id):
    session = db_session.create_session()
    user = session.query(Recipe).get(id)
    if not user:
        abort(404, message=f"Recipe with id = {id} not found")


def getByteStringFromIamge(id: int):
    image = Image.open(f"recipe_{id}.jpg").read()
    encoded_string = base64.b64encode(image.read())
