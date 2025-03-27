"""
This module contains the resources for handling ingredient related API endpoints.
"""
import json
from cookbookapp.utils import require_admin
from flask import Response, request, url_for
from flask_restful import Resource
from jsonschema import ValidationError, validate
from sqlalchemy.exc import IntegrityError
from cookbookapp import db
from cookbookapp.models import Ingredient

class IngredientCollection(Resource):
    """
    Represents a collection of ingredients.
    """
    @require_admin
    def get(self):
        """
        Handle GET requests to retrieve all ingredients.
        """
        body = {"items": []}
        ingredients = Ingredient.query.all()
        for ingredient in ingredients:
            item = ingredient.serialize()
            body["items"].append(item)

        return Response(json.dumps(body), status=200, mimetype="application/json")

    @require_admin
    def post(self):
        """
        Handle POST requests to create a new ingredient.
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
            validate(request.json, Ingredient.get_schema())
        except ValidationError as e:
            body = {
                "error": {
                    "title": "Invalid JSON document",
                    "description": str(e)
                }
            }
            return Response(json.dumps(body), status=400, mimetype="application/json")

        ingredient = Ingredient(
            name=request.json["name"],
            description=request.json["description"]
        )

        try:
            db.session.add(ingredient)
            db.session.commit()
        except IntegrityError:
            body = {
                "error": {
                    "title": "Already exists",
                    "description": f"Ingredient name '{request.json['name']}' is already exists."
                }
            }
            return Response(json.dumps(body), status=409, mimetype="application/json")

        return Response(status=201, headers={
            "Location": url_for("api.ingredientitem", ingredient=ingredient.name)
        })

class IngredientItem(Resource):
    """
    Represents a single ingredient.
    """
    @require_admin
    def get(self, ingredient):
        """
        Handle GET requests to retrieve a single ingredient.
        """
        body = ingredient.serialize()
        return Response(json.dumps(body), status=200, mimetype="application/json")

    @require_admin
    def put(self, ingredient):
        """
        Handle PUT requests to update a ingredient.
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
            validate(request.json, Ingredient.get_schema())
        except ValidationError as e:
            body = {
                "error": {
                    "title": "Invalid JSON document",
                    "description": str(e)
                }
            }
            return Response(json.dumps(body), status=400, mimetype="application/json")

        ingredient.name = request.json["name"]
        ingredient.description = request.json["description"]

        try:
            db.session.commit()
        except IntegrityError:
            body = {
                "error": {
                    "title": "Already exists",
                    "description": f"Ingredient name '{request.json['name']}' is already exists."
                }
            }
            return Response(json.dumps(body), status=409, mimetype="application/json")

        return Response(status=204)

    @require_admin
    def delete(self, ingredient):
        """
        Handle DELETE requests to delete a ingredient.
        """
        db.session.delete(ingredient)
        db.session.commit()
        return Response(status=204)
