"""
This file contains the models for the cookbook application.
"""
import click
from flask.cli import with_appcontext
from sqlalchemy import event, Engine
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from cookbookapp import db

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """
    Enable foreign key support for SQLite.
    """
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

class User(db.Model):
    """
    Represents a user in the application.
    """
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)

    recipes = db.relationship('Recipe', back_populates='user')
    reviews = db.relationship('Review', back_populates='user')

    def serialize(self):
        """
        Serialize the user object to a dictionary.
        """
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "password": self.password
        }

    # def deserialize(self):
    #     """
    #     Deserialize a dictionary to a user object.
    #     """
    #     return User(
    #         username=self.get("username"),
    #         email=self.get("email"),
    #         password=self.get("password")
    #     )

    @staticmethod
    def get_schema():
        """
        Get the JSON schema for the user model.
        """
        return {
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "email": {"type": "string"},
                "password": {"type": "string"}
            },
            "required": ["username", "email", "password"]
        }

class Recipe(db.Model):
    """
    Represents a recipe in the application.
    """
    __tablename__ = 'recipe'
    recipe_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.user_id', ondelete='SET NULL'), nullable=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    steps = db.Column(db.Text, nullable=False)
    preparation_time = db.Column(db.String(200), nullable=False)
    cooking_time = db.Column(db.String(200), nullable=False)
    serving = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', back_populates='recipes')
    reviews = db.relationship('Review', back_populates='recipe')
    recipeIngredient = db.relationship('RecipeIngredientQty', back_populates='recipe')

    def serialize(self):
        """
        Serialize the recipe object to a dictionary.
        """
        return {
            "recipe_id": self.recipe_id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "steps": self.steps,
            "preparation_time": self.preparation_time,
            "cooking_time": self.cooking_time,
            "serving": self.serving,
            "recipeIngredient": [
                {
                    "ingredient_id": ing.ingredient_id,
                    "ingredient" : ing.ingredient.name,
                    "qty": ing.qty,
                    "metric": ing.metric
                }
                for ing in  self.recipeIngredient
            ],
            "reviews": [
                {
                    "review_id": rev.review_id,
                    "rating": rev.rating,
                    "feedback": rev.feedback,
                    "user": rev.user.username
                }
                for rev in  self.reviews
            ]
            }

    # def deserialize(self):
    #     """
    #     Deserialize a dictionary to a recipe object.
    #     """
    #     return Recipe(
    #         user_id=self.get("user_id"),
    #         title=self.get("title"),
    #         description=self.get("description"),
    #         steps=self.get("steps"),
    #         preparation_time=self.get("preparation_time"),
    #         cooking_time=self.get("cooking_time"),
    #         serving=self.get("serving")
    #     )

    @staticmethod
    def get_schema():
        """
        Get the JSON schema for the recipe model.
        """
        return {
            "type": "object",
            "properties": {
                "user_id": {"type": "integer"},
                "title": {"type": "string"},
                "description": {"type": "string"},
                "steps": {"type": "string"},
                "preparation_time": {"type": "string"},
                "cooking_time": {"type": "string"},
                "serving": {"type": "integer"}
            },
            "required": ["title", "steps", "preparation_time", "cooking_time", "serving"]
        }

class Review(db.Model):
    """
    Represents a review in the application.
    """
    __tablename__ = 'review'
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.user_id', ondelete='SET NULL'), nullable=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        'recipe.recipe_id', ondelete='SET NULL'), nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.Text)

    recipe = db.relationship('Recipe', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')

    def serialize(self):
        """
        Serialize the review object to a dictionary.
        """
        return {
            "review_id": self.review_id,
            "user_id": self.user_id,
            "recipe_id": self.recipe_id,
            "rating": self.rating,
            "feedback": self.feedback}

    # def deserialize(self):
    #     """
    #     Deserialize a dictionary to a review object.
    #     """
    #     return Review(
    #         user_id=self.get("user_id"),
    #         recipe_id=self.get("recipe_id"),
    #         rating=self.get("rating"),
    #         feedback=self.get("feedback"))

    @staticmethod
    def get_schema():
        """
        Get the JSON schema for the review model.
        """
        return {
            "type": "object",
            "properties": {
                "user_id": {"type": "integer"},
                "recipe_id": {"type": "integer"},
                "rating": {"type": "integer"},
                "feedback": {"type": "string"}
            },
            "required": ["rating"]
        }

class Ingredient(db.Model):
    """
    Represents an ingredient in the application.
    """
    __tablename__ = 'ingredient'
    ingredient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True) #update in wiki
    description = db.Column(db.Text)

    recipeIngredient = db.relationship('RecipeIngredientQty', back_populates='ingredient')

    def serialize(self):
        """
        Serialize the ingredient object to a dictionary.
        """
        return {
            "ingredient_id": self.ingredient_id,
            "name": self.name,
            "description": self.description
        }

    # def deserialize(self):
    #     """
    #     Deserialize a dictionary to an ingredient object.
    #     """
    #     return Ingredient(
    #         name=self.get("name"),
    #         description=self.get("description")
    #     )

    @staticmethod
    def get_schema():
        """
        Get the JSON schema for the ingredient model.
        """
        return {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "description": {"type": "string"}
            },
            "required": ["name"]
        }

