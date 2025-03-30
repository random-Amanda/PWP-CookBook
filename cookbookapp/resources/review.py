"""
This module contains the resources for handling review-related API endpoints.
"""
import json
import logging
from flask_restful import Resource
from flask import Response, request
from jsonschema import ValidationError, validate
from cookbookapp import db, cache
from cookbookapp.constants import (
    UNSUPPORTED_MEDIA_TYPE_DESCRIPTION,
    UNSUPPORTED_MEDIA_TYPE_TITLE,
    VALIDATION_ERROR_INVALID_JSON_TITLE)
from cookbookapp.models import Review
from cookbookapp.utils import create_error_response, require_admin

logging.basicConfig(level=logging.INFO)

class ReviewCollection(Resource):
    """
    Represents a collection of reviews.
    """
    @require_admin
    def post(self, recipe):
        """
        Handle POST requests to create a new review.
        """
        if not request.is_json:
            return create_error_response(
                415,
                UNSUPPORTED_MEDIA_TYPE_TITLE,
                UNSUPPORTED_MEDIA_TYPE_DESCRIPTION
            )

        try:
            validate(request.json, Review.get_schema())
        except ValidationError as e:
            return create_error_response(
                400,
                VALIDATION_ERROR_INVALID_JSON_TITLE,
                str(e)
            )

        review = Review(
            rating=request.json["rating"],
            user_id=request.json.get("user_id"),
            recipe_id=recipe.recipe_id,
            feedback=request.json.get("feedback")
        )

        db.session.add(review)
        db.session.commit()

        cache.delete('recipes_all')

        return Response(status=201, headers={
            "Location": ""
        })

class ReviewItem(Resource):
    """
    Represents a single review.
    """
    @require_admin
    def delete(self, review):
        """
        Handle DELETE requests to delete a review.
        """
        review = Review.query.get_or_404(review.review_id)
        db.session.delete(review)
        db.session.commit()

        cache.delete('recipes_all')

        return Response(json.dumps({"message": "Review deleted"}), status=204)
