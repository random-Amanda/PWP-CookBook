"""
This module contains the resources for handling user API endpoints.
"""
import json
from flask_restful import Resource
from flask import Response, request, url_for
from jsonschema import ValidationError, validate
from sqlalchemy.exc import IntegrityError
from cookbookapp import db
from cookbookapp.models import User

class UserCollection(Resource):
    """
    Represents a collection of users.
    """
    def get(self):
        """
        Handle GET requests to retrieve all users.
        """
        body = {"items": []}
        # body["self_uri"] = "/api/users/"
        # body["name"] = "User Collection"
        # body["description"] = "A collection of users"

        # body["controls"] = {
        #     "Create_user": {"method": "POST", "href": "/api/users", "title": "Create a new user",
        # "schema": User.get_schema()},
        #     "Search_user": {"method": "GET", "href": "/api/users/search",
        # "title": "Search for users"}
        # }

        users = User.query.all()
        for user in users:

            item = user.serialize()
            # item["controls"] = {
            #     "Self": {"method": "GET", "href": url_for("api.useritem", user=user),
            #  "title": "User details"}
            # }

            body["items"].append(item)

        return Response(json.dumps(body), status=200, mimetype="application/json")

    def post(self):
        """
        Handle POST requests to create a new user."""
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

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            body = {
                "error": {
                    "title": "User already exists",
                    "description": f"A user with '{request.json['username']}' already exists."
                }
            }
            return Response(json.dumps(body), status=409, mimetype="application/json")

        return Response(status=201, headers={
            "Location": url_for("api.useritem", user=user)
        })

class UserItem(Resource):
    """
    Represents a single user."""
    def get(self, user):
        """
        Handle GET requests to retrieve a user."""
        body = user.serialize()
        # body["controls"] = {
        #     "user:update": {"method": "PUT", "href": url_for("api.useritem", user=user),
        # "title": "Update user", "schema": User.get_schema()},
        #     "user:delete": {"method": "DELETE", "href": url_for("api.useritem", user=user),
        #  "title": "Delete user"},
        #     "collection": {"method": "GET", "href": "/api/users/", "title": "Users collection"}
        # }
        return Response(json.dumps(body), status=200, mimetype="application/json")

    def put(self, user):
        """
        Handle PUT requests to update a user."""
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

        user.username = request.json["username"]
        user.email = request.json["email"]
        user.password = request.json["password"]

        try:
            db.session.commit()
            #logging.info("Database commit successful")
        except IntegrityError:
            #logging.error(f"Database commit failed: {e}")
            body = {
                "error": {
                    "title": "User already exists",
                    "description": f"A user with '{request.json['username']}' already exists."
                }
            }
            return Response(json.dumps(body), status=409, mimetype="application/json")

        return Response(status=204)

    def delete(self, user):
        """
        Handle DELETE requests to delete a user.
        """
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 204
    