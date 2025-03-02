import json
import logging
from flask_restful import Resource
from flask import Response, request, url_for
from jsonschema import ValidationError, validate
from sqlalchemy.exc import IntegrityError
from cookbookapp import db
from cookbookapp.models import Review

logging.basicConfig(level=logging.INFO)

class ReviewCollection(Resource):
    def get(self):
        body = {"items": []}
        body["self_uri"] = url_for("api.reviewcollection")
        body["name"] = "Review Collection"
        body["description"] = "A collection of reviews"

        body["controls"] = {
            "create_review": {"method": "POST", "href": url_for("api.reviewcollection"), "title": "Create a new review", "schema": Review.get_schema()},
            "search_review": {"method": "GET", "href": "/api/reviews/search", "title": "Search for reviews"} # not implemented
        }

        reviews = Review.query.all()
        for review in reviews:

            item = review.serialize()
            item["controls"] = {
                "self": {"method": "GET", "href": url_for("api.reviewitem", review=review.review_id), "title": "Review details"},
                "update": {"method": "PUT", "href": url_for("api.reviewitem", review=review.review_id), "title": "Update review", "schema": Review.get_schema()}, # for refference
                "delete": {"method": "DELETE", "href": url_for("api.reviewitem", review=review.review_id), "title": "Delete review"} # for refference
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
            recipe_id=request.json.get("recipe_id"),
            feedback=request.json.get("feedback")
        )

        db.session.add(review)
        db.session.commit()        

        return Response(status=201, headers={
            "Location": url_for("api.reviewitem", review=review.review_id)
        })

class ReviewItem(Resource):
    def get(self, review):
        body = review.serialize()
        body["controls"] = {
            "review:update": {"method": "PUT", "href": url_for("api.reviewitem", review=review.review_id), "title": "Update review", "schema": Review.get_schema()},
            "review:delete": {"method": "DELETE", "href": url_for("api.reviewitem", review=review.review_id), "title": "Delete review"},
            "collection": {"method": "GET", "href": url_for("api.reviewcollection"), "title": "Reviews collection"},
            "cookbook:get-recipie": {"method": "GET", "href": f"/api/recipes/{review.recipe_id}", "title": "Get recipe details"},
            "cookbook:get-user": {"method": "GET", "href": f"/api/users/{review.user_id}", "title": "Get user details"}
        }
        return Response(json.dumps(body), status=200, mimetype="application/json")
    
    
    def put(self, review):
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

        logging.info(f"Request JSON: {request.json}")

        review.rating = request.json["rating"]
        review.user_id = request.json.get("user_id")
        review.recipe_id = request.json.get("recipe_id")
        review.feedback = request.json.get("feedback")

        logging.info(f"Updated review: {review.serialize()}")

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

    
    def delete(self, review):
        review = Review.query.get_or_404(review.review_id)
        db.session.delete(review)
        db.session.commit()
        return {"message": "Review deleted"}, 204