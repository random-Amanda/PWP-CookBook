"""
Test the database models.
"""
import os
import tempfile
import pytest
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Engine

from cookbookapp import create_app, db
from cookbookapp.models import Ingredient, Recipe, RecipeIngredientQty, Review, User

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

@pytest.fixture
def app():
    """
    Create a new application for testing.
    """
    db_fd, db_fname = tempfile.mkstemp()
    config = {
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_fname}",
        "TESTING": True
    }

    app = create_app(config)

    with app.app_context():
        db.create_all()

    yield app

    # Ensure the database connection is closed
    with app.app_context():
        db.session.remove()
        db.engine.dispose()

    os.close(db_fd)
    os.unlink(db_fname)

@pytest.fixture
def client(app):
    """
    Return a test client for the app.
    """
    return app.test_client()

@pytest.fixture
def runner(app):
    """
    Return a test runner for the app.
    """
    return app.test_cli_runner()

def _get_user():
    return User(
        username="testuser",
        email="testuser@test.com",
        password="testpassword"
    )

def _get_recipe():
    return Recipe(
        title="testrecipe",
        description="testdescription",
        steps="teststeps",
        preparation_time=30,
        cooking_time=60,
        serving=4
    )

def _get_ingredient():
    return Ingredient(
        name="testingredient",
        description="testdescription"
    )

def _get_recipeingredientqty():
    return RecipeIngredientQty(
        qty=2,
        metric="cups"
    )

def _get_review():
    return Review(
        rating=4,
        feedback="testcomment"
    )

def test_create_instances(app):
    """
    Tests that we can create one instance of each model and save them to the
    database using valid values for all columns. After creation, test that
    everything can be found from database, and that all relationships have been
    saved correctly.
    """
    user = _get_user()
    recipe = _get_recipe()
    ingredient = _get_ingredient()
    recipeingredientqty = _get_recipeingredientqty()
    review = _get_review()

    user.recipes.append(recipe)
    user.reviews.append(review)
    recipe.user = user
    recipe.reviews.append(review)
    recipeingredientqty.recipe = recipe
    recipeingredientqty.ingredient = ingredient
    review.user = user
    review.recipe = recipe

    with app.app_context():
        db.session.add(user)
        db.session.add(recipe)
        db.session.add(ingredient)
        db.session.add(recipeingredientqty)
        db.session.add(review)
        db.session.commit()

        assert User.query.count() == 1
        assert Recipe.query.count() == 1
        assert Ingredient.query.count() == 1
        assert RecipeIngredientQty.query.count() == 1
        assert Review.query.count() == 1

        db_user = User.query.first()
        db_recipe = Recipe.query.first()
        db_ingredient = Ingredient.query.first()
        db_recipeingredientqty = RecipeIngredientQty.query.first()
        db_review = Review.query.first()

        assert db_recipe.user == db_user
        assert db_recipeingredientqty.recipe == db_recipe
        assert db_recipeingredientqty.ingredient == db_ingredient
        assert db_review.user == db_user
        assert db_review.recipe == db_recipe

def test_user_colums(app):
    """
    Tests user columns' restrictions. username and email should be unique. 
    username, email, and password should not be null.
    """

    with app.app_context():
        user_1 = _get_user()
        user_2 = _get_user()
        db.session.add(user_1)
        db.session.add(user_2)
        with pytest.raises(IntegrityError):
            db.session.commit()

        db.session.rollback()

        user = _get_user()
        user.username = None
        db.session.add(user)
        with pytest.raises(IntegrityError):
            db.session.commit()

        db.session.rollback()

        user = _get_user()
        user.email = None
        db.session.add(user)
        with pytest.raises(IntegrityError):
            db.session.commit()

        db.session.rollback()

        user = _get_user()
        user.password = None
        db.session.add(user)
        with pytest.raises(IntegrityError):
            db.session.commit()

