"""
This module contains the resources for handling recipe-ingredient related API endpoints.
"""
import json
import logging
from flask_restful import Resource
from flask import Response, request
from jsonschema import ValidationError, validate
from cookbookapp import db, cache
from cookbookapp.constants import (
    NOT_FOUND_ERROR_DESCRIPTION,
    NOT_FOUND_ERROR_TITLE,
    UNSUPPORTED_MEDIA_TYPE_DESCRIPTION,
    UNSUPPORTED_MEDIA_TYPE_TITLE,
    VALIDATION_ERROR_INVALID_JSON_TITLE)
from cookbookapp.models import RecipeIngredientQty
from cookbookapp.utils import create_error_response, require_admin

logging.basicConfig(level=logging.INFO)

class RecipeIngredientQtyCollection(Resource):
    """
    Represents a collection of recipe-ingredients.
    """
    @require_admin
    def post(self, recipe):
        """
        Handle POST requests to create a new recipe-ingredient.
        """
        if not request.is_json:
            return create_error_response(
                415,
                UNSUPPORTED_MEDIA_TYPE_TITLE,
                UNSUPPORTED_MEDIA_TYPE_DESCRIPTION
            )

        try:
            validate(request.json, RecipeIngredientQty.get_schema())
        except ValidationError as e:
            return create_error_response(
                400,
                VALIDATION_ERROR_INVALID_JSON_TITLE,
                str(e)
            )

        ingredientqty = RecipeIngredientQty(
            recipe_id=recipe.recipe_id,
            ingredient_id=request.json["ingredient_id"],
            qty=request.json["qty"],
            metric=request.get_json().get("metric", "g")
        )

        db.session.add(ingredientqty)
        db.session.commit()

        cache.delete('recipes_all')

        return Response(status=201)

# class RecipeIngredientQtyItem(Resource):
#     """
#     Represents a single recipe ingredient.
#     """
    @require_admin
    def put(self, recipe):
        """
        Handle GET requests to retrieve a single recipe ingredient.
        """
        if not request.is_json:
            return create_error_response(
                415,
                UNSUPPORTED_MEDIA_TYPE_TITLE,
                UNSUPPORTED_MEDIA_TYPE_DESCRIPTION
            )

        try:
            validate(request.json, RecipeIngredientQty.get_schema())
        except ValidationError as e:
            return create_error_response(
                400,
                VALIDATION_ERROR_INVALID_JSON_TITLE,
                str(e)
            )

        ingredient_id=request.json["ingredient_id"]

        ingredientqty = RecipeIngredientQty.query.filter_by(
            recipe_id=recipe.recipe_id ,ingredient_id=ingredient_id).first()

        ingredientqty.qty = request.json["qty"]
        ingredientqty.metric = request.json["metric"]

        db.session.commit()

        cache.delete('recipes_all')

        return Response(status=204)

    @require_admin
    def delete(self, recipe):
        """
        Handle DELETE requests to delete a recipe ingredient.
        """
        ingredient_id=request.json["ingredient_id"]
        ingredientqty = RecipeIngredientQty.query.filter_by(
            recipe_id=recipe.recipe_id ,ingredient_id=ingredient_id).first()
        if not ingredientqty:
            return create_error_response(
                404,
                NOT_FOUND_ERROR_TITLE,
                "Recipe Ingredient Quantity " + NOT_FOUND_ERROR_DESCRIPTION
            )
        db.session.delete(ingredientqty)
        db.session.commit()

        cache.delete('recipes_all')
        
        return Response(json.dumps({"message": "Recipe Ingredient Qty deleted"}), status=204)
