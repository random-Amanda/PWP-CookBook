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
    MASON)
from cookbookapp.models import Recipe
from cookbookapp.utils import (
    RecipeBuilder,
    create_415_error_response,
    create_400_error_response,
    require_admin,
)

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
              example:
                "@namespaces":
                  cookbook:
                    name: "/cookbook/link-relations/"
                "@controls":
                  self:
                    href: "/api/recipes/"
                  cookbook:add-recipe:
                    method: "POST"
                    encoding: "application/json"
                    title: "Add a new recipe"
                    schema:
                      type: object
                      properties:
                        user_id:
                          type: integer
                        title:
                          type: string
                        description:
                          type: string
                        steps:
                          type: string
                        preparation_time:
                          type: string
                        cooking_time:
                          type: string
                        serving:
                          type: integer
                      required:
                        - title
                        - steps
                        - preparation_time
                        - cooking_time
                        - serving
                    href: "/api/recipes/"
                items:
                  - recipe_id: 1
                    user_id: 1
                    title: "Recipe 1"
                    description: "Description 1"
                    steps: "{\'step1\': \'step 1\', \'step2\': \'step 2\'}"
                    preparation_time: "10 mins"
                    cooking_time: "20 mins"
                    serving: 2
                    recipeIngredients:
                      - ingredient_id: 1
                        ingredient: "Ingredient 1"
                        qty: 100
                        metric: "g"
                      - ingredient_id: 2
                        ingredient: "Ingredient 2"
                        qty: 200
                        metric: "g"
                    reviews:
                      - review_id: 1
                        rating: 5
                        feedback: "Feedback 1"
                        user: "user1"
                    "@controls":
                      self:
                        href: "/api/recipes/1/"
                      profile:
                        href: "/profiles/recipe/"
                      cookbook:update-recipe:
                        method: "PUT"
                        encoding: "application/json"
                        title: "Update this recipe"
                        schema:
                          type: object
                          properties:
                            user_id:
                              type: integer
                            title:
                              type: string
                            description:
                              type: string
                            steps:
                              type: string
                            preparation_time:
                              type: string
                            cooking_time:
                              type: string
                            serving:
                              type: integer
                          required:
                            - title
                            - steps
                            - preparation_time
                            - cooking_time
                            - serving
                        href: "/api/recipes/1/"
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
            body["items"].append(item)

        return Response(json.dumps(body), status=200, mimetype=MASON)

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
            validate(request.json, Recipe.get_schema())
        except ValidationError as e:
            return create_400_error_response(str(e))

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
              example:
                recipe_id: 1
                user_id: 1
                title: "Recipe 1"
                description: "Description 1"
                steps: "{\'step1\': \'step 1\', \'step2\': \'step 2\'}"
                preparation_time: "10 mins"
                cooking_time: "20 mins"
                serving: 2
                recipeIngredients:
                  - recipe_id: 1
                    ingredient_id: 1
                    qty: 100
                    metric: "g"
                    "@controls":
                      self:
                        href: "/api/recipes/1/ingredients/"
                      profile:
                        href: "/profiles/recipeingredient/"
                      cookbook:update-ingredient:
                        method: "PUT"
                        encoding: "application/json"
                        title: "Update this ingredient"
                        schema:
                          type: object
                          properties:
                            ingredient_id:
                              type: integer
                            qty:
                              type: number
                            metric:
                              type: string
                          required:
                            - ingredient_id
                            - qty
                            - metric
                        href: "/api/recipes/1/ingredients/"
                      cookbook:delete-ingredient:
                        method: "DELETE"
                        title: "Delete this ingredient"
                        schema:
                          type: object
                          properties:
                            ingredient_id:
                              type: integer
                          required:
                            - ingredient_id
                        href: "/api/recipes/1/ingredients/"
                reviews:
                  - review_id: 1
                    user_id: 1
                    recipe_id: 1
                    rating: 5
                    feedback: "Feedback 1"
                    "@controls":
                      self:
                        href: "/api/reviews/1/"
                      profile:
                        href: "/profiles/review/"
                      cookbook:add-review:
                        method: "POST"
                        encoding: "application/json"
                        title: "Add a new review"
                        schema:
                          type: object
                          properties:
                            user_id:
                              type: integer
                            rating:
                              type: integer
                            feedback:
                              type: string
                          required:
                            - rating
                        href: "/api/recipes/1/reviews/"
                      cookbook:delete-review:
                        method: "DELETE"
                        title: "Delete this review"
                        href: "/api/reviews/1/"
                "@namespaces":
                  cookbook:
                    name: "/cookbook/link-relations/"
                "@controls":
                  self:
                    href: "/api/recipes/1/"
                  profile:
                    href: "/profiles/recipe/"
                  cookbook:update-recipe:
                    method: "PUT"
                    encoding: "application/json"
                    title: "Update this recipe"
                    schema:
                      type: object
                      properties:
                        user_id:
                          type: integer
                        title:
                          type: string
                        description:
                          type: string
                        steps:
                          type: string
                        preparation_time:
                          type: string
                        cooking_time:
                          type: string
                        serving:
                          type: integer
                      required:
                        - title
                        - steps
                        - preparation_time
                        - cooking_time
                        - serving
                    href: "/api/recipes/1/"
                  cookbook:add-review:
                    method: "POST"
                    encoding: "application/json"
                    title: "Add a new review"
                    schema:
                      type: object
                      properties:
                        user_id:
                          type: integer
                        rating:
                          type: integer
                        feedback:
                          type: string
                      required:
                        - rating
                    href: "/api/recipes/1/reviews/"
                  cookbook:add-ingredient:
                    method: "POST"
                    encoding: "application/json"
                    title: "Add a new ingredient"
                    schema:
                      type: object
                      properties:
                        ingredient_id:
                          type: integer
                        qty:
                          type: number
                        metric:
                          type: string
                      required:
                        - qty
                        - metric
                    href: "/api/recipes/1/ingredients/"
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
            description: Recipe not found
        """
        body = RecipeBuilder(recipe.serialize())
        body.add_namespace("cookbook", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.recipeitem", recipe=recipe))
        body.add_control("profile", "/profiles/recipe/")
        body.add_control_update_recipe(recipe)

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

        return Response(json.dumps(body), status=200, mimetype=MASON)

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
            description: Recipe not found
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
            validate(request.json, Recipe.get_schema())
        except ValidationError as e:
            return create_400_error_response(str(e))

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

        return Response(status=204, mimetype=MASON)
