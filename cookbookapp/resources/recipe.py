import json
import logging
from flask_restful import Resource
from flask import Response, request, url_for
from jsonschema import ValidationError, validate
from cookbookapp import db
from sqlalchemy.exc import IntegrityError
from cookbookapp.models import Recipe

logging.basicConfig(level=logging.INFO)

class RecipeCollection(Resource):
    def get(self):
        body = {"items": []}
        # body["self_uri"] = url_for("api.recipecollection")
        # body["name"] = "Recipe Collection"
        # body["description"] = "A collection of recipes"

        # body["controls"] = {
        #     "create_recipe": {"method": "POST", "href": url_for("api.recipecollection"), "title": "Create a new recipe", "schema": Recipe.get_schema()},
        #     "search_recipe": {"method": "GET", "href": "/api/recipes/search", "title": "Search for recipes"} # not implemented
        # }

        recipes = Recipe.query.all()
        for recipe in recipes:

            item = recipe.serialize()
            # item["controls"] = {
            #     "self": {"method": "GET", "href": url_for("api.recipeitem", recipe=recipe.recipe_id), "title": "Recipe details"},
            #     "update": {"method": "PUT", "href": url_for("api.recipeitem", recipe=recipe.recipe_id), "title": "Update recipe", "schema": Recipe.get_schema()}, # for refference
            #     "delete": {"method": "DELETE", "href": url_for("api.recipeitem", recipe=recipe.recipe_id), "title": "Delete recipe"} # for refference
            # }

            body["items"].append(item)

        return Response(json.dumps(body), status=200, mimetype="application/json")

    def post(self):
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
        try:
            db.session.commit()
        except IntegrityError as e:
            body = {
                "error": {
                    "title": "Integrity Error",
                    "description": str(e)
                }
            }
            return Response(json.dumps(body), status=409, mimetype="application/json")

        return Response(status=201, headers={
            "Location": url_for("api.recipeitem", recipe=recipe)
        })
    
class RecipeItem(Resource):
    def get(self, recipe):
        body = recipe.serialize()
        # body["controls"] = {
        #     "recipe:update": {"method": "PUT", "href": url_for("api.recipeitem", recipe=recipe.recipe_id), "title": "Update recipe", "schema": Recipe.get_schema()},
        #     "recipe:delete": {"method": "DELETE", "href": url_for("api.recipeitem", recipe=recipe.recipe_id), "title": "Delete recipe"},
        #     "collection": {"method": "GET", "href": url_for("api.recipecollection"), "title": "Recipes collection"}
        # }

        return Response(json.dumps(body), status=200, mimetype="application/json")
    
    def put(self, recipe):
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

        try:
            db.session.commit()
        except IntegrityError as e:
            body = {
                "error": {
                    "title": "Integrity Error",
                    "description": str(e)
                }
            }
            return Response(json.dumps(body), status=409, mimetype="application/json")
        
        return Response(status=204, mimetype="application/json")

    def delete(self, recipe):
        db.session.delete(recipe)
        db.session.commit()
        return {"message": "Recipe deleted"}, 204
    