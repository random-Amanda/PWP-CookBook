from flask import Blueprint
from flask_restful import Api

from cookbookapp.resources.review import ReviewCollection, ReviewItem
from cookbookapp.resources.user import UserCollection, UserItem
from cookbookapp.resources.ingredient import IngredientCollection, IngredientItem
from cookbookapp.resources.recipe import RecipeCollection, RecipeItem
from cookbookapp.resources.recipe_ingredient_qty import IngredientQtyCollection, IngredientQtyItem

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

# Add the resources to the API
api.add_resource(ReviewCollection, "/reviews/")
api.add_resource(ReviewItem, "/reviews/<review:review>/")
api.add_resource(UserCollection, "/users/")
api.add_resource(UserItem, "/users/<user:user>/")
api.add_resource(IngredientCollection, "/ingredients/")
api.add_resource(IngredientItem, "/ingredients/<ingredient:ingredient>/")
api.add_resource(RecipeCollection, "/recipes/")
api.add_resource(RecipeItem, "/recipes/<recipe:recipe>/")
api.add_resource(IngredientQtyCollection, "/ingredientqty/")
api.add_resource(IngredientQtyItem, "/ingredientqty/<ingredientqty:ingredientqty>/")
