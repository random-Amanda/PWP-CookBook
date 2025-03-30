"""
This module contains the resources for handling recipe related API endpoints.
"""
import json
import logging
from flask_restful import Resource
from flask import Response, request, url_for
from jsonschema import ValidationError, validate
from cookbookapp import db, cache
from cookbookapp.constants import (
    LINK_RELATIONS_URL,
    UNSUPPORTED_MEDIA_TYPE_DESCRIPTION,
    UNSUPPORTED_MEDIA_TYPE_TITLE,
    VALIDATION_ERROR_INVALID_JSON_TITLE)
from cookbookapp.models import Recipe
from cookbookapp.utils import RecipeBuilder, create_error_response, require_admin

logging.basicConfig(level=logging.INFO)

class RecipeCollection(Resource):
    """
    Represents a collection of recipe.
    """
    @require_admin
    @cache.cached(timeout=300, key_prefix='recipes_all')
    def get(self):
        """
        Get all recipes
        ---
        tags:
          - recipes
        summary: Retrieve all recipes
        description: Returns a list of all recipes in the system. Requires admin API key.
        security:
          - ApiKeyAuth: []
        responses:
          200:
            description: List of recipes retrieved successfully
            schema:
              type: object
              properties:
                items:
                  type: array
                  items:
                    type: object
                    properties:
                      recipe_id:
                        type: integer
                        description: Unique identifier for the recipe
                      user_id:
                        type: integer
                        description: ID of the user who created the recipe
                      title:
                        type: string
                        description: Title of the recipe
                      description:
                        type: string
                        description: Description of the recipe
                      steps:
                        type: string
                        description: Cooking steps in JSON format
                      preparation_time:
                        type: string
                        description: Time required for preparation
                      cooking_time:
                        type: string
                        description: Time required for cooking
                      serving:
                        type: integer
                        description: Number of servings
                      recipeIngredient:
                        type: array
                        description: List of ingredients with quantities
                        items:
                          type: object
                          properties:
                            ingredient_id:
                              type: integer
                            ingredient:
                              type: string
                            qty:
                              type: number
                            metric:
                              type: string
                      reviews:
                        type: array
                        description: List of reviews for the recipe
                        items:
                          type: object
                          properties:
                            review_id:
                              type: integer
                            rating:
                              type: integer
                            feedback:
                              type: string
                            user:
                              type: string
          401:
            description: Unauthorized - Invalid or missing API key
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: Error message
        """

        body = RecipeBuilder()
        body.add_namespace("cookbook", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.recipecollection"))
        body.add_control_add_recipe()
        body["items"] = []

        recipes = Recipe.query.all()
        for recipe in recipes:
            item = RecipeBuilder(recipe.serialize())
            item.add_control("self", url_for("api.recipeitem", recipe=recipe))
            item.add_control("profile", "/profiles/recipe/")
            item.add_control_update_recipe(recipe)
            item.add_control_delete_recipe(recipe)
            body["items"].append(item)

        return Response(json.dumps(body), status=200, mimetype="application/json")

    @require_admin
    def post(self):
        """
        Create a new recipe
        ---
        tags:
          - recipes
        summary: Create a new recipe
        description: Creates a new recipe in the system. Requires admin API key.
        security:
          - ApiKeyAuth: []
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - title
                - steps
                - preparation_time
                - cooking_time
                - serving
              properties:
                user_id:
                  type: integer
                  description: ID of the user creating the recipe
                title:
                  type: string
                  description: Title of the recipe
                description:
                  type: string
                  description: Description of the recipe
                steps:
                  type: string
                  description: Cooking steps in JSON format
                preparation_time:
                  type: string
                  description: Time required for preparation
                cooking_time:
                  type: string
                  description: Time required for cooking
                serving:
                  type: integer
                  description: Number of servings
        responses:
          201:
            description: Recipe created successfully
            headers:
              Location:
                type: string
                description: URL of the newly created recipe
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
            validate(request.json, Recipe.get_schema())
        except ValidationError as e:
            return create_error_response(
                400,
                VALIDATION_ERROR_INVALID_JSON_TITLE,
                str(e)
            )

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
        Get a single recipe
        ---
        tags:
          - recipes
        summary: Retrieve a single recipe
        description: Returns details of a specific recipe. Requires admin API key.
        security:
          - ApiKeyAuth: []
        parameters:
          - in: path
            name: recipe
            required: true
            type: integer
            description: ID of the recipe to retrieve
        responses:
          200:
            description: Recipe retrieved successfully
            schema:
              type: object
              properties:
                recipe_id:
                  type: integer
                  description: Unique identifier for the recipe
                user_id:
                  type: integer
                  description: ID of the user who created the recipe
                title:
                  type: string
                  description: Title of the recipe
                description:
                  type: string
                  description: Description of the recipe
                steps:
                  type: string
                  description: Cooking steps in JSON format
                preparation_time:
                  type: string
                  description: Time required for preparation
                cooking_time:
                  type: string
                  description: Time required for cooking
                serving:
                  type: integer
                  description: Number of servings
                recipeIngredient:
                  type: array
                  description: List of ingredients with quantities
                  items:
                    type: object
                    properties:
                      ingredient_id:
                        type: integer
                      ingredient:
                        type: string
                      qty:
                        type: number
                      metric:
                        type: string
                reviews:
                  type: array
                  description: List of reviews for the recipe
                  items:
                    type: object
                    properties:
                      review_id:
                        type: integer
                      rating:
                        type: integer
                      feedback:
                        type: string
                      user:
                        type: string
          401:
            description: Unauthorized - Invalid or missing API key
          404:
            description: Recipe not found
        """
        body = RecipeBuilder(recipe.serialize())
        body.add_namespace("cookbook", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.recipeitem", recipe=recipe))
        body.add_control("profile", "/profiles/recipe/")
        body.add_control_update_recipe(recipe)
        body.add_control_delete_recipe(recipe)

        body.add_control_add_review(recipe)
        reviews = recipe.reviews
        body["reviews"] = []
        for review in reviews:
            item = RecipeBuilder(review.serialize())
            item.add_control("self", url_for("api.reviewitem", review=review.review_id))
            item.add_control("profile", "/profiles/review/")
            item.add_control_add_review(recipe)
            item.add_control_delete_review(review.review_id)
            body["reviews"].append(item)

        body.add_control_add_ingredient(recipe)
        recipe_ingredients = recipe.recipeIngredient
        body["recipeIngredients"] = []
        for recipe_ingredient in recipe_ingredients:
            item = RecipeBuilder(recipe_ingredient.serialize())
            item.add_control("self",
                             url_for("api.recipeingredientqtycollection",
                                     recipe=recipe))
            item.add_control("profile", "/profiles/recipeingredient/")
            item.add_control_update_ingredient(recipe)
            item.add_control_delete_ingredient(recipe)
            body["recipeIngredients"].append(item)

        return Response(json.dumps(body), status=200, mimetype="application/json")

    @require_admin
    def put(self, recipe):
        """
        Update a recipe
        ---
        tags:
          - recipes
        summary: Update a recipe
        description: Updates an existing recipe. Requires admin API key.
        security:
          - ApiKeyAuth: []
        parameters:
          - in: path
            name: recipe
            required: true
            type: integer
            description: ID of the recipe to update
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - title
                - steps
                - preparation_time
                - cooking_time
                - serving
              properties:
                title:
                  type: string
                  description: New title of the recipe
                description:
                  type: string
                  description: New description of the recipe
                steps:
                  type: string
                  description: New cooking steps in JSON format
                preparation_time:
                  type: string
                  description: New preparation time
                cooking_time:
                  type: string
                  description: New cooking time
                serving:
                  type: integer
                  description: New number of servings
        responses:
          204:
            description: Recipe updated successfully
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
            description: Recipe not found
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
            validate(request.json, Recipe.get_schema())
        except ValidationError as e:
            return create_error_response(
                400,
                VALIDATION_ERROR_INVALID_JSON_TITLE,
                str(e)
            )

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
