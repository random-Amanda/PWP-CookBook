"""
This file contain Converters for urls
"""
import functools
import json
import bcrypt
from werkzeug.routing import BaseConverter
from werkzeug.exceptions import NotFound
from flask import request, Response, url_for
from cookbookapp.constants import (
    MASON,
    ERROR_PROFILE,
    UNSUPPORTED_MEDIA_TYPE_DESCRIPTION,
    UNSUPPORTED_MEDIA_TYPE_TITLE,
    INTERGTRITY_ERROR_ALREADY_EXISTS,
    NOT_FOUND_ERROR_TITLE,
    NOT_FOUND_ERROR_DESCRIPTION,
    VALIDATION_ERROR_INVALID_JSON_TITLE)

from cookbookapp.models import RecipeIngredientQty, Review, Ingredient, User, Recipe, ApiKey

class MasonBuilder(dict):
    """
    A convenience class for managing dictionaries that represent Mason
    objects. It provides nice shorthands for inserting some of the more
    elements into the object but mostly is just a parent for the much more
    useful subclass defined next. This class is generic in the sense that it
    does not contain any application specific implementation details.
    """

    def add_error(self, title, details):
        """
        Adds an error element to the object. Should only be used for the root
        object, and only in error scenarios.

        Note: Mason allows more than one string in the @messages property (it's
        in fact an array). However we are being lazy and supporting just one
        message.

        : param str title: Short title for the error
        : param str details: Longer human-readable description
        """

        self["@error"] = {
            "@message": title,
            "@messages": [details],
        }

    def add_namespace(self, ns, uri):
        """
        Adds a namespace element to the object. A namespace defines where our
        link relations are coming from. The URI can be an address where
        developers can find information about our link relations.

        : param str ns: the namespace prefix
        : param str uri: the identifier URI of the namespace
        """

        if "@namespaces" not in self:
            self["@namespaces"] = {}

        self["@namespaces"][ns] = {
            "name": uri
        }

    def add_control(self, ctrl_name, href, **kwargs):
        """
        Adds a control property to an object. Also adds the @controls property
        if it doesn't exist on the object yet. Technically only certain
        properties are allowed for kwargs but again we're being lazy and don't
        perform any checking.

        The allowed properties can be found from here
        https://github.com/JornWildt/Mason/blob/master/Documentation/Mason-draft-2.md

        : param str ctrl_name: name of the control (including namespace if any)
        : param str href: target URI for the control
        """

        if "@controls" not in self:
            self["@controls"] = {}

        self["@controls"][ctrl_name] = kwargs
        self["@controls"][ctrl_name]["href"] = href


class UserBuilder(MasonBuilder):
    """
    A subclass of MasonBuilder that is used to build a user object. This class
    is used to build the user object that is returned in the response.
    """

    def add_control_add_user(self):
        """
        Adds a create control property to the response object. This is used to
        build the response object that is returned in the response.
        """
        self.add_control(
            "cookbook:add-user",
            url_for("api.usercollection"),
            method="POST",
            encoding="application/json",
            title="Add a new user",
            schema=User.get_schema()
        )

    def add_control_delete_user(self, user):
        """
        Adds a delete control property to the response object. This is used to
        build the response object that is returned in the response.
        """
        self.add_control(
            "cookbook:delete-user",
            url_for("api.useritem", user=user),
            method="DELETE",
            title="Delete this user"
        )

    def add_control_update_user(self, user):
        """
        Adds a update control property to the response object. This is used to
        build the response object that is returned in the response.
        """
        self.add_control(
            "cookbook:update-user",
            url_for("api.useritem", user=user),
            method="PUT",
            encoding="application/json",
            title="Update this user",
            schema=User.get_schema()
        )

class IngredientBuilder(MasonBuilder):
    """
    A subclass of MasonBuilder that is used to build an ingredient object.
    This class is used to build the ingredient object that is returned in the
    response.
    """
    def add_control_add_ingredient(self):
        """
        Adds a create control property to the response object. This is used to
        build the response object that is returned in the response.
        """
        self.add_control(
            "cookbook:add-ingredient",
            url_for("api.ingredientcollection"),
            method="POST",
            encoding="application/json",
            title="Add a new ingredient",
            schema=Ingredient.get_schema()
        )
    def add_control_delete_ingredient(self, ingredient):
        """
        Adds a delete control property to the response object. This is used to
        build the response object that is returned in the response.
        """
        self.add_control(
            "cookbook:delete-ingredient",
            url_for("api.ingredientitem", ingredient=ingredient),
            method="DELETE",
            title="Delete this ingredient"
        )
    def add_control_update_ingredient(self, ingredient):
        """
        Adds a update control property to the response object. This is used to
        build the response object that is returned in the response.
        """
        self.add_control(
            "cookbook:update-ingredient",
            url_for("api.ingredientitem", ingredient=ingredient),
            method="PUT",
            encoding="application/json",
            title="Update this ingredient",
            schema=Ingredient.get_schema()
        )

