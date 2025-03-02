import json
import logging
from flask_restful import Resource
from flask import Response, request, url_for
from jsonschema import ValidationError, validate
from cookbookapp import db
from sqlalchemy.exc import IntegrityError
from cookbookapp.models import RecipeIngredientQty

logging.basicConfig(level=logging.INFO)

class IngredientQtyCollection(Resource):
    def get(self):
        body = {"items": []}
        # body["self_uri"] = url_for("api.ingredientqtycollection")
        # body["name"] = "Recipe Ingredient Qty Collection"
        # body["description"] = "A collection of recipe ingredient quantities"

        # body["controls"] = {
        #     "create_recipe_ingredient_qty": {"method": "POST", "href": url_for("api.ingredientqtycollection"), "title": "Create a new recipe ingredient quantity", "schema": RecipeIngredientQty.get_schema()},
        #     "search_recipe_ingredient_qty": {"method": "GET", "href": "/api/ingredientqty/search", "title": "Search for recipes"} # not implemented
        # }

        ingreQtys = RecipeIngredientQty.query.all()
        for ingreQty in ingreQtys:
            
            item = ingreQty.serialize()
            # item["controls"] = {
            #     "self": {"method": "GET", "href": url_for("api.ingredientqtyitem", ingredientqty=ingredientqty.qty_id), "title": "Recipe Ingredient Quantity details"},
            #     "update": {"method": "PUT", "href": url_for("api.ingredientqtyitem", ingredientqty=ingredientqty.qty_id), "title": "Update recipe ingredient quantity", "schema": RecipeIngredientQty.get_schema()}, # for reference
            #     "delete": {"method": "DELETE", "href": url_for("api.ingredientqtyitem", ingredientqty=ingredientqty.qty_id), "title": "Delete recipe ingredient quantity"} # for reference
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
            validate(request.json, RecipeIngredientQty.get_schema())
        except ValidationError as e:
            body = {
                "error": {
                    "title": "Invalid JSON document",
                    "description": str(e)
                }
            }
            return Response(json.dumps(body), status=400, mimetype="application/json")

        ingredientqty = RecipeIngredientQty(
            recipe_id=request.json["recipe_id"],
            ingredient_id=request.json["ingredient_id"],
            qty=request.json["qty"],
            metric=request.json["metric"]
        )

        try:
            db.session.add(ingredientqty)
            db.session.commit()
        except IntegrityError:
            body = {
                "error": {
                    "title": "Integrity Error",
                    "description": "Recipe Ingredient Quantity already exists"
                }
            }
            return Response(json.dumps(body), status=409, mimetype="application/json")
        
        return Response(status=201, headers={
            "Location": url_for("api.ingredientqtyitem", ingredientqty=ingredientqty)
        })
    
class IngredientQtyItem(Resource):
    def get(self, ingredientqty):
        body = ingredientqty.serialize()
        # body["controls"] = {
        #     "ingredientqty:update": {"method": "PUT", "href": url_for("api.ingredientqtyitem", ingredientqty=ingredientqty.qty_id), "title": "Update recipe ingredient quantity", "schema": RecipeIngredientQty.get_schema()},
        #     "ingredientqty:delete": {"method": "DELETE", "href": url_for("api.ingredientqtyitem", ingredientqty=ingredientqty.qty_id), "title": "Delete recipe ingredient quantity"}
        # }
        return Response(json.dumps(body), status=200, mimetype="application/json")

    def put(self, ingredientqty):
        if not request.is_json:
            body = { 
                "error": {
                    "title": "Unsupported media type",
                    "description": "Requests must be JSON"
                }
            }
            return Response(json.dumps(body), status=415, mimetype="application/json")
    
        try:
            validate(request.json, RecipeIngredientQty.get_schema())
        except ValidationError as e:
            body = {
                "error": {
                    "title": "Invalid JSON document",
                    "description": str(e)
                }
            }
            return Response(json.dumps(body), status=400, mimetype="application/json")
        
        #ingredientqty.qty_id = request.json["qty_id"]
        ingredientqty.recipe_id = request.json["recipe_id"]
        ingredientqty.ingredient_id = request.json["ingredient_id"]
        ingredientqty.qty = request.json["qty"]
        ingredientqty.metric = request.json["metric"]

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
        
        return Response(status=204)
    
    def delete(self, ingredientqty):
        db.session.delete(ingredientqty)
        db.session.commit()
        return {"message": "Recipe Ingredient Qty deleted"}, 204

