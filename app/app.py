from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask("cookbook")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_timestamp = db.Column(db.Date, nullable=False)
    updated_timestamp = db.Column(db.Date, nullable=False)

    recipes = db.relationship(
        'Recipe', backref='author', lazy=True, cascade="all, delete-orphan")
    reviews = db.relationship(
        'Review', backref='reviewer', lazy=True, cascade="all, delete-orphan")


class Recipe(db.Model):
    recipe_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.user_id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    steps = db.Column(db.Text, nullable=False)
    preparation_time = db.Column(db.String(20), nullable=False)  # 20 minutes
    cooking_time = db.Column(db.String(20), nullable=False)
    serving = db.Column(db.Integer, nullable=False)
    created_timestamp = db.Column(db.Date, nullable=False)
    updated_timestamp = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(17), nullable=False)
    approver_id = db.Column(db.Integer, nullable=False)

    reviews = db.relationship(
        'Review', backref='recipe', lazy=True, cascade="all, delete-orphan")
    ingredients = db.relationship(
        'RecipeIngredientQty', backref='recipe', lazy=True, cascade="all, delete-orphan")
    cuisines = db.relationship(
        'RecipeCuisine', backref='recipe', lazy=True, cascade="all, delete-orphan")
    nutritions = db.relationship(
        'RecipeNutrition', backref='recipe', lazy=True, cascade="all, delete-orphan")


class Review(db.Model):
    review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.user_id', ondelete='CASCADE'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        'recipe.recipe_id', ondelete='CASCADE'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.String(1000))
    created_timestamp = db.Column(db.Date, nullable=False)
    updated_timestamp = db.Column(db.Date, nullable=False)


class Ingredient(db.Model):
    ingredient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    approver_id = db.Column(db.Integer, nullable=False)
    created_timestamp = db.Column(db.Date, nullable=False)
    updated_timestamp = db.Column(db.Date, nullable=False)


class RecipeIngredientQty(db.Model):
    qty_id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        'recipe.recipe_id', ondelete='CASCADE'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey(
        'ingredient.ingredient_id', ondelete='CASCADE'), nullable=False)


class Cuisine(db.Model):
    cuisine_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    approver_id = db.Column(db.Integer, nullable=False)
    created_timestamp = db.Column(db.Date, nullable=False)
    updated_timestamp = db.Column(db.Date, nullable=False)


class RecipeCuisine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        'recipe.recipe_id', ondelete='CASCADE'), nullable=False)
    cuisine_id = db.Column(db.Integer, db.ForeignKey(
        'cuisine.cuisine_id', ondelete='CASCADE'), nullable=False)


class Nutrition(db.Model):
    nutrition_id = db.Column(db.Integer, primary_key=True)
    benefits = db.Column(db.Text, nullable=False)
    approver_id = db.Column(db.Integer, nullable=False)
    created_timestamp = db.Column(db.Date, nullable=False)
    updated_timestamp = db.Column(db.Date, nullable=False)


class RecipeNutrition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        'recipe.recipe_id', ondelete='CASCADE'), nullable=False)
    nutrition_id = db.Column(db.Integer, db.ForeignKey(
        'nutrition.nutrition_id', ondelete='CASCADE'), nullable=False)


class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True)


class Image(db.Model):
    image_id = db.Column(db.Integer, primary_key=True)
