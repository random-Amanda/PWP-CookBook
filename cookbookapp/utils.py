"""
This file contain Converters for urls
"""
from werkzeug.routing import BaseConverter
from werkzeug.exceptions import NotFound

from cookbookapp.models import Review, Ingredient, User, Recipe, RecipeIngredientQty

class ReviewConverter(BaseConverter):
    """
    Represents the ReviewConverter.
    """
    def to_python(self, value):
        db_review = Review.query.filter_by(review_id=value).first()
        if db_review is None:
            raise NotFound
        return db_review

    def to_url(self, value):
        return str(value)

class UserConverter(BaseConverter):
    """
    Represents the UserConverter.
    """
    def to_python(self, value):
        db_user = User.query.filter_by(username=value).first()
        if db_user is None:
            raise NotFound
        return db_user

    def to_url(self, value):
        return value.username

class IngredientConverter(BaseConverter):
    """
    Represents the IngredientConverter.
    """
    def to_python(self, value):
        db_ingredient = Ingredient.query.filter_by(name=value).first()
        if db_ingredient is None:
            raise NotFound
        return db_ingredient

    def to_url(self, value):
        if isinstance(value, str):
            return value
        return value.name

class RecipeConverter(BaseConverter):
    """
    Represents the RecipeConverter.
    """
    def to_python(self, value):
        db_recipe = Recipe.query.filter_by(recipe_id=value).first()
        if db_recipe is None:
            raise NotFound
        return db_recipe

    def to_url(self, value):
        return str(value.recipe_id)

class RecipeIngredientQtyConverter(BaseConverter):
    def to_python(self, value):
        db_qty = RecipeIngredientQty.query.filter_by(qty_id=value).first()
        if db_qty is None:
            raise NotFound
        return db_qty

    def to_url(self, value):
        return str(value.qty_id)
