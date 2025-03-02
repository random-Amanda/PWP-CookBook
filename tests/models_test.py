import pytest
from cookbookapp.models import User, Recipe, Review, Ingredient, RecipeIngredientQty
from cookbookapp import db

@pytest.fixture
def test_user():
    user = User(
        user_id=1,
        email="test@example.com",
        username="testuser",
        password="testpass"
    )
    return user

@pytest.fixture
def test_recipe(test_user):
    recipe = Recipe(
        recipe_id=1,
        user_id=test_user.user_id,
        title="Test Recipe",
        description="Test Description",
        steps="Test Steps",
        preparation_time="10 mins",
        cooking_time="20 mins",
        serving=4
    )
    return recipe

@pytest.fixture
def test_ingredient():
    ingredient = Ingredient(
        ingredient_id=1,
        name="Test Ingredient",
        description="Test Ingredient Description"
    )
    return ingredient

@pytest.fixture
def test_recipe_ingredient(test_recipe, test_ingredient):
    recipe_ingredient = RecipeIngredientQty(
        qty_id=1,
        recipe_id=test_recipe.recipe_id,
        ingredient_id=test_ingredient.ingredient_id,
        qty=100.0,
        metric="g"
    )
    recipe_ingredient.ingredient = test_ingredient
    return recipe_ingredient

@pytest.fixture
def test_review(test_user, test_recipe):
    review = Review(
        review_id=1,
        user_id=test_user.user_id,
        recipe_id=test_recipe.recipe_id,
        rating=5,
        feedback="Test Feedback"
    )
    review.user = test_user
    return review

def test_user_serialize(test_user):
    serialized = test_user.serialize()
    assert serialized == {
        "user_id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass"
    }

def test_recipe_serialize(test_recipe, test_review, test_recipe_ingredient):
    # Set up relationships
    test_recipe.reviews = [test_review]
    test_recipe.recipeIngredient = [test_recipe_ingredient]
    
    serialized = test_recipe.serialize()
    assert serialized == {
        "recipe_id": 1,
        "user_id": 1,
        "title": "Test Recipe",
        "description": "Test Description",
        "steps": "Test Steps",
        "preparation_time": "10 mins",
        "cooking_time": "20 mins",
        "serving": 4,
        "recipeIngredient": [{
            "ingredient_id": 1,
            "ingredient": "Test Ingredient",
            "qty": 100.0,
            "metric": "g"
        }],
        "reviews": [{
            "review_id": 1,
            "rating": 5,
            "feedback": "Test Feedback",
            "user": "testuser"
        }]
    }

def test_review_serialize(test_review):
    serialized = test_review.serialize()
    assert serialized == {
        "review_id": 1,
        "user_id": 1,
        "recipe_id": 1,
        "rating": 5,
        "feedback": "Test Feedback"
    }

def test_ingredient_serialize(test_ingredient):
    serialized = test_ingredient.serialize()
    assert serialized == {
        "ingredient_id": 1,
        "name": "Test Ingredient",
        "description": "Test Ingredient Description"
    }

def test_recipe_ingredient_qty_serialize(test_recipe_ingredient):
    serialized = test_recipe_ingredient.serialize()
    assert serialized == {
        "qty_id": 1,
        "recipe_id": 1,
        "ingredient_id": 1,
        "qty": 100.0,
        "metric": "g"
    } 