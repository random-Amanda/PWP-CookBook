import json
from flask_restful import Resource, reqparse
from flask import Response, jsonify, request, url_for
from jsonschema import ValidationError, validate
from cookbookapp import db
from sqlalchemy.exc import IntegrityError
from cookbookapp.models import Review

class ReviewCollection(Resource):
    def get(self):
        body = {"items": []}
        body["self_uri"] = "/api/reviews/"
        body["name"] = "Review Collection"
        body["description"] = "A collection of reviews"

        body["controls"] = {
            "Create_review": {"method": "POST", "href": "/api/reviews", "title": "Create a new review", "schema": Review.get_schema()},
            "Search_review": {"method": "GET", "href": "/api/reviews/search", "title": "Search for reviews"}
        }

        reviews = Review.query.all()
        for review in reviews:

            item = review.serialize()
            item["controls"] = {
                "Self": {"method": "GET", "href": url_for("api.reviewitem", review=review.review_id), "title": "Review details"},
                "Update": {"method": "PUT", "href": f"/api/reviews/{review.review_id}", "title": "Update review", "schema": Review.get_schema()},
                "Delete": {"method": "DELETE", "href": f"/api/reviews/{review.review_id}", "title": "Delete review"}
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
        review = Review.query.get_or_404(review.review_id)
        return review.serialize()
    
    """
    def put(self, review_id):
        review = Review.query.get_or_404(review_id)
        #args = review_parser.parse_args()
        review.user_id = args["user_id"]
        review.recipe_id = args["recipe_id"]
        review.rating = args["rating"]
        review.feedback = args.get("feedback")
        db.session.commit()
        return review.serialize()
    """
    def delete(self, review):
        review = Review.query.get_or_404(review.review_id)
        db.session.delete(review)
        db.session.commit()
        return {"message": "Review deleted"}, 204