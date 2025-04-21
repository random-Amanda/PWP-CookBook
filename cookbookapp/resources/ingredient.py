"""
This module contains the resources for handling ingredient related API endpoints.
"""
import json
from flask import Response, request, url_for
from flask_restful import Resource
from jsonschema import ValidationError, validate
from sqlalchemy.exc import IntegrityError
from cookbookapp import db
from cookbookapp.constants import LINK_RELATIONS_URL, MASON
from cookbookapp.models import Ingredient
from cookbookapp.utils import (
    IngredientBuilder,
    require_admin,
    create_415_error_response,
    create_400_error_response,
    create_409_error_response,
)

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
              example:
                "@namespaces":
                  cookbook:
                    name: "/cookbook/link-relations/"
                "@controls":
                  self:
                    href: "/api/ingredients/"
                  cookbook:add-ingredient:
                    method: "POST"
                    encoding: "application/json"
                    title: "Add a new ingredient"
                    href: "/api/ingredients/"
                    schema:
                      type: object
                      properties:
                        name:
                          type: string
                        description:
                          type: string
                      required:
                        - name
                items:
                  - ingredient_id: 1
                    name: "Ingredient 1"
                    description: "Description 1"
                    "@controls":
                      self:
                        href: "/api/ingredients/Ingredient 1/"
                      profile:
                        href: "/profiles/ingredient/"
                      cookbook:update-ingredient:
                        method: "PUT"
                        encoding: "application/json"
                        title: "Update this ingredient"
                        href: "/api/ingredients/Ingredient 1/"
                        schema:
                          type: object
                          properties:
                            name:
                              type: string
                            description:
                              type: string
                          required:
                            - name
                      cookbook:delete-ingredient:
                        method: "DELETE"
                        title: "Delete this ingredient"
                        href: "/api/ingredients/Ingredient 1/"
          401:
            description: Unauthorized - Invalid or missing API key
            schema:
              type: object
              properties:
                error:
                  type: string
                message:
                  type: string
        """

        body = IngredientBuilder()
        body.add_namespace("cookbook", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.ingredientcollection"))
        body.add_control_add_ingredient()
        body["items"] = []

        ingredients = Ingredient.query.all()
        for ingredient in ingredients:
            item = IngredientBuilder(ingredient.serialize())
            item.add_control("self", url_for("api.ingredientitem", ingredient=ingredient.name))
            item.add_control("profile", "/profiles/ingredient/")
            item.add_control_update_ingredient(ingredient.name)
            item.add_control_delete_ingredient(ingredient.name)
            body["items"].append(item)

        return Response(json.dumps(body), status=200, mimetype=MASON)

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
                resource_url:
                  type: string
                  description: The URL of the resource that triggered the error
                "@error":
                  type: object
                  properties:
                    "@message":
                      type: string
                      description: A short summary of the error
                    "@messages":
                      type: array
                      description: Detailed validation or system error messages
                      items:
                        type: string
                "@controls":
                  type: object
                  properties:
                    profile:
                      type: object
                      properties:
                        href:
                          type: string
          401:
            description: Unauthorized - Invalid or missing API key
            schema:
              type: object
              properties:
                error:
                  type: string
                message:
                  type: string
          409:
            description: Ingredient already exists
            schema:
              type: object
              example:
                resource_url: "/api/ingredients/"
                "@error":
                  "@message": "already exists"
                  "@messages":
                    - "Ingredient name 'Ingredient 5' is already exists."
                "@controls":
                  profile:
                    href: "/profiles/error/"
          415:
            description: Unsupported media type
            schema:
              type: object
              example:
                resource_url: "string"
                "@error":
                  "@message": "Unsupported media type"
                  "@messages":
                    - "Requests must be JSON"
                "@controls":
                  profile:
                    href: "/profiles/error/"
        """
        if not request.is_json:
            return create_415_error_response()

        try:
            validate(request.json, Ingredient.get_schema())
        except ValidationError as e:
            return create_400_error_response(str(e))

        ingredient = Ingredient(
            name=request.json["name"],
            description=request.json["description"]
        )

        try:
            db.session.add(ingredient)
            db.session.commit()
        except IntegrityError:
            return create_409_error_response(
                f"Ingredient name '{request.json['name']}' is already exists."
            )

        return Response(
            status=201,
            headers={
                "Location": url_for("api.ingredientitem", ingredient=ingredient.name)
            },
        )


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
              example:
                ingredient_id: 1
                name: "Ingredient 1"
                description: "Description 1"
                "@namespaces":
                  cookbook:
                    name: "/cookbook/link-relations/"
                "@controls":
                  self:
                    href: "/api/ingredients/Ingredient 1/"
                  profile:
                    href: "/profiles/ingredient/"
                  cookbook:update-ingredient:
                    method: "PUT"
                    encoding: "application/json"
                    title: "Update this ingredient"
                    href: "/api/ingredients/Ingredient 1/"
                    schema:
                      type: object
                      properties:
                        name:
                          type: string
                        description:
                          type: string
                      required:
                        - name
                  cookbook:delete-ingredient:
                    method: "DELETE"
                    title: "Delete this ingredient"
                    href: "/api/ingredients/Ingredient 1/"
          401:
            description: Unauthorized - Invalid or missing API key
            schema:
              type: object
              properties:
                error:
                  type: string
                message:
                  type: string
          404:
            description: Ingredient not found
        """
        body = IngredientBuilder(ingredient.serialize())
        body.add_namespace("cookbook", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.ingredientitem", ingredient=ingredient.name))
        body.add_control("profile", "/profiles/ingredient/")
        body.add_control_update_ingredient(ingredient.name)
        body.add_control_delete_ingredient(ingredient.name)

        return Response(json.dumps(body), status=200, mimetype=MASON)

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
                resource_url:
                  type: string
                  description: The URL of the resource that triggered the error
                "@error":
                  type: object
                  properties:
                    "@message":
                      type: string
                      description: A short summary of the error
                    "@messages":
                      type: array
                      description: Detailed validation or system error messages
                      items:
                        type: string
                "@controls":
                  type: object
                  properties:
                    profile:
                      type: object
                      properties:
                        href:
                          type: string
          401:
            description: Unauthorized - Invalid or missing API key
            schema:
              type: object
              properties:
                error:
                  type: string
                message:
                  type: string
          404:
            description: Ingredient not found
          415:
            description: Unsupported media type
            schema:
              type: object
              example:
                resource_url: "string"
                "@error":
                  "@message": "Unsupported media type"
                  "@messages":
                    - "Requests must be JSON"
                "@controls":
                  profile:
                    href: "/profiles/error/"
        """
        if not request.is_json:
            return create_415_error_response()

        try:
            validate(request.json, Ingredient.get_schema())
        except ValidationError as e:
            return create_400_error_response(str(e))

        ingredient.name = request.json["name"]
        ingredient.description = request.json.get("description", ingredient.description)

        try:
            db.session.commit()
        except IntegrityError:
            return create_409_error_response(
                f"Ingredient name '{request.json['name']}' is already exists."
            )
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
            schema:
              type: object
              properties:
                error:
                  type: string
                message:
                  type: string
          404:
            description: Ingredient not found
        """
        db.session.delete(ingredient)
        db.session.commit()
        return Response(json.dumps({"message": "Ingredient deleted"}), status=204)
