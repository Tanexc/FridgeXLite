import random

from data import db_session
from data.recipes import Recipe

db_session.global_init("db/FridgeXX.db")
db_sess = db_session.create_session()


DAILY_RECIPES = None


def getDailyRecipes():
    global DAILY_RECIPES
    if DAILY_RECIPES is None:
        DAILY_RECIPES = []
        category = ["Горячие блюда", "Супы", "Салаты", "Напитки"]
        for i in range(4):
            recipes = db_sess.query(Recipe).filter(Recipe.category_global == category[i]).all()
            DAILY_RECIPES.append(recipes[random.randrange(0, len(recipes))])
    return DAILY_RECIPES