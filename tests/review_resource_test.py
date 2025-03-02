import json
import os
import tempfile
import pytest
from unittest.mock import patch
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.exc import SQLAlchemyError

from cookbookapp import create_app, db
from cookbookapp.models import Ingredient, Recipe, RecipeIngredientQty, Review, User

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
    db_fd, db_fname = tempfile.mkstemp()
    config = {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_fname,
        "TESTING": True
    }

    app = create_app(config)

    with app.app_context():
        db.create_all()
        _populate_db()

    # app.test_client_class = AuthHeaderClient
    yield app.test_client()

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

    RESOURCE_URL = "/api/reviews/"

    def test_get(self, client):
        """
        Tests the GET method. Checks that the response status code is 200, and
        then checks that all of the expected attributes. Also checks that all of the items from
        the DB popluation are present, and their controls.
        """
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert len(body["items"]) == 2
        for item in body["items"]:
            assert "rating" in item
            assert "feedback" in item

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
        assert resp.headers["Location"].endswith(self.RESOURCE_URL + "3/")
        resp = client.get(resp.headers["Location"])
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["rating"] == 4
        assert body["feedback"] == "extra-feedback-1"

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

    def test_get(self, client):
        """
        Tests the GET method. Checks that the response status code is 200, and
        then checks that all of the expected attributes and controls are
        present, and the controls work. Also checks that all of the items from
        the DB popluation are present, and their controls.
        """

        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["rating"] == 4
        assert body["feedback"] == "feedback-A"

        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404

    def test_put(self, client):
        """
        Tests the PUT method. Checks all of the possible error codes, and also
        checks that a valid request receives a 204 response. Also tests that
        when id is changed, the review can be found from its new URI.
        """

        valid = _get_review_json()
        invalid = _get_review_invalid_json()

        resp = client.put(self.RESOURCE_URL, data=json.dumps(invalid))
        assert resp.status_code == 415

        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404

        # test with valid data
        valid["rating"] = 6
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204

        # Mock SQLAlchemy commit to raise an error
        with patch('cookbookapp.db.session.commit') as mock_commit:
            mock_commit.side_effect = SQLAlchemyError("Database error")
            
            response = client.put(
                self.RESOURCE_URL,
                data=json.dumps(valid),
                content_type='application/json'
            )
            
            assert response.status_code == 500
            assert "Database commit failed" in response.json["error"]["title"]

        # remove rating field for 400
        valid.pop("rating")
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

    def test_delete(self, client):
        """
        Tests the DELETE method. Checks that a valid request reveives 204
        response and that trying to GET the ingredient afterwards results in 404.
        Also checks that trying to delete a ingredient that doesn't exist results
        in 404.
        """

        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404