class RecipeIngredientQty(db.Model):
    """
    Represents the quantity of an ingredient in a recipe.
    """
    __tablename__ = 'recipe_ingredient_qty'
    qty_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id',
                                                    ondelete='SET NULL'), nullable=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.ingredient_id',
                                                        ondelete='SET NULL'), nullable=True)
    qty = db.Column(db.Float, nullable=False)
    metric = db.Column(db.String(20), nullable=False)

    ingredient = db.relationship('Ingredient', back_populates='recipeIngredient')
    recipe = db.relationship('Recipe', back_populates='recipeIngredient')

    def serialize(self):
        """
        Serialize the recipe ingredient quantity object to a dictionary.
        """
        return {
            'qty_id': self.qty_id,
            'recipe_id': self.recipe_id,
            'ingredient_id': self.ingredient_id,
            'qty': self.qty,
            'metric': self.metric
        }

    # def deserialize(self):
    #     """
    #     Deserialize a dictionary to a recipe ingredient quantity object.
    #     """
    #     return RecipeIngredientQty(
    #         recipe_id=self.get("recipe_id"),
    #         ingredient_id=self.get("ingredient_id"),
    #         qty=self.get("qty"),
    #         metric=self.get("metric")
    #     )

    @staticmethod
    def get_schema():
        """
        Get the JSON schema for the recipe ingredient quantity model.
        """
        return {
            "type": "object",
            "properties": {
                "recipe_id": {"type": "integer"},
                "ingredient_id": {"type": "integer"},
                "qty": {"type": "number"},
                "metric": {"type": "string"}
            },
            "required": ["qty", "metric"]
        }

@click.command("init-db")
@with_appcontext
def init_db_command():
    """
    Initialize the database.
    """
    db.create_all()
    click.echo("Initialized the database.")

@click.command("drop-db")
@with_appcontext
def drop_db_command():
    """
    Drop all tables in the database.
    """
    db.drop_all()
    click.echo("Dropped the database.")

@click.command("gen-test-data")
@with_appcontext
def gen_test_data_command():
    """
    Generate test data for all tables.
    """
    try:
        add_users()
        add_ingredients()
        add_recipes()
        add_recipe_ingredients()
        add_reviews()
        click.echo("Generated test data for all tables.")
    except (SQLAlchemyError, IntegrityError) as e:
        db.session.rollback()
        click.echo(f'Error generating data: {e}')
        raise e

def add_users():
    """
    Generate test user data
    """
    user1 = User(email="user1@test.com", username="user1", password="user1")
    user2 = User(email="user2@test.com", username="user2", password="user2")
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()
    click.echo("Added user test data.")

def add_ingredients():
    """
    Generate test ingredients data
    """
    ingredient1 = Ingredient(name="Ingredient 1", description="Description 1")
    ingredient2 = Ingredient(name="Ingredient 2", description="Description 2")
    ingredient3 = Ingredient(name="Ingredient 3", description="Description 3")
    ingredient4 = Ingredient(name="Ingredient 4", description="Description 4")
    db.session.add(ingredient1)
    db.session.add(ingredient2)
    db.session.add(ingredient3)
    db.session.add(ingredient4)
    db.session.commit()
    click.echo("Added ingredient test data.")

