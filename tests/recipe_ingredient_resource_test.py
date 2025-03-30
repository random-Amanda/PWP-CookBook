"""
Test the RecipeIngredientCollection and RecipeIngredientItem resources.
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

def _get_recipe_ingredient_json(number=1):
    return {
        "ingredient_id": number,
        "qty": number * 2.5,
        "metric": "cups"
    }

class TestRecipeIngredientCollection():
    """
    This class implements tests for each HTTP method in recipe ingredient collection
    resource.
    """

    RESOURCE_URL = "/api/recipes/1/ingredients/"

    def test_post(self, client):
        """
        Handle POST requests to create a new recipe-ingredient.
        """
        valid = _get_recipe_ingredient_json()

        # test with wrong content type
        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415

        # test with valid and see that it exists afterward
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201

        # remove name field for 400
        valid.pop("qty")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

class TestRecipeIngredientItem():
    """
    This class implements tests for each HTTP method in recipe ingredient item
    resource.
    """

    RESOURCE_URL = "/api/recipes/1/ingredients/ingredient-A/"
    INVALID_URL = "/api/recipes/1/ingredients/ingredient-test/"

    def test_put(self, client):
        """
        Test PUT method for updating a recipe ingredient quantity.
        """
        valid = _get_recipe_ingredient_json()

        # test with wrong content type
        resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415

        # test with valid data
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204

        # test with invalid data (missing required field)
        invalid = _get_recipe_ingredient_json()
        invalid.pop("qty")
        resp = client.put(self.RESOURCE_URL, json=invalid)
        assert resp.status_code == 400

        # test with non-existent recipe-ingredient
        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404

    def test_delete(self, client):
        """
        Test DELETE method for removing a recipe ingredient quantity.
        """
        # test successful deletion
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204

        # verify it's gone by trying to delete again
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 404

        # test with non-existent recipe-ingredient
        resp = client.delete("/api/recipes/999/ingredients/999/")
        assert resp.status_code == 404
