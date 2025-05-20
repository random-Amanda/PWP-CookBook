import pytest
from cookbookapp import create_app, db
from cookbookapp.models import User, Recipe, Ingredient, Review, RecipeIngredientQty
from cookbookapp.models import (init_db_command, drop_db_command, 
                              gen_test_data_command, clear_test_data_command)

@pytest.fixture
def app():
    """Create and configure a test app instance"""
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })
    
    # Create application context
    with app.app_context():
        yield app

@pytest.fixture
def runner(app):
    """Create a CLI test runner"""
    return app.test_cli_runner()

def test_init_db_command(runner, app):
    """Test database initialization and verify tables were created"""
    result = runner.invoke(init_db_command)
    assert 'Initialized the database' in result.output

    with app.app_context():
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        expected_tables = ['user', 'recipe', 'ingredient', 
                         'review', 'recipe_ingredient_qty']
        for table in expected_tables:
            assert table in tables

def test_drop_db_command(runner, app):
    """
    Test database dropping
    1) First initialize the database
    2) Then drop it
    3) Verify that the tables were dropped
    """
    runner.invoke(init_db_command)
    
    result = runner.invoke(drop_db_command)
    assert 'Dropped the database' in result.output

    with app.app_context():
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        assert len(tables) == 0

def test_gen_test_data_command(runner, app):
    """
    Test test data generation
    1) Initialize database first
    2) Generate test data
    3) Verify data was inserted
    4) Verify relationships
    """
    runner.invoke(init_db_command)
    
    result = runner.invoke(gen_test_data_command)
    assert 'Generated test data for all tables' in result.output
    
    with app.app_context():
        assert User.query.count() == 2
        assert Recipe.query.count() == 4
        assert Ingredient.query.count() == 4
        assert Review.query.count() == 4
        assert RecipeIngredientQty.query.count() == 7

        user = User.query.filter_by(username='user1').first()
        assert len(user.recipes) > 0
        assert len(user.reviews) > 0

        recipe = Recipe.query.first()
        assert recipe.user is not None
        assert len(recipe.recipeIngredient) > 0
        assert len(recipe.reviews) > 0

def test_clear_test_data_command(runner, app):
    """
    Test clearing test data
    1) Initialize and generate test data first
    2) Clear the test data
    3) Verify that the data was cleared
    """
    runner.invoke(init_db_command)
    runner.invoke(gen_test_data_command)
    
    result = runner.invoke(clear_test_data_command)
    assert 'Cleared test data from all tables' in result.output
    
    with app.app_context():
        assert User.query.count() == 0
        assert Recipe.query.count() == 0
        assert Ingredient.query.count() == 0
        assert Review.query.count() == 0
        assert RecipeIngredientQty.query.count() == 0

def test_data_integrity(runner, app):
    """
    Test data integrity and relationships after generation
    1) Initialize and generate test data first
    2) Verify relationships
    """
    runner.invoke(init_db_command)
    runner.invoke(gen_test_data_command)
    
    with app.app_context():
        user = User.query.filter_by(username='user1').first()
        assert any(recipe.title == 'Recipe 1' for recipe in user.recipes)

        recipe = Recipe.query.filter_by(title='Recipe 1').first()
        assert any(ri.ingredient.name == 'Ingredient 1' 
                  for ri in recipe.recipeIngredient)

        review = Review.query.first()
        assert review.user is not None
        assert review.recipe is not None 