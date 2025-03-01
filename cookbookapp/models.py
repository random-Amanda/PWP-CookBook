import click
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, Engine
from cookbookapp import db


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)

    recipes = db.relationship('Recipe', back_populates='user')
    reviews = db.relationship('Review', back_populates='user')

    def serialize(self):
        return {
            "user_id": self.user_id,
            "email": self.email,
            "username": self.username,
            "password": self.password
        }
    
    def deserialize(data):
        return User(
            email=data.get("email"),
            username=data.get("username"),
            password=data.get("password")
        )
    
    @staticmethod
    def get_schema():
        return {
            "type": "object",
            "properties": {
                "email": {"type": "string"},
                "username": {"type": "string"},
                "password": {"type": "string"}
            },
            "required": ["email", "username", "password"]
        }

class Recipe(db.Model):
    __tablename__ = 'recipe'
    recipe_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='SET NULL'), nullable=True)
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
        return {
            "recipe_id": self.recipe_id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "steps": self.steps,
            "preparation_time": self.preparation_time,
            "cooking_time": self.cooking_time,
            "serving": self.serving
        }
    
    def deserialize(data):
        return Recipe(
            user_id=data.get("user_id"),
            title=data.get("title"),
            description=data.get("description"),
            steps=data.get("steps"),
            preparation_time=data.get("preparation_time"),
            cooking_time=data.get("cooking_time"),
            serving=data.get("serving")
        )
    
    @staticmethod
    def get_schema():
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
    __tablename__ = 'review'
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='SET NULL'), nullable=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id', ondelete='SET NULL'), nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.Text)

    recipe = db.relationship('Recipe', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')

    def serialize(self):
        return {
            "review_id": self.review_id,
            "user_id": self.user_id,
            "recipe_id": self.recipe_id,
            "rating": self.rating,
            "feedback": self.feedback
        }
    
    def deserialize(data):
        return Review(
            user_id=data.get("user_id"),
            recipe_id=data.get("recipe_id"),
            rating=data.get("rating"),
            feedback=data.get("feedback")
        )
    
    @staticmethod
    def get_schema():
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
    __tablename__ = 'ingredient'
    ingredient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)

    recipeIngredient = db.relationship('RecipeIngredientQty', back_populates='ingredient')

    def serialize(self):
        return {
            "ingredient_id": self.ingredient_id,
            "name": self.name,
            "description": self.description
        }
    
    def deserialize(data):
        return Ingredient(
            name=data.get("name"),
            description=data.get("description")
        )
    
    @staticmethod
    def get_schema():
        return {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "description": {"type": "string"}
            },
            "required": ["name"]
        }
    
class RecipeIngredientQty(db.Model):
    __tablename__ = 'recipe_ingredient_qty'
    qty_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id', ondelete='SET NULL'), nullable=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.ingredient_id', ondelete='SET NULL'), nullable=True)
    qty = db.Column(db.Float, nullable=False)
    metric = db.Column(db.String(20), nullable=False)

    ingredient = db.relationship('Ingredient', back_populates='recipeIngredient')
    recipe = db.relationship('Recipe', back_populates='recipeIngredient')

    def serialize(self):
        return {
            'qty_id': self.qty_id,
            'recipe_id': self.recipe_id,
            'ingredient_id': self.ingredient_id,
            'qty': self.qty,
            'metric': self.metric
        }
    
    def deserialize(data):
        return RecipeIngredientQty(
            recipe_id=data.get("recipe_id"),
            ingredient_id=data.get("ingredient_id"),
            qty=data.get("qty"),
            metric=data.get("metric")
        )

    @staticmethod
    def get_schema():
        return {
            "type": "object",
            "properties": {
                "recipe_id": {"type": "integer"},
                "ingredient_id": {"type": "integer"},
                "qty": {"type": "number"},
                "metric": {"type": "string"}
            },
            "required": ["recipe_id", "ingredient_id", "qty", "metric"]
        }
    
@click.command("init-db")
@with_appcontext
def init_db_command():
    db.create_all()
    click.echo("Initialized the database.")

