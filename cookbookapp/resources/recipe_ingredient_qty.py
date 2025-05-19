"""
This module contains the resources for handling recipe-ingredient related API endpoints.
"""
import json
import logging
from flask_restful import Resource
from flask import Response, request
from jsonschema import ValidationError, validate
from cookbookapp import db, cache
from cookbookapp.models import RecipeIngredientQty
from cookbookapp.utils import (
    create_415_error_response,
    create_400_error_response,
    create_404_error_response,
    require_admin,
)

logging.basicConfig(level=logging.INFO)

class RecipeIngredientQtyCollection(Resource):
    """
    Represents a collection of recipe-ingredients.
    """
    @require_admin
    def post(self, recipe):
        """
        Create a new recipe-ingredient quantity
        ---
        tags:
          - recipe-ingredients
        summary: Add an ingredient to a recipe
        description: Adds a new ingredient with quantity to a specific recipe. Requires admin API key.
        security:
          - ApiKeyAuth: []
        parameters:
          - in: path
            name: recipe
            required: true
            type: string
            description: Recipe ID to add ingredient
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - ingredient_id
                - qty
                - metric
              properties:
                ingredient_id:
                  type: integer
                  description: ID of the ingredient to add
                qty:
                  type: number
                  description: Quantity of the ingredient
                metric:
                  type: string
                  description: Unit of measurement (defaults to "g")
        responses:
          201:
            description: Recipe ingredient added successfully
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
            validate(request.json, RecipeIngredientQty.get_schema())
        except ValidationError as e:
            return create_400_error_response(str(e))

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
        Update a recipe ingredient quantity
        ---
        tags:
          - recipe-ingredients
        summary: Update ingredient quantity in a recipe
        description: Updates the quantity and metric of an ingredient in a specific recipe. Requires admin API key.
        security:
          - ApiKeyAuth: []
        parameters:
          - in: path
            name: recipe
            required: true
            type: string
            description: Recipe ID containing the ingredient
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - ingredient_id
                - qty
                - metric
              properties:
                ingredient_id:
                  type: integer
                  description: ID of the ingredient to add
                qty:
                  type: number
                  description: Quantity of the ingredient
                metric:
                  type: string
                  description: Unit of measurement (defaults to "g")
        responses:
          204:
            description: Recipe ingredient updated successfully
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
            validate(request.json, RecipeIngredientQty.get_schema())
        except ValidationError as e:
            return create_400_error_response(str(e))

        ingredient_id=request.json["ingredient_id"]

        ingredientqty = RecipeIngredientQty.query.filter_by(
            recipe_id=recipe.recipe_id ,ingredient_id=ingredient_id).first()
        
        if not ingredientqty:
            return create_404_error_response(
                "Recipe Ingredient "
                )

        ingredientqty.qty = request.json["qty"]
        ingredientqty.metric = request.json["metric"]

        db.session.commit()

        cache.delete('recipes_all')

        return Response(status=204)

    @require_admin
    def delete(self, recipe):
        """
        Delete a recipe ingredient quantity
        ---
        tags:
          - recipe-ingredients
        summary: Remove an ingredient from a recipe
        description: Removes an ingredient and its quantity from a specific recipe. Requires admin API key.
        security:
          - ApiKeyAuth: []
        parameters:
          - in: path
            name: recipe
            required: true
            type: string
            description: Recipe ID containing the ingredient
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - ingredient_id
              properties:
                ingredient_id:
                  type: integer
                  description: ID of the ingredient to delete
        responses:
          204:
            description: Recipe ingredient deleted successfully
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
            description: Recipe ingredient not found
            schema:
              type: object
              example:
                  resource_url: "/api/recipes/4/ingredients/"
                  "@error":
                    "@message": "Not Found"
                    "@messages":
                      - "Recipe Ingredient Quantity resource not found"
                  "@controls":
                    profile:
                      href: "/profiles/error/"

        """
        ingredient_id=request.json["ingredient_id"]
        ingredientqty = RecipeIngredientQty.query.filter_by(
            recipe_id=recipe.recipe_id ,ingredient_id=ingredient_id).first()
        if not ingredientqty:
            return create_404_error_response(
                "Recipe Ingredient Quantity "
                )
        db.session.delete(ingredientqty)
        db.session.commit()

        cache.delete('recipes_all')
        
        return Response(json.dumps({"message": "Recipe Ingredient Qty deleted"}), status=204)
