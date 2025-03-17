"""
Test the RecipeCollection and RecipeItem resources.
"""
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
    """
    Return a test client for the app."""
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

    # Ensure the database connection is closed
    with app.app_context():
        db.session.remove()
        db.engine.dispose()

    os.close(db_fd)
    os.unlink(db_fname)

def _populate_db():
    """
    Populate the database with test data."""
    for idx, letter in enumerate("AB", start=1):
        user = User(
            email=f"user-{idx}@example.com",
            username=f"user-{idx}",
            password="password"
        )
        db.session.add(user)

    for idx, letter in enumerate("AB", start=1):
        recipe = Recipe(
            user_id=idx,
            title=f"recipe-{letter}",
            description=f"description-{letter}",
            steps=json.dumps({'step1': 'step 1', 'step2': 'step 2'}),
            preparation_time=f"preparation Time-{idx}",
            cooking_time=f"cooking Time-{idx}",
            serving=f"serving-{idx}" 
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

def test_get_recipe_json(number=3):
    """
    Return a JSON representation of a recipe.
    """
    return {
        "user_id": 1,
        "title": f"recipe-{number}",
        "description": f"description-{number}",
        "steps": "{'step1': 'step 1', 'step2': 'step 2'}",
        "preparation_time": f"preparation time-{number}",
        "cooking_time": f"cooking time-{number}",
        "serving": number
    }

def test_get_recipe_invalid_json(number=3):
    """
    Return an invalid JSON representation of a recipe.
    """
    return {
        "user_id": number,
        "description": f"description-{number}",
        "steps": f"steps-{number}",
        "preparation_time": f"preparation time-{number}",
        "cooking_time": f"cooking time-{number}",
        "serving": f"serving-{number}"
    }

class TestRecipeCollection:
    """
    Test the RecipeCollection resource.
    """

    RESOURCE_URL = "/api/recipes/"

    def test_get(self, client):
        """
        Test the GET method of the RecipeCollection resource.
        """
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200

        data = json.loads(resp.data)
        assert len(data["items"]) == 2
        for item in data["items"]:
            assert "title" in item
            assert "description" in item
            assert "steps" in item
            assert "preparation_time" in item
            assert "cooking_time" in item
            assert "serving" in item
            assert "user_id" in item

    def test_post(self, client):
        """
        Test the POST method of the RecipeCollection resource.
        """
        
        valid = test_get_recipe_json()
        invalid = test_get_recipe_invalid_json()

        # test with wrong content type
        resp = client.post(self.RESOURCE_URL, data=json.dumps(invalid))
        assert resp.status_code == 415

        # test with valid data
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201
        assert resp.headers["Location"].endswith(self.RESOURCE_URL + "3/")

        resp = client.get(resp.headers["Location"])
        assert resp.status_code == 200

        body = json.loads(resp.data)
        assert body["title"] == "recipe-3"
        assert body["description"] == "description-3"
        assert body["steps"] == "{'step1': 'step 1', 'step2': 'step 2'}"
        assert body["preparation_time"] == "preparation time-3"
        assert body["cooking_time"] == "cooking time-3"
        assert body["serving"] == 3
        assert body["user_id"] == 1

        # remove name field for 400
        valid.pop("title")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

class TestRecipeItem:
    """
    Test the RecipeItem resource.
    """
    RESOURCE_URL = "/api/recipes/1/"
    INVALID_URL = "/api/recipes/no-10/"
    MODIFIED_URL = "/api/recipes/15/"

    def test_get(self, client):
        """
        Test the GET method of the RecipeItem resource.
        """
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200

        body = json.loads(resp.data)
        assert body["title"] == "recipe-A"
        assert body["description"] == "description-A"
        assert body["steps"] == json.dumps({'step1': 'step 1', 'step2': 'step 2'})
        assert body["preparation_time"] == "preparation Time-1"
        assert body["cooking_time"] == "cooking Time-1"
        assert body["serving"] == "serving-1"
        assert body["user_id"] == 1

        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404
    
    def test_put(self, client):
        """
        Test the PUT method of the RecipeItem resource.
        """
        valid = test_get_recipe_json()
        invalid = test_get_recipe_invalid_json()

        # test with wrong content type
        resp = client.put(self.RESOURCE_URL, data=json.dumps(invalid))
        assert resp.status_code == 415

        # test with valid data
        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404

        ##test with another recipe 
        # valid["title"] = "recipe-B"
        # valid["description"] = "description-B"
        # valid["steps"] = json.dumps({'step1': 'step 1', 'step2': 'step 2'})
        # valid["preparation_time"] = "preparation Time-2"
        # valid["cooking_time"] = "cooking Time-2"
        # valid["serving"] = "serving-2"
        # valid["user_id"] = 2
        # resp = client.put(self.RESOURCE_URL, json=valid)
        # assert resp.status_code == 409

        # test with valid data
        valid["title"] = "recipe-A"
        valid["description"] = "description-A"
        valid["steps"] = "{'step1': 'step 1', 'step2': 'step 2'}"
        valid["preparation_time"] = "preparation Time-1"
        valid["cooking_time"] = "cooking Time-1"
        valid["serving"] = 2
        valid["user_id"] = 1
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204

        # remove title field for 400
        valid.pop("title")
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400