def add_recipes():
    """
    Generate test recipe data
    """
    user1 = User.query.filter_by(username="user1").first()
    user2 = User.query.filter_by(username="user2").first()
    recipe1 = Recipe(user=user1, title="Recipe 1", description="Description 1",
                         steps=' {"step1": "step 1", "step2": "step 2"} ',
                         preparation_time="10 mins", cooking_time="20 mins", serving=2)
    recipe2 = Recipe(user=user2, title="Recipe 2", description="Description 2",
                         steps=' {"step1": "step 1", "step2": "step 2"}  ',
                         preparation_time="15 mins", cooking_time="25 mins", serving=1)
    recipe3 = Recipe(user=user1, title="Recipe 3", description="Description 3",
                         steps=' {"step1": "step 1", "step2": "step 2"}  ',
                         preparation_time="20 mins", cooking_time="30 mins", serving=1)
    recipe4 = Recipe(user=user2, title="Recipe 4", description="Description 4",
                         steps=' {"step1": "step 1", "step2": "step 2"}  ',
                         preparation_time="25 mins", cooking_time="35 mins", serving=3)
    db.session.add(recipe1)
    db.session.add(recipe2)
    db.session.add(recipe3)
    db.session.add(recipe4)
    db.session.commit()
    click.echo("Added recipe test data.")

def add_recipe_ingredients():
    """
    Generate test recipe ingredient data
    """
    recipe1 = Recipe.query.filter_by(title="Recipe 1").first()
    recipe2 = Recipe.query.filter_by(title="Recipe 2").first()
    recipe3 = Recipe.query.filter_by(title="Recipe 3").first()
    recipe4 = Recipe.query.filter_by(title="Recipe 4").first()
    ingredient1 = Ingredient.query.filter_by(name="Ingredient 1").first()
    ingredient2 = Ingredient.query.filter_by(name="Ingredient 2").first()
    ingredient3 = Ingredient.query.filter_by(name="Ingredient 3").first()
    ingredient4 = Ingredient.query.filter_by(name="Ingredient 4").first()
    recipe_ingredient_qty1 = RecipeIngredientQty(recipe=recipe1, ingredient=ingredient1,
                                                 qty=100, metric="g")
    recipe_ingredient_qty2 = RecipeIngredientQty(recipe=recipe1, ingredient=ingredient2,
                                                 qty=200, metric="g")
    recipe_ingredient_qty3 = RecipeIngredientQty(recipe=recipe2, ingredient=ingredient1,
                                                 qty=500, metric="g")
    recipe_ingredient_qty4 = RecipeIngredientQty(recipe=recipe2, ingredient=ingredient3,
                                                 qty=3, metric="tablespoon")
    recipe_ingredient_qty5 = RecipeIngredientQty(recipe=recipe2, ingredient=ingredient4,
                                                 qty=40, metric="ml")
    recipe_ingredient_qty6 = RecipeIngredientQty(recipe=recipe3, ingredient=ingredient2,
                                                 qty=500, metric="g")
    recipe_ingredient_qty7 = RecipeIngredientQty(recipe=recipe4, ingredient=ingredient4,
                                                  qty=150, metric="ml")
    db.session.add(recipe_ingredient_qty1)
    db.session.add(recipe_ingredient_qty2)
    db.session.add(recipe_ingredient_qty3)
    db.session.add(recipe_ingredient_qty4)
    db.session.add(recipe_ingredient_qty5)
    db.session.add(recipe_ingredient_qty6)
    db.session.add(recipe_ingredient_qty7)
    db.session.commit()
    click.echo("Added recipe ingredient test data.")

def add_reviews():
    """
    Generate test review data
    """
    user1 = User.query.filter_by(username="user1").first()
    user2 = User.query.filter_by(username="user2").first()
    recipe1 = Recipe.query.filter_by(title="Recipe 1").first()
    recipe2 = Recipe.query.filter_by(title="Recipe 2").first()
    recipe3 = Recipe.query.filter_by(title="Recipe 3").first()
    recipe4 = Recipe.query.filter_by(title="Recipe 4").first()
    review1 = Review(user=user1, recipe=recipe1, rating=5, feedback="Feedback 1")
    review2 = Review(user=user2, recipe=recipe2, rating=4, feedback="Feedback 2")
    review3 = Review(user=user1, recipe=recipe3, rating=3, feedback="Feedback 3")
    review4 = Review(user=user2, recipe=recipe4, rating=2, feedback="Feedback 4")
    db.session.add(review1)
    db.session.add(review2)
    db.session.add(review3)
    db.session.add(review4)
    db.session.commit()
    click.echo("Added review test data.")


@click.command("clear-test-data")
@with_appcontext
def clear_test_data_command():
    """
    Clear test data from all tables.
    """
    try:
        db.session.query(Review).delete()
        db.session.query(RecipeIngredientQty).delete()
        db.session.query(Ingredient).delete()
        db.session.query(Recipe).delete()
        db.session.query(User).delete()
        db.session.commit()
        click.echo("Cleared test data from all tables.")
    except (SQLAlchemyError) as e:
        db.session.rollback()
        click.echo(f'Error clearing data from database: {e}')
