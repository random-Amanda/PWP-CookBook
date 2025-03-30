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
        Get all users
        ---
        tags:
          - users
        summary: Retrieve all users
        description: Returns a list of all users in the system. Requires admin API key.
        security:
          - ApiKeyAuth: []
        responses:
          200:
            description: List of users retrieved successfully
            schema:
              type: object
              properties:
                items:
                  type: array
                  items:
                    type: object
                    properties:
                      user_id:
                        type: integer
                        description: Unique identifier for the user
                      username:
                        type: string
                        description: Username (unique)
                      email:
                        type: string
                        description: User's email address (unique)
                      password:
                        type: string
                        description: User's password (hashed)
          401:
            description: Unauthorized - Invalid or missing API key
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: Error message
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
        Create a new user
        ---
        tags:
          - users
        summary: Create a new user
        description: Creates a new user in the system. Requires admin API key.
        security:
          - ApiKeyAuth: []
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - username
                - email
                - password
              properties:
                username:
                  type: string
                  description: Username (must be unique)
                email:
                  type: string
                  description: Email address (must be unique)
                password:
                  type: string
                  description: User's password
        responses:
          201:
            description: User created successfully
            headers:
              Location:
                type: string
                description: URL of the newly created user
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
          409:
            description: User already exists
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
        Get a single user
        ---
        tags:
          - users
        summary: Retrieve a single user
        description: Returns details of a specific user. Requires admin API key.
        security:
          - ApiKeyAuth: []
        parameters:
          - in: path
            name: user
            required: true
            type: string
            description: Username to retrieve
        responses:
          200:
            description: User retrieved successfully
            schema:
              type: object
              properties:
                user_id:
                  type: integer
                  description: Unique identifier for the user
                username:
                  type: string
                  description: Username (unique)
                email:
                  type: string
                  description: Email address (unique)
                password:
                  type: string
                  description: User's password (hashed)
          401:
            description: Unauthorized - Invalid or missing API key
          404:
            description: User not found
        """

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
        Update a user
        ---
        tags:
          - users
        summary: Update a user
        description: Updates an existing user. Requires admin API key.
        security:
          - ApiKeyAuth: []
        parameters:
          - in: path
            name: user
            required: true
            type: string
            description: Username to update
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - username
                - email
                - password
              properties:
                username:
                  type: string
                  description: New username (must be unique)
                email:
                  type: string
                  description: New email address (must be unique)
                password:
                  type: string
                  description: New password
        responses:
          204:
            description: User updated successfully
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
            description: User not found
          409:
            description: Username already exists
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
        Delete a user
        ---
        tags:
          - users
        summary: Delete a user
        description: Deletes a specific user. Requires admin API key.
        security:
          - ApiKeyAuth: []
        parameters:
          - in: path
            name: user
            required: true
            type: string
            description: Username to delete
        responses:
          204:
            description: User deleted successfully
          401:
            description: Unauthorized - Invalid or missing API key
          404:
            description: User not found
        """
        db.session.delete(user)
        db.session.commit()
        return Response(json.dumps({"message": "User deleted"}), status=204)
