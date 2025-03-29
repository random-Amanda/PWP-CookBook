"""
This file contain Converters for urls
"""
from werkzeug.routing import BaseConverter
from werkzeug.exceptions import NotFound
from werkzeug.exceptions import Forbidden
from flask import Flask, request, jsonify,Response
import functools
import json
import bcrypt

from cookbookapp.models import Review, Ingredient, User, Recipe, ApiKey

# The authentication key will be in "Api-Key" header
def require_admin(func):
    """
    Decorator to require API key for protected routes.
    """
    @functools.wraps(func)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("API-KEY", "").strip()
        
        if not api_key:
            return Response(
                status=401,
                response=json.dumps({
                    "error": "Unauthorized",
                    "message": "Missing API key"
                }),
                mimetype="application/json"
            )

        # Get the admin key from database
        db_key = ApiKey.query.filter_by(admin=True).first()
        
        if not db_key:
            return Response(
                status=401,
                response=json.dumps({
                    "error": "Unauthorized",
                    "message": "Admin key not configured"
                }),
                mimetype="application/json"
            )

        # Hash the provided API key and compare with stored hash
        key_hash = ApiKey.key_hash(api_key)

        # Use bcrypt.checkpw to compare the hashes
        if not bcrypt.checkpw(api_key.encode('utf-8'), db_key.key):
            return Response(
                status=401,
                response=json.dumps({
                    "error": "Unauthorized",
                    "message": "Invalid API key"
                }),
                mimetype="application/json"
            )

        return func(*args, **kwargs)
    return decorated_function

#Fetch the first API key from the database
def get__api_key():
    api_key_entry = ApiKey.query.first()
    return api_key_entry.key if api_key_entry else None

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

# class RecipeIngredientQtyConverter(BaseConverter):
#     def to_python(self, value):
#         db_qty = RecipeIngredientQty.query.filter_by(qty_id=value).first()
#         if db_qty is None:
#             raise NotFound
#         return db_qty

#     def to_url(self, value):
#         return str(value.qty_id)