@click.command("drop-db")
@with_appcontext   
def drop_db_command():
    db.drop_all()
    click.echo("Dropped the database.")

@click.command("gen-test-data")
@with_appcontext
def gen_test_data_command():

    try:
        user1 = User(email="user1@test.com", username="user1", password="user1")
        user2 = User(email="user2@test.com", username="user2", password="user2") 
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        click.echo("Added user test data.")

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

        recipe1 = Recipe(user=user1, title="Recipe 1", description="Description 1", steps=' {"step1": "step 1", "step2": "step 2"} ', preparation_time="10 mins", cooking_time="20 mins", serving=2)
        recipe2 = Recipe(user=user2, title="Recipe 2", description="Description 2", steps=' {"step1": "step 1", "step2": "step 2"}  ', preparation_time="15 mins", cooking_time="25 mins", serving=1)
        recipe3 = Recipe(user=user1, title="Recipe 3", description="Description 3", steps=' {"step1": "step 1", "step2": "step 2"}  ', preparation_time="20 mins", cooking_time="30 mins", serving=1)
        recipe4 = Recipe(user=user2, title="Recipe 4", description="Description 4", steps=' {"step1": "step 1", "step2": "step 2"}  ', preparation_time="25 mins", cooking_time="35 mins", serving=3)
        db.session.add(recipe1)
        db.session.add(recipe2)
        db.session.add(recipe3)
        db.session.add(recipe4)
        db.session.commit()
        click.echo("Added recipe test data.")

        recipeIngredientQty1 = RecipeIngredientQty(recipe=recipe1, ingredient=ingredient1, qty=100, metric="g")
        recipeIngredientQty2 = RecipeIngredientQty(recipe=recipe1, ingredient=ingredient2, qty=200, metric="g")
        recipeIngredientQty3 = RecipeIngredientQty(recipe=recipe2, ingredient=ingredient1, qty=500, metric="g")
        recipeIngredientQty4 = RecipeIngredientQty(recipe=recipe2, ingredient=ingredient3, qty=3, metric="tablespoon")
        recipeIngredientQty5 = RecipeIngredientQty(recipe=recipe2, ingredient=ingredient4, qty=40, metric="ml")
        recipeIngredientQty6 = RecipeIngredientQty(recipe=recipe3, ingredient=ingredient1, qty=500, metric="g")
        recipeIngredientQty7 = RecipeIngredientQty(recipe=recipe3, ingredient=ingredient2, qty=500, metric="g")
        recipeIngredientQty8 = RecipeIngredientQty(recipe=recipe4, ingredient=ingredient1, qty=200, metric="g")
        recipeIngredientQty9 = RecipeIngredientQty(recipe=recipe4, ingredient=ingredient2, qty=500, metric="g")
        recipeIngredientQty10 = RecipeIngredientQty(recipe=recipe4, ingredient=ingredient4, qty=150, metric="ml")
        db.session.add(recipeIngredientQty1)
        db.session.add(recipeIngredientQty2)
        db.session.add(recipeIngredientQty3)
        db.session.add(recipeIngredientQty4)
        db.session.add(recipeIngredientQty5)
        db.session.add(recipeIngredientQty6)
        db.session.add(recipeIngredientQty7)
        db.session.add(recipeIngredientQty8)
        db.session.add(recipeIngredientQty9)
        db.session.add(recipeIngredientQty10)
        db.session.commit()
        click.echo("Added recipe ingredient test data.")

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

        click.echo("Generated test data for all tables.")
    except Exception as e:
        db.session.rollback()
        click.echo(f'Error generating data: {e}')
        raise e

@click.command("clear-test-data")
@with_appcontext
def clear_test_data_command():
    try:
        db.session.query(Review).delete()
        db.session.query(RecipeIngredientQty).delete()
        db.session.query(Ingredient).delete()
        db.session.query(Recipe).delete()
        db.session.query(User).delete()
        db.session.commit()
        click.echo("Cleared test data from all tables.")
    except Exception as e:
        db.session.rollback()
        click.echo(f'Error clearing data from database: {e}')
    
