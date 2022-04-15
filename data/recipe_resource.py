import base64

from PIL.Image import Image
from flask import jsonify
from flask_restful import Resource, abort

from .daily_recipes import getDailyRecipes
from .recipes import Recipe
from . import db_session


class RecipeResource(Resource):
    def get(self, recipe_id):
        abort_if_user_not_found(id)
        session = db_session.create_session()
        recipe = session.query(Recipe).get(recipe_id)
        info = recipe.to_dict()
        info["image"] = f"https://fridgex.herokuapp.com/static/img/recipe_{recipe_id}.jpg"
        return jsonify({'recipe': info})


class RecipeDailyResource(Resource):
    def get(self):
        session = db_session.create_session()
        recipes = getDailyRecipes()
        a = []
        for item in recipes:
            info = item.to_dict()
            info["image"] = f"https://fridgex.herokuapp.com/static/img/recipe_{item.id}.jpg"
            a.append(info)
        return jsonify({'recipes': a})


class RecipeCategoryResource(Resource):
    def get(self, category: str):
        session = db_session.create_session()
        recipes = session.query(Recipe).filter(Recipe.category_global == category).all()
        a = []
        for item in recipes:
            info = item.to_dict()
            info["image"] = f"https://fridgex.herokuapp.com/static/img/recipe_{item.id}.jpg"
            a.append(info)
        return jsonify({'recipes': a})


class RecipeListResource(Resource):
    def get(self):
        session = db_session.create_session()
        recipes = session.query(Recipe).all()
        a = []
        for item in recipes:
            info = item.to_dict()
            info["image"] = f"https://fridgex.herokuapp.com/static/img/recipe_{item.id}.jpg"
            a.append(info)
        return jsonify({'recipes': a})


def abort_if_user_not_found(id):
    session = db_session.create_session()
    recipe = session.query(Recipe).get(id)
    if not recipe:
        abort(404, message=f"Recipe with id = {id} not found")

