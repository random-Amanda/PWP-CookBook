"""
Test the UserCollection and UserItem resources.
"""
import json
import os
import tempfile
import pytest
from sqlalchemy.engine import Engine
from sqlalchemy import event

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
    for idx, letter in enumerate("AB", start=1):
        user = User(
            username=f"user{idx}",
            email=f"user{idx}@example.com",
            password=f"password{idx}"
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

def _get_user_json(number=1):
    """
    Return a JSON representation of a user.
    """
    return {
        "username": f"test-user{number}",
        "email": f"test-user{number}@test.com",
        "password": f"test-password{number}"
    }

def _get_user_invalid_json(number=1):
    """
    Return an invalid JSON representation of a user.
    """
    return {
        "email": f"test-user{number}@test.com",
        "password": f"test-password{number}"
    }

class TestUserCollection:
    """
    Test the UserCollection resource.
    """

    RESOURCE_URL = "/api/users/"

    def test_get(self, client):
        """
        Test the GET method of the UserCollection resource.
        """
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200

        data = json.loads(resp.data)
        assert len(data["items"]) == 2
        for item in data["items"]:
            assert "username" in item
            assert "email" in item
            assert "password" in item

    def test_post(self, client):
        """
        Test the POST method of the UserCollection resource.
        """
        valid = _get_user_json()
        invalid = _get_user_invalid_json()

        # test with wrong content type
        resp = client.post(self.RESOURCE_URL, data=json.dumps(invalid))
        assert resp.status_code == 415

        # test with valid and see that it exists afterwards
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201
        assert resp.headers["Location"].endswith(self.RESOURCE_URL + valid["username"] + "/")

        resp = client.get(resp.headers["Location"])
        assert resp.status_code == 200

        body = json.loads(resp.data)
        assert body["username"] == "test-user1"
        assert body["email"] == "test-user1@test.com"
        assert body["password"] == "test-password1"

        # send same data again for 409
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409

        # remove name field for 400
        valid.pop("username")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

class TestUserItem:
    """
    Test the UserItem resource.
    """
    RESOURCE_URL = "/api/users/user1/"
    INVALID_URL = "api/users/non-user-x/"
    MODIFIED_URL = "/api/users/extra-user2/"

    def test_get(self, client):
        """
        Test the GET method of the UserItem resource.
        """
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200

        body = json.loads(resp.data)
        assert body["username"] == "user1"
        assert body["email"] == "user1@example.com"
        assert body["password"] == "password1"

        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404

    def test_put(self, client):
        """
        Test the PUT method of the UserItem resource.
        """
        valid = _get_user_json()
        invalid = _get_user_invalid_json()

        # test with wrong content type
        resp = client.put(self.RESOURCE_URL, data=json.dumps(invalid))
        assert resp.status_code == 415

        # test with invalid JSON
        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404

        #test with another user's username
        valid["username"] = "user2"
        valid["email"] = "testuser2@example.com"
        valid["password"] = "testpassword2"
        print(self.RESOURCE_URL)
        print(valid)
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409

        # test with valid data
        valid["username"] = "user1"
        valid["email"] = "user1@example.com"
        valid["password"] = "password1"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204

        # remove username field for 400
        valid.pop("username")
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

    def test_delete(self, client):
        """
        Test the DELETE method of the UserItem resource.
        """
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204

        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 404

        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404
