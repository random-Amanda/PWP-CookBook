"""
This file contain APIs of the cookbook application
"""
from flask import Blueprint
from flask_restful import Api

from cookbookapp.resources.review import ReviewCollection, ReviewItem
from cookbookapp.resources.user import UserCollection, UserItem
from cookbookapp.resources.ingredient import IngredientCollection, IngredientItem
from cookbookapp.resources.recipe import RecipeCollection, RecipeItem
from cookbookapp.resources.recipe_ingredient_qty import (
    RecipeIngredientQtyCollection,
    RecipeIngredientQtyItem)

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

# Add the resources to the API
# ReviewAPIs
api.add_resource(ReviewCollection, "/recipes/<recipe:recipe>/reviews/")
api.add_resource(ReviewItem, "/reviews/<review:review>/")

# User APIs
api.add_resource(UserCollection, "/users/")
api.add_resource(UserItem, "/users/<user:user>/")

# Ingredient APIs
api.add_resource(IngredientCollection, "/ingredients/")
api.add_resource(IngredientItem, "/ingredients/<ingredient:ingredient>/")

# Recipe APIs
api.add_resource(RecipeCollection, "/recipes/")
api.add_resource(RecipeItem, "/recipes/<recipe:recipe>/")

# Recipe Ingredient APIs
api.add_resource(RecipeIngredientQtyCollection, "/recipes/<recipe:recipe>/ingredients/")
api.add_resource(RecipeIngredientQtyItem,
                 "/recipes/<recipe:recipe>/ingredients/<ingredient:ingredient>/")
