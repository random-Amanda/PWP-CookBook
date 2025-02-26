from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pwp_cb.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Many to Many Relationship
recipe_nutrition = db.Table("recipe_nutrition",
                            db.Column("recipe_id", db.Integer, db.ForeignKey(
                                "recipe.recipe_id"), primary_key=True),
                            db.Column("nutrition_id", db.Integer, db.ForeignKey(
                                "nutrition.nutrition_id"), primary_key=True)
                            )


recipe_cuisine = db.Table("recipe_cuisine",
                          db.Column("recipe_id", db.Integer, db.ForeignKey(
                              "recipe.recipe_id"), primary_key=True),
                          db.Column("cuisine_id", db.Integer, db.ForeignKey(
                              "cuisine.cuisine_id"), primary_key=True)
                          )

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(500), nullable=False)
    created_timestamp = db.Column(db.Date, nullable=False)
    updated_timestamp = db.Column(db.Date, nullable=True)

    recipes = db.relationship(
        'Recipe', back_populates='user', cascade="all, delete-orphan")
    reviews = db.relationship(
        'Review', back_populates='user', cascade="all, delete-orphan")


class Recipe(db.Model):
    __tablename__ = 'recipe'
    recipe_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.user_id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    steps = db.Column(db.Text, nullable=False)
    preparation_time = db.Column(db.String(200), nullable=False)
    cooking_time = db.Column(db.String(200), nullable=False)
    serving = db.Column(db.Integer, nullable=False)
    created_timestamp = db.Column(db.Date, nullable=False)
    updated_timestamp = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(17), nullable=False)
    approver_id = db.Column(db.Integer, nullable=True)

    user = db.relationship('User', back_populates='recipes')
    reviews = db.relationship('Review', back_populates='recipe')
    recipeIngredient = db.relationship(
        'RecipeIngredientQty', back_populates='recipe')

    cuisines = db.relationship(
        'Cuisine', secondary=recipe_cuisine, back_populates='recipes')
    nutritions = db.relationship(
        'Nutrition', secondary=recipe_nutrition, back_populates='recipes')


class Review(db.Model):
    __tablename__ = 'review'
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.user_id', ondelete='CASCADE'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        'recipe.recipe_id', ondelete='CASCADE'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.Text)
    created_timestamp = db.Column(db.Date, nullable=False)
    updated_timestamp = db.Column(db.Date, nullable=True)

    recipe = db.relationship('Recipe', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')


class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    ingredient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    approver_id = db.Column(db.Integer, nullable=True)
    created_timestamp = db.Column(db.Date, nullable=False)
    updated_timestamp = db.Column(db.Date, nullable=True)

    recipeIngredient = db.relationship(
        'RecipeIngredientQty', back_populates='ingredient')


class RecipeIngredientQty(db.Model):
    __tablename__ = 'recipe_ingredient_qty'
    qty_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        'recipe.recipe_id', ondelete='CASCADE'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey(
        'ingredient.ingredient_id', ondelete='CASCADE'), nullable=False)
    qty = db.Column(db.Float, nullable=False)
    metric = db.Column(db.String(20), nullable=False)

    ingredient = db.relationship(
        'Ingredient', back_populates='recipeIngredient')
    recipe = db.relationship('Recipe', back_populates='recipeIngredient')


class Cuisine(db.Model):
    __tablename__ = 'cuisine'
    cuisine_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    approver_id = db.Column(db.Integer, nullable=True)
    created_timestamp = db.Column(db.Date, nullable=False)
    updated_timestamp = db.Column(db.Date, nullable=True)

    recipes = db.relationship(
        'Recipe', secondary=recipe_cuisine, back_populates='cuisines')


# class RecipeCuisine(db.Model):
#     __tablename__ = 'recipe_cuisine'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     recipe_id = db.Column(db.Integer, db.ForeignKey(
#         'recipe.recipe_id', ondelete='CASCADE'), nullable=False)
#     cuisine_id = db.Column(db.Integer, db.ForeignKey(
#         'cuisine.cuisine_id', ondelete='CASCADE'), nullable=False)

#     cuisine = db.relationship('Cuisine', back_populates='recipeCuisine')
#     recipe = db.relationship('Recipe', back_populates='recipeCuisine')


class Nutrition(db.Model):
    __tablename__ = 'nutrition'
    nutrition_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    benefits = db.Column(db.Text, nullable=False)
    approver_id = db.Column(db.Integer, nullable=True)
    created_timestamp = db.Column(db.Date, nullable=False)
    updated_timestamp = db.Column(db.Date, nullable=True)
    
    recipes = db.relationship(
        'Recipe', secondary=recipe_nutrition, back_populates='nutritions')


# class RecipeNutrition(db.Model):
#     __tablename__ = 'recipe_nutrition'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     recipe_id = db.Column(db.Integer, db.ForeignKey(
#         'recipe.recipe_id', ondelete='CASCADE'), nullable=False)
#     nutrition_id = db.Column(db.Integer, db.ForeignKey(
#         'nutrition.nutrition_id', ondelete='CASCADE'), nullable=False)

#     nutrition = db.relationship(
#         'Nutrition', back_populates='recipeNutrition')
#     recipe = db.relationship('Recipe', back_populates='recipeNutrition')


class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    link = db.Column(db.Text, nullable=False)


class Image(db.Model):
    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    link = db.Column(db.Text, nullable=False)
