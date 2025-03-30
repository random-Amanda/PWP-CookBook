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
        Create a new review
        ---
        tags:
          - reviews
        summary: Add a review to a recipe
        description: Creates a new review for a specific recipe. Requires admin API key.
        security:
          - ApiKeyAuth: []
        parameters:
          - in: path
            name: recipe
            required: true
            type: string
            description: Recipe ID to add review to
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - rating
              properties:
                rating:
                  type: integer
                  description: Rating given to the recipe (1-5)
                user_id:
                  type: integer
                  description: ID of the user giving the review
                feedback:
                  type: string
                  description: Text feedback about the recipe
        responses:
          201:
            description: Review created successfully
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
        Delete a review
        ---
        tags:
          - reviews
        summary: Delete a review
        description: Deletes a specific review. Requires admin API key.
        security:
          - ApiKeyAuth: []
        parameters:
          - in: path
            name: review
            required: true
            type: string
            description: Review ID to delete
        responses:
          204:
            description: Review deleted successfully
          401:
            description: Unauthorized - Invalid or missing API key
          404:
            description: Review not found
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
        review = Review.query.get_or_404(review.review_id)
        db.session.delete(review)
        db.session.commit()

        cache.delete('recipes_all')

        return Response(json.dumps({"message": "Review deleted"}), status=204)
