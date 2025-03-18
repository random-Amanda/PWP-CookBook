"""
This module contains the resources for handling review-related API endpoints.
"""
import json
import logging
from cookbookapp.utils import require_admin
from flask_restful import Resource
from flask import Response, request, url_for
from jsonschema import ValidationError, validate
from cookbookapp import db, cache
from cookbookapp.models import Review
from cookbookapp.resources.recipe import RecipeItem

logging.basicConfig(level=logging.INFO)

@require_admin
class ReviewCollection(Resource):
    """
    Represents a collection of reviews.
    """
    def post(self, recipe):
        """
        Handle POST requests to create a new review.
        """
        if not request.is_json:
            body = {
                "error": {
                    "title": "Unsupported media type",
                    "description": "Requests must be JSON"
                }
            }
            return Response(json.dumps(body), status=415, mimetype="application/json")

        try:
            validate(request.json, Review.get_schema())
        except ValidationError as e:
            body = {
                "error": {
                    "title": "Invalid JSON document",
                    "description": str(e)
                }
            }
            return Response(json.dumps(body), status=400, mimetype="application/json")

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

    def delete(self, review):
        """
        Handle DELETE requests to delete a review.
        """
        review = Review.query.get_or_404(review.review_id)
        db.session.delete(review)
        db.session.commit()

        cache.delete('recipes_all')

        return {"message": "Review deleted"}, 204
