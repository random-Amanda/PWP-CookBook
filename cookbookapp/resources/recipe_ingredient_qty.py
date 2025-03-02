"""
This module contains the resources for handling recipe-ingredient related API endpoints.
"""
import json
import logging
from flask_restful import Resource
from flask import Response, request, url_for
from jsonschema import ValidationError, validate
from sqlalchemy.exc import IntegrityError
from cookbookapp import db
from cookbookapp.models import RecipeIngredientQty

logging.basicConfig(level=logging.INFO)

class RecipeIngredientQtyCollection(Resource):
    """
    Represents a collection of recipe-ingredients.
    """
    def post(self, recipe):
        """
        Handle POST requests to create a new recipe-ingredient.
        """
        if not request.is_json:
            body = {
                "error": {
                    "title": "Unsupported media type",
                    "description": "Requests must be JSON"
                }
            }
            return Response(json.dumps(body), status=415, mimetype="application/json")

        try:
            validate(request.json, RecipeIngredientQty.get_schema())
        except ValidationError as e:
            body = {
                "error": {
                    "title": "Invalid JSON document",
                    "description": str(e)
                }
            }
            return Response(json.dumps(body), status=400, mimetype="application/json")

        ingredientqty = RecipeIngredientQty(
            recipe_id=recipe.recipe_id,
            ingredient_id=request.json["ingredient_id"],
            qty=request.json["qty"],
            metric=request.get_json().get("metric", "g")
        )

        db.session.add(ingredientqty)
        db.session.commit()

        return Response(status=201)

class RecipeIngredientQtyItem(Resource):
    """
    Represents a single recipe ingredient.
    """
    def put(self, recipe, ingredient):
        """
        Handle GET requests to retrieve a single recipe ingredient.
        """
        if not request.is_json:
            body = {
                "error": {
                    "title": "Unsupported media type",
                    "description": "Requests must be JSON"
                }
            }
            return Response(json.dumps(body), status=415, mimetype="application/json")

        try:
            validate(request.json, RecipeIngredientQty.get_schema())
        except ValidationError as e:
            body = {
                "error": {
                    "title": "Invalid JSON document",
                    "description": str(e)
                }
            }
            return Response(json.dumps(body), status=400, mimetype="application/json")
        ingredientqty = RecipeIngredientQty.query.filter_by(
            recipe_id=recipe.recipe_id ,ingredient_id=ingredient.ingredient_id).first()

        ingredientqty.qty = request.json["qty"]
        ingredientqty.metric = request.json["metric"]

        db.session.commit()

        return Response(status=204)

    def delete(self, recipe, ingredient):
        """
        Handle DELETE requests to delete a recipe ingredient.
        """
        ingredientqty = RecipeIngredientQty.query.filter_by(
            recipe_id=recipe.recipe_id ,ingredient_id=ingredient.ingredient_id).first()
        if not ingredientqty:
            body = {
                "error": {
                    "title": "Not Found",
                    "description": "Recipe Ingredient Quantity not found"
                }
            }
            return Response(json.dumps(body), status=404, mimetype="application/json")
        db.session.delete(ingredientqty)
        db.session.commit()
        return {"message": "Recipe Ingredient Qty deleted"}, 204
