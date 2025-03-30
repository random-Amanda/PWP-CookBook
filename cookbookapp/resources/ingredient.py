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
        Get all ingredients
        ---
        tags:
          - ingredients
        summary: Retrieve all ingredients
        description: Returns a list of all ingredients in the system. Requires admin API key.
        security:
          - ApiKeyAuth: []
        responses:
          200:
            description: List of ingredients retrieved successfully
            schema:
              type: object
              properties:
                items:
                  type: array
                  items:
                    type: object
                    properties:
                      ingredient_id:
                        type: integer
                        description: Unique identifier for the ingredient
                      name:
                        type: string
                        description: Name of the ingredient (unique)
                      description:
                        type: string
                        description: Description of the ingredient
          401:
            description: Unauthorized - Invalid or missing API key
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: Error message
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
        Create a new ingredient
        ---
        tags:
          - ingredients
        summary: Create a new ingredient
        description: Creates a new ingredient in the system. Requires admin API key.
        security:
          - ApiKeyAuth: []
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - name
              properties:
                name:
                  type: string
                  description: Name of the ingredient (must be unique)
                description:
                  type: string
                  description: Description of the ingredient
        responses:
          201:
            description: Ingredient created successfully
            headers:
              Location:
                type: string
                description: URL of the newly created ingredient
          400:
            description: Invalid input data
            schema:
              type: object
              properties:
                error:
                  type: object
                  properties:
                    title:
                      type: string
                    description:
                      type: string
          401:
            description: Unauthorized - Invalid or missing API key
          409:
            description: Ingredient already exists
            schema:
              type: object
              properties:
                error:
                  type: object
                  properties:
                    title:
                      type: string
                    description:
                      type: string
          415:
            description: Unsupported media type
            schema:
              type: object
              properties:
                error:
                  type: object
                  properties:
                    title:
                      type: string
                    description:
                      type: string
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
        Get a single ingredient
        ---
        tags:
          - ingredients
        summary: Retrieve a single ingredient
        description: Returns details of a specific ingredient. Requires admin API key.
        security:
          - ApiKeyAuth: []
        parameters:
          - in: path
            name: ingredient
            required: true
            type: string
            description: Name of the ingredient to retrieve
        responses:
          200:
            description: Ingredient retrieved successfully
            schema:
              type: object
              properties:
                ingredient_id:
                  type: integer
                  description: Unique identifier for the ingredient
                name:
                  type: string
                  description: Name of the ingredient (unique)
                description:
                  type: string
                  description: Description of the ingredient
          401:
            description: Unauthorized - Invalid or missing API key
          404:
            description: Ingredient not found
        """
        body = ingredient.serialize()
        return Response(json.dumps(body), status=200, mimetype="application/json")

    @require_admin
    def put(self, ingredient):
        """
        Update an ingredient
        ---
        tags:
          - ingredients
        summary: Update an ingredient
        description: Updates an existing ingredient. Requires admin API key.
        security:
          - ApiKeyAuth: []
        parameters:
          - in: path
            name: ingredient
            required: true
            type: string
            description: Name of the ingredient to update
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - name
              properties:
                name:
                  type: string
                  description: New name of the ingredient (must be unique)
                description:
                  type: string
                  description: New description of the ingredient
        responses:
          204:
            description: Ingredient updated successfully
          400:
            description: Invalid input data
            schema:
              type: object
              properties:
                error:
                  type: object
                  properties:
                    title:
                      type: string
                    description:
                      type: string
          401:
            description: Unauthorized - Invalid or missing API key
          404:
            description: Ingredient not found
          409:
            description: Ingredient name already exists
            schema:
              type: object
              properties:
                error:
                  type: object
                  properties:
                    title:
                      type: string
                    description:
                      type: string
          415:
            description: Unsupported media type
            schema:
              type: object
              properties:
                error:
                  type: object
                  properties:
                    title:
                      type: string
                    description:
                      type: string
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
        Delete an ingredient
        ---
        tags:
          - ingredients
        summary: Delete an ingredient
        description: Deletes a specific ingredient. Requires admin API key.
        security:
          - ApiKeyAuth: []
        parameters:
          - in: path
            name: ingredient
            required: true
            type: string
            description: Name of the ingredient to delete
        responses:
          204:
            description: Ingredient deleted successfully
          401:
            description: Unauthorized - Invalid or missing API key
          404:
            description: Ingredient not found
        """
        db.session.delete(ingredient)
        db.session.commit()
        return Response(status=204)