class RecipeBuilder(MasonBuilder):
    """
    A subclass of MasonBuilder that is used to build a recipe object. This class
    is used to build the recipe object that is returned in the response.
    """
    def add_control_add_recipe(self):
        """
        Adds a create control property to the response object. This is used to
        build the response object that is returned in the response.
        """
        self.add_control(
            "cookbook:add-recipe",
            url_for("api.recipecollection"),
            method="POST",
            encoding="application/json",
            title="Add a new recipe",
            schema=Recipe.get_schema()
        )

    def add_control_delete_recipe(self, recipe):
        """
        Adds a delete control property to the response object. This is used to
        build the response object that is returned in the response.
        """
        self.add_control(
            "cookbook:delete-recipe",
            url_for("api.recipeitem", recipe=recipe),
            method="DELETE",
            title="Delete this recipe"
        )

    def add_control_update_recipe(self, recipe):
        """
        Adds a update control property to the response object. This is used to
        build the response object that is returned in the response.
        """
        self.add_control(
            "cookbook:update-recipe",
            url_for("api.recipeitem", recipe=recipe),
            method="PUT",
            encoding="application/json",
            title="Update this recipe",
            schema=Recipe.get_schema()
        )

    def add_control_add_review(self, recipe):
        """
        Adds a create control property to the response object. This is used to
        build the response object that is returned in the response.
        """
        self.add_control(
            "cookbook:add-review",
            url_for("api.reviewcollection", recipe=recipe),
            method="POST",
            encoding="application/json",
            title="Add a new review",
            schema=Review.get_schema()
        )

    def add_control_delete_review(self, review):
        """
        Adds a delete control property to the response object. This is used to
        build the response object that is returned in the response.
        """
        self.add_control(
            "cookbook:delete-review",
            url_for("api.reviewitem", review=review),
            method="DELETE",
            title="Delete this review"
        )

    def add_control_add_ingredient(self, recipe):
        """
        Adds a create control property to the response object. This is used to
        build the response object that is returned in the response.
        """
        self.add_control(
            "cookbook:add-ingredient",
            url_for("api.recipeingredientqtycollection", recipe=recipe),
            method="POST",
            encoding="application/json",
            title="Add a new ingredient",
            schema=RecipeIngredientQty.get_schema()
        )

    def add_control_delete_ingredient(self, recipe):
        """
        Adds a delete control property to the response object. This is used to
        build the response object that is returned in the response.
        """
        self.add_control(
            "cookbook:delete-ingredient",
            url_for("api.recipeingredientqtycollection", recipe=recipe),
            method="DELETE",
            encoding="application/json",
            title="Delete this ingredient",
            schema=RecipeIngredientQty.get_schema_delete()
        )

    def add_control_update_ingredient(self, recipe):
        """
        Adds a update control property to the response object. This is used to
        build the response object that is returned in the response.
        """
        self.add_control(
            "cookbook:update-ingredient",
            url_for("api.recipeingredientqtycollection", recipe=recipe),
            method="PUT",
            encoding="application/json",
            title="Update this ingredient",
            schema=RecipeIngredientQty.get_schema_update()
        )


# class ReviewBuilder(MasonBuilder):
#     """
#     A subclass of MasonBuilder that is used to build a review object. This class
#     is used to build the review object that is returned in the response.
#     """
#     def add_control_delete_review(self, review):
#         """
#         Adds a delete control property to the response object. This is used to
#         build the response object that is returned in the response.
#         """
#         self.add_control(
#             "cookbook:delete-review",
#             url_for("api.reviewitem", review=review),
#             method="DELETE",
#             title="Delete this review"
#         )


