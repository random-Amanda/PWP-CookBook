"""
This module contains the resources for handling ingredient-related API endpoints.
"""
import json
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
    def get(self):
        """
        Handle GET requests to retrieve all ingredients.
        """
        body = {"items": []}
        # body["self_uri"] = url_for("api.ingredientcollection")
        # body["name"] = "Ingredient Collection"
        # body["description"] = "A collection of ingredients"
        # body["controls"] = {
        #     "create_ingredient": {"method": "POST", "href": url_for("api.ingredientcollection"),
        #                           "title": "Create a new ingredient",
        #                           "schema": Ingredient.get_schema()}
        # }

        ingredients = Ingredient.query.all()
        for ingredient in ingredients:

            item = ingredient.serialize()
            # item["controls"] = {
            #     "self": {"method": "GET", "href": url_for(
            #         "api.ingredientitem",ingredient=ingredient), "title": "Ingredient details"}
            # }

            body["items"].append(item)

        return Response(json.dumps(body), status=200, mimetype="application/json")

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
    def get(self, ingredient):
        """
        Handle GET requests to retrieve a single ingredient.
        """
        body = ingredient.serialize()
        # body["controls"] = {
        #     "ingredient:update": {"method": "PUT", "href": url_for(
        #         "api.ingredientitem", ingredient=ingredient), "title": "Update ingredient",
        #         "schema": Ingredient.get_schema()},
        #     "ingredient:delete": {"method": "DELETE", "href": url_for(
        #         "api.ingredientitem", ingredient=ingredient), "title": "Delete ingredient"},
        #     "collection": {"method": "GET", "href": url_for("api.ingredientcollection"),
        #                    "title": "Ingredients collection"},
        # }

        return Response(json.dumps(body), status=200, mimetype="application/json")

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

    def delete(self, ingredient):
        """
        Handle DELETE requests to delete a ingredient.
        """
        db.session.delete(ingredient)
        db.session.commit()
        return Response(status=204)
