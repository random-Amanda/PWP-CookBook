"""
Test the UserCollection and UserItem resources.
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
INVALID_KEY = "invalidsafetestkey"

class AuthHeaderClient(FlaskClient):
    """
    A test client that automatically adds the API key to all requests.
    """
    def __init__(self, *args, **kwargs):
        self.api_key = kwargs.pop('api_key', TEST_KEY)
        super().__init__(*args, **kwargs)

    def open(self, *args, **kwargs):
        api_key_headers = Headers({
            'API-KEY': self.api_key
        })
        headers = kwargs.pop('headers', Headers())
        headers.extend(api_key_headers)
        kwargs['headers'] = headers
        return super().open(*args, **kwargs)

class NoAuthHeaderClient(FlaskClient):
    """
    A test client that doesn't add any API key.
    """
    pass

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
    """Return a test client for the app with valid API key."""
    return _get_client(TEST_KEY)

@pytest.fixture
def client_no_auth():
    """Return a test client for the app with no API key."""
    return _get_client(None, NoAuthHeaderClient)

@pytest.fixture
def client_invalid_auth():
    """Return a test client for the app with invalid API key."""
    return _get_client(INVALID_KEY)

@pytest.fixture
def client_no_admin_key():
    """Return a test client for the app with no admin key in database."""
    db_fd, db_fname = tempfile.mkstemp()
    config = {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_fname,
        "TESTING": True
    }

    app = create_app(config)

    with app.app_context():
        db.create_all()
        _populate_db()  # Only populate with test data, no API key

    app.test_client_class = AuthHeaderClient
    client = app.test_client()

    def cleanup():
        with app.app_context():
            db.session.remove()
            db.engine.dispose()
        os.close(db_fd)
        os.unlink(db_fname)

    return client, cleanup

def _get_client(api_key, client_class=AuthHeaderClient):
    """Helper function to create a test client with the given API key."""
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

    if api_key:
        app.test_client_class = lambda *args, **kwargs: client_class(*args, api_key=api_key, **kwargs)
    else:
        app.test_client_class = client_class
    
    client = app.test_client()

    # Return a function that can be used to clean up
    def cleanup():
        with app.app_context():
            db.session.remove()
            db.engine.dispose()
        os.close(db_fd)
        os.unlink(db_fname)

    return client, cleanup

def _populate_db():
    """
    Populate the database with test data."""
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

    def test_get_unauthorized_no_key(self, client_no_auth):
        """Test GET without API key."""
        client, cleanup = client_no_auth
        try:
            resp = client.get(self.RESOURCE_URL)
            assert resp.status_code == 401
            data = json.loads(resp.data)
            assert "error" in data
            assert data["error"] == "Unauthorized"
            assert "message" in data
            assert data["message"] == "Missing API key"
        finally:
            cleanup()

    def test_get_unauthorized_invalid_key(self, client_invalid_auth):
        """Test GET with invalid API key."""
        client, cleanup = client_invalid_auth
        try:
            resp = client.get(self.RESOURCE_URL)
            assert resp.status_code == 401
            data = json.loads(resp.data)
            assert "error" in data
            assert data["error"] == "Unauthorized"
            assert "message" in data
            assert data["message"] == "Invalid API key"
        finally:
            cleanup()

    def test_get(self, client):
        """
        Test the GET method of the UserCollection resource.
        """
        client_app, cleanup = client
        try:
            resp = client_app.get(self.RESOURCE_URL)
            assert resp.status_code == 200

            data = json.loads(resp.data)
            assert len(data["items"]) == 2
            for item in data["items"]:
                assert "username" in item
                assert "email" in item
                assert "password" in item
        finally:
            cleanup()

    def test_post(self, client):
        """
        Test the POST method of the UserCollection resource.
        """
        client_app, cleanup = client
        try:
            valid = _get_user_json()
            invalid = _get_user_invalid_json()

            # test with wrong content type
            resp = client_app.post(self.RESOURCE_URL, data=json.dumps(invalid))
            assert resp.status_code == 415

            # test with valid and see that it exists afterwards
            resp = client_app.post(self.RESOURCE_URL, json=valid)
            assert resp.status_code == 201
            assert resp.headers["Location"].endswith(self.RESOURCE_URL + valid["username"] + "/")

            resp = client_app.get(resp.headers["Location"])
            assert resp.status_code == 200

            body = json.loads(resp.data)
            assert body["username"] == "test-user1"
            assert body["email"] == "test-user1@test.com"
            assert body["password"] == "test-password1"

            # send same data again for 409
            resp = client_app.post(self.RESOURCE_URL, json=valid)
            assert resp.status_code == 409

            # remove name field for 400
            valid.pop("username")
            resp = client_app.post(self.RESOURCE_URL, json=valid)
            assert resp.status_code == 400
        finally:
            cleanup()

    def test_get_unauthorized_no_admin_key(self, client_no_admin_key):
        """Test GET when no admin key is configured in database."""
        client_app, cleanup = client_no_admin_key
        try:
            resp = client_app.get(self.RESOURCE_URL)
            assert resp.status_code == 401
            data = json.loads(resp.data)
            assert "error" in data
            assert data["error"] == "Unauthorized"
            assert "message" in data
            assert data["message"] == "Admin key not configured"
        finally:
            cleanup()

    def test_post_unauthorized_no_admin_key(self, client_no_admin_key):
        """Test POST when no admin key is configured in database."""
        client_app, cleanup = client_no_admin_key
        try:
            valid = _get_user_json()
            resp = client_app.post(self.RESOURCE_URL, json=valid)
            assert resp.status_code == 401
            data = json.loads(resp.data)
            assert "error" in data
            assert data["error"] == "Unauthorized"
            assert "message" in data
            assert data["message"] == "Admin key not configured"
        finally:
            cleanup()

class TestUserItem:
    """
    Test the UserItem resource.
    """
    RESOURCE_URL = "/api/users/user1/"
    INVALID_URL = "api/users/non-user-x/"
    MODIFIED_URL = "/api/users/extra-user2/"

    def test_get_unauthorized_no_key(self, client_no_auth):
        """Test GET without API key."""
        client, cleanup = client_no_auth
        try:
            resp = client.get(self.RESOURCE_URL)
            assert resp.status_code == 401
            data = json.loads(resp.data)
            assert "error" in data
            assert data["error"] == "Unauthorized"
            assert "message" in data
            assert data["message"] == "Missing API key"
        finally:
            cleanup()

    def test_get_unauthorized_invalid_key(self, client_invalid_auth):
        """Test GET with invalid API key."""
        client, cleanup = client_invalid_auth
        try:
            resp = client.get(self.RESOURCE_URL)
            assert resp.status_code == 401
            data = json.loads(resp.data)
            assert "error" in data
            assert data["error"] == "Unauthorized"
            assert "message" in data
            assert data["message"] == "Invalid API key"
        finally:
            cleanup()

    def test_get(self, client):
        """
        Test the GET method of the UserItem resource.
        """
        client_app, cleanup = client
        try:
            resp = client_app.get(self.RESOURCE_URL)
            assert resp.status_code == 200

            body = json.loads(resp.data)
            assert body["username"] == "user1"
            assert body["email"] == "user1@example.com"
            assert body["password"] == "password1"

            resp = client_app.get(self.INVALID_URL)
            assert resp.status_code == 404
        finally:
            cleanup()

    def test_get_unauthorized_no_admin_key(self, client_no_admin_key):
        """Test GET when no admin key is configured in database."""
        client_app, cleanup = client_no_admin_key
        try:
            resp = client_app.get(self.RESOURCE_URL)
            assert resp.status_code == 401
            data = json.loads(resp.data)
            assert "error" in data
            assert data["error"] == "Unauthorized"
            assert "message" in data
            assert data["message"] == "Admin key not configured"
        finally:
            cleanup()

    def test_put_unauthorized_no_key(self, client_no_auth):
        """Test PUT without API key."""
        client, cleanup = client_no_auth
        try:
            valid = _get_user_json()
            resp = client.put(self.RESOURCE_URL, json=valid)
            assert resp.status_code == 401
            data = json.loads(resp.data)
            assert "error" in data
            assert data["error"] == "Unauthorized"
            assert "message" in data
            assert data["message"] == "Missing API key"
        finally:
            cleanup()

    def test_put_unauthorized_invalid_key(self, client_invalid_auth):
        """Test PUT with invalid API key."""
        client, cleanup = client_invalid_auth
        try:
            valid = _get_user_json()
            resp = client.put(self.RESOURCE_URL, json=valid)
            assert resp.status_code == 401
            data = json.loads(resp.data)
            assert "error" in data
            assert data["error"] == "Unauthorized"
            assert "message" in data
            assert data["message"] == "Invalid API key"
        finally:
            cleanup()

    def test_put_unauthorized_no_admin_key(self, client_no_admin_key):
        """Test PUT when no admin key is configured in database."""
        client_app, cleanup = client_no_admin_key
        try:
            valid = _get_user_json()
            resp = client_app.put(self.RESOURCE_URL, json=valid)
            assert resp.status_code == 401
            data = json.loads(resp.data)
            assert "error" in data
            assert data["error"] == "Unauthorized"
            assert "message" in data
            assert data["message"] == "Admin key not configured"
        finally:
            cleanup()

    def test_put(self, client):
        """
        Test the PUT method of the UserItem resource.
        """
        client_app, cleanup = client
        try:
            valid = _get_user_json()
            invalid = _get_user_invalid_json()

            # test with wrong content type
            resp = client_app.put(self.RESOURCE_URL, data=json.dumps(invalid))
            assert resp.status_code == 415

            # test with invalid JSON
            resp = client_app.put(self.INVALID_URL, json=valid)
            assert resp.status_code == 404

            #test with another user's username
            valid["username"] = "user2"
            valid["email"] = "testuser2@example.com"
            valid["password"] = "testpassword2"
            resp = client_app.put(self.RESOURCE_URL, json=valid)
            assert resp.status_code == 409

            # test with valid data
            valid["username"] = "user1"
            valid["email"] = "user1@example.com"
            valid["password"] = "password1"
            resp = client_app.put(self.RESOURCE_URL, json=valid)
            assert resp.status_code == 204

            # remove username field for 400
            valid.pop("username")
            resp = client_app.put(self.RESOURCE_URL, json=valid)
            assert resp.status_code == 400
        finally:
            cleanup()

    def test_delete_unauthorized_no_key(self, client_no_auth):
        """Test DELETE without API key."""
        client, cleanup = client_no_auth
        try:
            resp = client.delete(self.RESOURCE_URL)
            assert resp.status_code == 401
            data = json.loads(resp.data)
            assert "error" in data
            assert data["error"] == "Unauthorized"
            assert "message" in data
            assert data["message"] == "Missing API key"
        finally:
            cleanup()

    def test_delete_unauthorized_invalid_key(self, client_invalid_auth):
        """Test DELETE with invalid API key."""
        client, cleanup = client_invalid_auth
        try:
            resp = client.delete(self.RESOURCE_URL)
            assert resp.status_code == 401
            data = json.loads(resp.data)
            assert "error" in data
            assert data["error"] == "Unauthorized"
            assert "message" in data
            assert data["message"] == "Invalid API key"
        finally:
            cleanup()

    def test_delete_unauthorized_no_admin_key(self, client_no_admin_key):
        """Test DELETE when no admin key is configured in database."""
        client_app, cleanup = client_no_admin_key
        try:
            resp = client_app.delete(self.RESOURCE_URL)
            assert resp.status_code == 401
            data = json.loads(resp.data)
            assert "error" in data
            assert data["error"] == "Unauthorized"
            assert "message" in data
            assert data["message"] == "Admin key not configured"
        finally:
            cleanup()

    def test_delete(self, client):
        """
        Test the DELETE method of the UserItem resource.
        """
        client_app, cleanup = client
        try:
            resp = client_app.delete(self.RESOURCE_URL)
            assert resp.status_code == 204

            resp = client_app.get(self.RESOURCE_URL)
            assert resp.status_code == 404

            resp = client_app.delete(self.INVALID_URL)
            assert resp.status_code == 404
        finally:
            cleanup()
