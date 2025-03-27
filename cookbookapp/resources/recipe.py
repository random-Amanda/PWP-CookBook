"""
This module contains the resources for handling recipe related API endpoints.
"""
import json
import logging
from cookbookapp.utils import require_admin
from flask_restful import Resource
from flask import Response, request, url_for
from jsonschema import ValidationError, validate
from sqlalchemy.exc import IntegrityError
from cookbookapp import db, cache
from cookbookapp.models import Recipe

logging.basicConfig(level=logging.INFO)

class RecipeCollection(Resource):
    """
    Represents a collection of recipe.
    """
    @require_admin
    @cache.cached(timeout=300, key_prefix='recipes_all')
    def get(self):
        """
        Handle GET requests to retrieve all recipe.
        """
        body = {"items": []}
        recipes = Recipe.query.all()
        for recipe in recipes:
            item = recipe.serialize()
            body["items"].append(item)

        return Response(json.dumps(body), status=200, mimetype="application/json")

    @require_admin    
    def post(self):
        """
        Handle POST requests to create a new recipe.
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
            validate(request.json, Recipe.get_schema())
        except ValidationError as e:
            body = {
                "error": {
                    "title": "Invalid JSON document",
                    "description": str(e)
                }
            }
            return Response(json.dumps(body), status=400, mimetype="application/json")

        recipe = Recipe(
            user_id=request.json["user_id"],
            title=request.json["title"],
            description=request.json["description"],
            steps=request.json["steps"],
            preparation_time=request.json["preparation_time"],
            cooking_time=request.json["cooking_time"],
            serving=request.json["serving"]
        )

        db.session.add(recipe)

        db.session.commit()
        cache.delete('recipes_all')

        return Response(status=201, headers={
            "Location": url_for("api.recipeitem", recipe=recipe)
        })

class RecipeItem(Resource):
    """
    Represents a single recipe.
    """
    @require_admin
    def get(self, recipe):
        """
        Handle GET requests to retrieve a single recipe.
        """
        body = recipe.serialize()
        return Response(json.dumps(body), status=200, mimetype="application/json")

    @require_admin
    def put(self, recipe):
        """
        Handle PUT requests to update a recipe.
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
            validate(request.json, Recipe.get_schema())
        except ValidationError as e:
            body = {
                "error": {
                    "title": "Invalid JSON document",
                    "description": str(e)
                }
            }
            return Response(json.dumps(body), status=400, mimetype="application/json")

        #recipe.user_id = request.json["user_id"]
        recipe.title = request.json["title"]
        recipe.description = request.json["description"]
        recipe.steps = request.json["steps"]
        recipe.preparation_time = request.json["preparation_time"]
        recipe.cooking_time = request.json["cooking_time"]
        recipe.serving = request.json["serving"]

        # try:
        db.session.commit()
        cache.delete('recipes_all')

        return Response(status=204, mimetype="application/json")