def test_recipe_columns(app):
    """
    Tests recipe columns' restrictions. title, steps, preparation_time 
    cooking_time and serving should not be null.
    """

    with app.app_context():
        recipe = _get_recipe()
        recipe.title = None
        db.session.add(recipe)
        with pytest.raises(IntegrityError):
            db.session.commit()

        db.session.rollback()

        recipe = _get_recipe()
        recipe.steps = None
        db.session.add(recipe)
        with pytest.raises(IntegrityError):
            db.session.commit()

        db.session.rollback()

        recipe = _get_recipe()
        recipe.preparation_time = None
        db.session.add(recipe)
        with pytest.raises(IntegrityError):
            db.session.commit()

        db.session.rollback()

        recipe = _get_recipe()
        recipe.cooking_time = None
        db.session.add(recipe)
        with pytest.raises(IntegrityError):
            db.session.commit()

        db.session.rollback()

        recipe = _get_recipe()
        recipe.serving = None
        db.session.add(recipe)
        with pytest.raises(IntegrityError):
            db.session.commit()

def test_ingredient_columns(app):
    """
    Tests ingredient columns' restrictions. 
    name must be unique, and name should not be null.
    """

    with app.app_context():
        ingredient_1 = _get_ingredient()
        ingredient_2 = _get_ingredient()
        db.session.add(ingredient_1)
        db.session.add(ingredient_2)
        with pytest.raises(IntegrityError):
            db.session.commit()

        db.session.rollback()

        ingredient = _get_ingredient()
        ingredient.name = None
        db.session.add(ingredient)
        with pytest.raises(IntegrityError):
            db.session.commit()

def test_recipeingredientqty_columns(app):
    """
    Tests recipeingredientqty columns' restrictions. 
    qty and metric should not be null.
    """
    with app.app_context():
        recipeingredientqty = _get_recipeingredientqty()
        recipeingredientqty.qty = None
        db.session.add(recipeingredientqty)
        with pytest.raises(IntegrityError):
            db.session.commit()

        db.session.rollback()

        recipeingredientqty = _get_recipeingredientqty()
        recipeingredientqty.metric = None
        db.session.add(recipeingredientqty)
        with pytest.raises(IntegrityError):
            db.session.commit()

def test_review_columns(app):
    """
    Tests review columns' restrictions. 
    rating should not be null.
    """

    with app.app_context():
        review = _get_review()
        review.rating = None
        db.session.add(review)
        with pytest.raises(IntegrityError):
            db.session.commit()

def test_user_ondelete_recipe(app):
    """
    Tests that recipe's user foreing key is set to null 
    when user is deleted.
    """

    with app.app_context():
        recipe = _get_recipe()
        user = _get_user()
        recipe.user = user
        db.session.add(recipe)
        db.session.commit()
        db.session.delete(user)
        db.session.commit()
        assert recipe.user is None

def test_user_ondelete_review(app):
    """
    Tests that review's user foreing key is set to null
    when user is deleted.
    """

    with app.app_context():
        review = _get_review()
        user = _get_user()
        review.user = user
        db.session.add(review)
        db.session.commit()
        db.session.delete(user)
        db.session.commit()
        assert review.user is None

def test_recipe_ondelete_review(app):
    """
    Tests that review's recipe foreing key is set to null
    when recipe is deleted.
    """

    with app.app_context():
        review = _get_review()
        recipe = _get_recipe()
        review.recipe = recipe
        db.session.add(review)
        db.session.commit()
        db.session.delete(recipe)
        db.session.commit()
        assert review.recipe is None

def test_recipe_ondelete_recipeingredientqty(app):
    """
    Tests that recipeingredientqty's recipe foreing key is set to null
    when recipe is deleted.
    """

    with app.app_context():
        recipeingredientqty = _get_recipeingredientqty()
        recipe = _get_recipe()
        recipeingredientqty.recipe = recipe
        db.session.add(recipeingredientqty)
        db.session.commit()
        db.session.delete(recipe)
        db.session.commit()
        assert recipeingredientqty.recipe is None

def test_ingredient_ondelete_recipeingredientqty(app):
    """
    Tests that recipeingredientqty's ingredient foreing key is set to null
    when ingredient is deleted.
    """

    with app.app_context():
        recipeingredientqty = _get_recipeingredientqty()
        ingredient = _get_ingredient()
        recipeingredientqty.ingredient = ingredient
        db.session.add(recipeingredientqty)
        db.session.commit()
        db.session.delete(ingredient)
        db.session.commit()
        assert recipeingredientqty.ingredient is None
