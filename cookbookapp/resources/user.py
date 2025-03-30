"""
This module contains the resources for handling user API endpoints.
"""
import json
from flask_restful import Resource
from flask import Response, request, url_for
from jsonschema import ValidationError, validate
from sqlalchemy.exc import IntegrityError
from cookbookapp import db
from cookbookapp.constants import (
    INTERGTRITY_ERROR_ALREADY_EXISTS,
    LINK_RELATIONS_URL, MASON,
    UNSUPPORTED_MEDIA_TYPE_DESCRIPTION,
    UNSUPPORTED_MEDIA_TYPE_TITLE, USER_PROFILE,
    VALIDATION_ERROR_INVALID_JSON_TITLE)
from cookbookapp.models import User
from cookbookapp.utils import UserBuilder, create_error_response, require_admin

class UserCollection(Resource):
    """
    Represents a collection of users.
    """
    @require_admin
    def get(self):
        """
        Handle GET requests to retrieve all users.
        """

        body = UserBuilder()
        body.add_namespace("cookbook", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.usercollection"))
        body.add_control_add_user()
        body["items"] = []

        users = User.query.all()
        for user in users:

            item = UserBuilder(user.serialize())
            item.add_control("self", url_for("api.useritem", user=user))
            item.add_control("profile", USER_PROFILE)
            body.add_control_update_user(user)
            body.add_control_delete_user(user)

            body["items"].append(item)

        return Response(json.dumps(body), 200, mimetype=MASON)

    @require_admin
    def post(self):
        """
        Handle POST requests to create a new user."""
        if not request.is_json:
            return create_error_response(
                415,
                UNSUPPORTED_MEDIA_TYPE_TITLE,
                UNSUPPORTED_MEDIA_TYPE_DESCRIPTION
            )

        try:
            validate(request.json, User.get_schema())
        except ValidationError as e:
            return create_error_response(
                400,
                VALIDATION_ERROR_INVALID_JSON_TITLE,
                str(e)
            )

        user = User(
            username=request.json["username"],
            email=request.json["email"],
            password=request.json["password"]
        )

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            return create_error_response(
                409,
                "User " + INTERGTRITY_ERROR_ALREADY_EXISTS,
                f"A user with '{request.json['username']}' already exists."
            )

        return Response(status=201, headers={
            "Location": url_for("api.useritem", user=user)
        })

class UserItem(Resource):
    """
    Represents a single user."""
    @require_admin
    def get(self, user):
        """
        Handle GET requests to retrieve a user."""

        body = UserBuilder(user.serialize())
        body.add_namespace("cookbook", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.useritem", user=user))
        body.add_control("profile", USER_PROFILE)
        body.add_control_update_user(user)
        body.add_control_delete_user(user)
        return Response(json.dumps(body), 200, mimetype=MASON)

    @require_admin
    def put(self, user):
        """
        Handle PUT requests to update a user."""
        if not request.is_json:
            return create_error_response(
                415,
                UNSUPPORTED_MEDIA_TYPE_TITLE,
                UNSUPPORTED_MEDIA_TYPE_DESCRIPTION
            )

        try:
            validate(request.json, User.get_schema())
        except ValidationError as e:
            return create_error_response(
                400,
                VALIDATION_ERROR_INVALID_JSON_TITLE,
                str(e)
            )

        user.username = request.json["username"]
        user.email = request.json["email"]
        user.password = request.json["password"]

        try:
            db.session.commit()
        except IntegrityError:
            return create_error_response(
                409,
                "User " + INTERGTRITY_ERROR_ALREADY_EXISTS,
                f"A user with '{request.json['username']}' already exists."
            )

        return Response(status=204)

    @require_admin
    def delete(self, user):
        """
        Handle DELETE requests to delete a user.
        """
        db.session.delete(user)
        db.session.commit()
        return Response(json.dumps({"message": "User deleted"}), status=204)
