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
                error:
                  type: object
                  properties:
                    title:
                      type: string
                    description:
                      type: string
          401:
            description: Unauthorized - Invalid or missing API key
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
          - in: path
            name: ingredient
            required: true
            type: string
            description: Ingredient name to update
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - qty
                - metric
              properties:
                qty:
                  type: number
                  description: New quantity of the ingredient
                metric:
                  type: string
                  description: New unit of measurement
        responses:
          204:
            description: Recipe ingredient updated successfully
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
          - in: path
            name: ingredient
            required: true
            type: string
            description: Name of the ingredient
        responses:
          204:
            description: Recipe ingredient deleted successfully
          401:
            description: Unauthorized - Invalid or missing API key
          404:
            description: Recipe ingredient not found
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