def require_admin(func):
    """
    Decorator to require admin authentication for a route.
    :param func: The function to decorate.
    :return: The decorated function.
    """
    @functools.wraps(func)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("API-KEY", "").strip()

        if not api_key:
            return Response(
                status=401,
                response=json.dumps({
                    "error": "Unauthorized",
                    "message": "Missing API key"
                }),
                mimetype=MASON
            )

        # Get the admin key from database
        db_key = ApiKey.query.filter_by(admin=True).first()

        if not db_key:
            return Response(
                status=401,
                response=json.dumps({
                    "error": "Unauthorized",
                    "message": "Admin key not configured"
                }),
                mimetype=MASON
            )

        # Hash the provided API key and compare with stored hash
        if not bcrypt.checkpw(api_key.encode('utf-8'), db_key.key):
            return Response(
                status=401,
                response=json.dumps({
                    "error": "Unauthorized",
                    "message": "Invalid API key"
                }),
                mimetype=MASON
            )

        return func(*args, **kwargs)
    return decorated_function

#Fetch the first API key from the database
def get__api_key():
    """
    Fetch the first API key from the database.
    :return: The API key if it exists, otherwise None.
    """
    api_key_entry = ApiKey.query.first()
    return api_key_entry.key if api_key_entry else None

# Error handling
def create_error_response(status_code, title, message=None):
    """
    Create a JSON error response with the given status code, title, and message.
    :param status_code: HTTP status code for the response.
    :param title: Title of the error.
    :param message: Detailed error message (optional).
    :return: Flask Response object with the error message.
    """
    resource_url = request.path
    body = MasonBuilder(resource_url=resource_url)
    body.add_error(title, message)
    body.add_control("profile", href=ERROR_PROFILE)
    return Response(json.dumps(body), status_code, mimetype=MASON)

# Create 400 Error Resonse
def create_400_error_response(error):
    """
    Create a JSON error response with a 400 status code.
    :param error: The error as a string.
    :return: Flask Response object with the error message.
    """
    return create_error_response(400,
                    VALIDATION_ERROR_INVALID_JSON_TITLE,
                    error)

# Create 415 Error Resonse
def create_415_error_response():
    """
    Create a JSON error response with a 415 status code.
    :return: Flask Response object with the error message.
    """
    return create_error_response(415,
                UNSUPPORTED_MEDIA_TYPE_TITLE,
                UNSUPPORTED_MEDIA_TYPE_DESCRIPTION)

# Create 409 Error Resonse
def create_409_error_response(message):
    """
    Create a JSON error response with a 409 status code.
    :param message: The error message.
    :return: Flask Response object with the error message.
    """
    return create_error_response(
                409,
                INTERGTRITY_ERROR_ALREADY_EXISTS,
                message
            )

# Create 404 Error Resonse
def create_404_error_response(message_prefix):
    """
    Create a JSON error response with a 404 status code.
    :param message_prefix: The prefix of the error message.
    :return: Flask Response object with the error message.
    """
    return create_error_response(
                404,
                NOT_FOUND_ERROR_TITLE,
                message_prefix + NOT_FOUND_ERROR_DESCRIPTION
            )

# Converters for URL parameters

class ReviewConverter(BaseConverter):
    """
    Represents the ReviewConverter.
    """
    def to_python(self, value):
        db_review = Review.query.filter_by(review_id=value).first()
        if db_review is None:
            raise NotFound
        return db_review

    def to_url(self, value):
        return str(value)

class UserConverter(BaseConverter):
    """
    Represents the UserConverter.
    """
    def to_python(self, value):
        db_user = User.query.filter_by(username=value).first()
        if db_user is None:
            raise NotFound
        return db_user

    def to_url(self, value):
        return value.username

class IngredientConverter(BaseConverter):
    """
    Represents the IngredientConverter.
    """
    def to_python(self, value):
        db_ingredient = Ingredient.query.filter_by(name=value).first()
        if db_ingredient is None:
            raise NotFound
        return db_ingredient

    def to_url(self, value):
        if isinstance(value, str):
            return value
        return value.name

class RecipeConverter(BaseConverter):
    """
    Represents the RecipeConverter.
    """
    def to_python(self, value):
        db_recipe = Recipe.query.filter_by(recipe_id=value).first()
        if db_recipe is None:
            raise NotFound
        return db_recipe

    def to_url(self, value):
        return str(value.recipe_id)

# class RecipeIngredientQtyConverter(BaseConverter):
#     def to_python(self, value):
#         db_qty = RecipeIngredientQty.query.filter_by(qty_id=value).first()
#         if db_qty is None:
#             raise NotFound
#         return db_qty

#     def to_url(self, value):
#         return str(value.qty_id)
