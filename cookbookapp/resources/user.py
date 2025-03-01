import json
import logging
from flask_restful import Resource, reqparse
from flask import Response, jsonify, request, url_for
from jsonschema import ValidationError, validate
from cookbookapp import db
from sqlalchemy.exc import IntegrityError
from cookbookapp.models import User

class UserCollection(Resource):
    def get(self):
        body = {"items": []}
        body["self_uri"] = "/api/users/"
        body["name"] = "User Collection"
        body["description"] = "A collection of users"

        body["controls"] = {
            "Create_user": {"method": "POST", "href": "/api/users", "title": "Create a new user", "schema": User.get_schema()},
            "Search_user": {"method": "GET", "href": "/api/users/search", "title": "Search for users"}
        }

        users = User.query.all()
        for user in users:
            
            item = user.serialize()
            item["controls"] = {
                "Self": {"method": "GET", "href": url_for("api.useritem", user=user), "title": "User details"}
            }

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
            validate(request.json, User.get_schema())
        except ValidationError as e:
            body = {
                "error": {
                    "title": "Invalid JSON document",
                    "description": str(e)
                }
            }
            return Response(json.dumps(body), status=400, mimetype="application/json")

        user = User(
            username=request.json["username"],
            email=request.json["email"],
            password=request.json["password"]
        )

        db.session.add(user)
        db.session.commit()        

        return Response(status=201, headers={
            "Location": url_for("api.useritem", user=user)
        })
    
class UserItem(Resource):
    def get(self, user):
        body = user.serialize()
        body["controls"] = {
            "user:update": {"method": "PUT", "href": url_for("api.useritem", user=user), "title": "Update user", "schema": User.get_schema()},
            "user:delete": {"method": "DELETE", "href": url_for("api.useritem", user=user), "title": "Delete user"},
            "collection": {"method": "GET", "href": "/api/users/", "title": "Users collection"}
        }
        return Response(json.dumps(body), status=200, mimetype="application/json")
    
    def put(self, user):
        if not request.is_json:
            body = { 
                "error": {
                    "title": "Unsupported media type",
                    "description": "Requests must be JSON"
                }
            }
            return Response(json.dumps(body), status=415, mimetype="application/json")

        try:
            validate(request.json, User.get_schema())
        except ValidationError as e:
            body = {
                "error": {
                    "title": "Invalid JSON document",
                    "description": str(e)
                }
            }
            return Response(json.dumps(body), status=400, mimetype="application/json")

        logging.info(f"Request JSON: {request.json}")

        user.username = request.json["username"]
        user.email = request.json["email"]
        user.password = request.json["password"]

        logging.info(f"Updated user: {user.serialize()}")

        try:
            db.session.commit()
            logging.info("Database commit successful")
        except Exception as e:
            logging.error(f"Database commit failed: {e}")
            db.session.rollback()
            body = {
                "error": {
                    "title": "Database commit failed",
                    "description": str(e)
                }
            }
            return Response(json.dumps(body), status=500, mimetype="application/json")
        
        return Response(status=204)

    
    def delete(self, user):
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 204
    