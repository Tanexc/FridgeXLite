import os
import random
from flask import Flask, render_template, redirect, request
from sqlalchemy import and_

from data import db_session, recipe_resource
from data.daily_recipes import getDailyRecipes
from data.forms import SearcherForm
from data.products import Product
from data.recipes import Recipe
from flask_restful import reqparse, abort, Api, Resource


# Инициализация приложения
app = Flask(__name__)
app.config["SECRET_KEY"] = "QWav-43sd-svs3-001a"
db_sess = None
recipes = None
DAILY_RECIPES = None
CATEGORY = "all"
string_id = None


# API приложения
api = Api(app)
api.add_resource(recipe_resource.RecipeListResource, "/api/fridge-x-lite-api/recipes")
api.add_resource(recipe_resource.RecipeResource, "/api/fridge-x-lite-api/recipe/<int:user_id>")
api.add_resource(recipe_resource.RecipeDailyResource, "/api/fridge-x-lite-api/recipes/daily")
api.add_resource(recipe_resource.RecipeCategoryResource, "/api/fridge-x-lite-api/recipes/category/<string:category>")

# функция запуска приложения
def main():
    global recipes, DAILY_RECIPES, db_sess, string_id
    db_session.global_init("db/FridgeXX.db")
    db_sess = db_session.create_session()
    recipes = db_sess.query(Recipe).all()
    DAILY_RECIPES = getDailyRecipes()

    string_id = {}
    for i in range(len(recipes)):
        string_id[recipes[i].id] = str(recipes[i].id)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


# главная страница социальной сети
@app.route("/", methods=["GET"])
def base():
    return render_template("base.html", title="FridgeXWeb")


# функция для страницы рецептов
@app.route("/fridge", methods=["GET", "POST"])
def catalog():
    global DAILY_RECIPES, db_sess, string_id, CATEGORY
    try:
        form = SearcherForm()
        recipes = db_sess.query(Recipe).all()
        search_recipe = None
        print("Asasdasf")
        if request.method == "POST":
            print("SDsdvsdvsdvsdv")
            CATEGORY = request.form["submit_button"]
            title = form.title.data if form.title.data is not None else " "
            time = form.time.data if form.time.data is not None else 9999
            fats = form.fats.data if form.fats.data is not None else 9999
            carboh = form.carboh.data if form.carboh.data is not None else 9999
            protein = form.protein.data if form.protein.data is not None else 9999
            try:
                search_recipe = db_sess.query(Recipe).filter(Recipe.recipe_name == title).first()
            except:
                pass
            if CATEGORY != "all":
                recipes = db_sess.query(Recipe).filter(and_(Recipe.proteins <= protein,
                                                       Recipe.carboh <= carboh,
                                                       Recipe.fats <= fats,
                                                       Recipe.time <= time + 10,
                                                       Recipe.category_global == CATEGORY)).all()
                print("yryt")
            else:
                recipes = db_sess.query(Recipe).filter(and_(Recipe.proteins <= protein,
                                                       Recipe.carboh <= carboh,
                                                       Recipe.fats <= fats,
                                                       Recipe.time <= time + 10)
                                                       ).all()
        return render_template("catalog.html", recipes=recipes, form=form, search_recipe=search_recipe, daily_recipes=DAILY_RECIPES, string_id=string_id)
    except Exception as e:
        return redirect(f"fridge/error/{e}")


# функция для страницы выбранного рецепта
@app.route("/fridge/<id>", methods=["POST", "GET"])
def recipe(id: int):
    global db_sess
    recipe = db_sess.query(Recipe).filter(Recipe.id == id).first()
    ingr = recipe.recipe.split()
    ingredients = list(map(lambda x: db_sess.query(Product).filter(Product.id == int(x)).first().product, ingr))
    value = recipe.recipe_value.split()
    prepare = recipe.actions.split("\n")
    return render_template("recipe.html",
                           recipe=recipe,
                           ingredients=ingredients,
                           prepare=prepare,
                           id=str(recipe.id),
                           value=value)


@app.route("/fridge/error/<message>", methods=["POST", "GET"])
def error(message: str):
    return render_template("base.html",
                           error=message)


@app.route("/fridgex/get-category/<category>")
def getCategory(category: str):
    global CATEGORY
    CATEGORY = category


if __name__ == "__main__":
    main()
