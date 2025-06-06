"""
Test the ReviewCollection and ReviewItem resources.
"""
import json
import os
import tempfile
import pytest
from sqlalchemy.engine import Engine
from sqlalchemy import event
from flask.testing import FlaskClient
from werkzeug.datastructures import Headers

from cookbookapp import create_app, db
from cookbookapp.models import Ingredient, Recipe, RecipeIngredientQty, Review, User, ApiKey

# Test API key
TEST_KEY = "verysafetestkey"

class AuthHeaderClient(FlaskClient):
    """
    A test client that automatically adds the API key to all requests.
    """
    def open(self, *args, **kwargs):
        api_key_headers = Headers({
            'API-KEY': TEST_KEY
        })
        headers = kwargs.pop('headers', Headers())
        headers.extend(api_key_headers)
        kwargs['headers'] = headers
        return super().open(*args, **kwargs)

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """
    Enable foreign key support for SQLite.
    """
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


@pytest.fixture
def client():
    """
    Return a test client for the app.
    """
    db_fd, db_fname = tempfile.mkstemp()
    config = {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_fname,
        "TESTING": True
    }

    app = create_app(config)

    with app.app_context():
        db.create_all()
        # Create test API key in the database
        db_key = ApiKey(
            key=ApiKey.key_hash(TEST_KEY),
            admin=True
        )
        db.session.add(db_key)
        db.session.commit()
        _populate_db()

    app.test_client_class = AuthHeaderClient
    yield app.test_client()

    # Ensure the database connection is closed
    with app.app_context():
        db.session.remove()
        db.engine.dispose()

    os.close(db_fd)
    os.unlink(db_fname)

def _populate_db():
    for idx, letter in enumerate("AB", start=1):
        user = User(
            email=f"user-{idx}@example.com",
            username=f"user-{idx}",
            password="password"
        )
        db.session.add(user)

    for idx, letter in enumerate("AB", start=1):
        recipe = Recipe(
            title=f"recipe-{letter}",
            description=f"description-{letter}",
            steps=f"steps-{letter}",
            preparation_time=f"preparation Time-{idx}",
            cooking_time=f"cooking Time-{idx}",
            serving=f"serving-{idx}",
            user_id=idx
        )
        db.session.add(recipe)

    for idx, letter in enumerate("AB", start=1):
        ingredient = Ingredient(
            name=f"ingredient-{letter}",
            description=f"description-{letter}"
        )
        db.session.add(ingredient)

    for idx, letter in enumerate("AB", start=1):
        review = Review(
            rating=idx + 3,
            feedback=f"feedback-{letter}",
            user_id=idx,
            recipe_id=idx
        )
        db.session.add(review)

    for idx, letter in enumerate("AB", start=1):
        recipe_ingredient = RecipeIngredientQty(
            recipe_id=idx,
            ingredient_id=idx,
            qty=idx * 2.5,
            metric="cups"
        )
        db.session.add(recipe_ingredient)

    db.session.commit()

def _get_review_json(number=1):
    """
    Creates a valid review JSON object to be used for PUT and POST tests.
    """
    return {
        "rating": 4,
        "feedback": f"extra-feedback-{number}"
    }

def _get_review_invalid_json(number=1):
    """
    Creates a invalid review JSON object to be used for PUT and POST tests.
    """
    return {
        "feedback": f"extra-feedback-{number}"
    }

class TestReviewCollection():
    """
    This class implements tests for each HTTP method in review collection
    resource.
    """

    RESOURCE_URL = "/api/recipes/1/reviews/"

    def test_post(self, client):
        """
        Tests the POST method. Checks all of the possible error codes, and
        also checks that a valid request receives a 201 response with a
        location header that leads into the newly created resource.
        """

        valid = _get_review_json()
        invalid = _get_review_invalid_json()

        # test with wrong content type
        resp = client.post(self.RESOURCE_URL, data=json.dumps(invalid))
        assert resp.status_code == 415

        # test with valid and see that it exists afterward
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201

        # remove name field for 400
        valid.pop("rating")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

class TestReviewItem():
    """
    This class implements tests for each HTTP method in ingredient item
    resource.
    """

    RESOURCE_URL = "/api/reviews/1/"
    INVALID_URL = "/api/reviews/10/"
    MODIFIED_URL = "/api/reviews/3/"

    def test_delete(self, client):
        """
        Tests the DELETE method. Checks that a valid request reveives 204
        response and that trying to GET the ingredient afterwards results in 404.
        Also checks that trying to delete a ingredient that doesn't exist results
        in 404.
        """

        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404
