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
    # type = db.Column(db.String(15), nullable=False) # removed based on the suggestion
    email = db.Column(db.String(200), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    # created_timestamp = db.Column(db.Date, nullable=False) # removed based on the suggestion
    # updated_timestamp = db.Column(db.Date, nullable=True) # removed based on the suggestion
    recipes = db.relationship(
        'Recipe', back_populates='user') # set null to child when parent is deleted
    reviews = db.relationship(
        'Review', back_populates='user') # set null to child when parent is deleted


class Recipe(db.Model):
    __tablename__ = 'recipe'
    recipe_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.user_id', ondelete='SET NULL'), nullable=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    steps = db.Column(db.Text, nullable=False) # steps in json format
    preparation_time = db.Column(db.String(200), nullable=False)
    cooking_time = db.Column(db.String(200), nullable=False)
    serving = db.Column(db.Integer, nullable=False)
    # created_timestamp = db.Column(db.Date, nullable=False) # removed based on the suggestion
    # updated_timestamp = db.Column(db.Date, nullable=True) # removed based on the suggestion
    # status = db.Column(db.String(17), nullable=False) # removed based on the suggestion
    # approver_id = db.Column(db.Integer, nullable=True) # removed based on the suggestion

    user = db.relationship('User', back_populates='recipes')
    reviews = db.relationship('Review', back_populates='recipe')
    recipeIngredient = db.relationship(
        'RecipeIngredientQty', back_populates='recipe')

    cuisines = db.relationship(
        'Cuisine', secondary=recipe_cuisine, back_populates='recipes') # keep feilds but not used
    nutritions = db.relationship(
        'Nutrition', secondary=recipe_nutrition, back_populates='recipes') # keep feilds but not used


class Review(db.Model):
    __tablename__ = 'review'
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.user_id', ondelete='SET NULL'), nullable=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        'recipe.recipe_id', ondelete='SET NULL'), nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.Text)
    # created_timestamp = db.Column(db.Date, nullable=False) # removed based on the suggestion
    # updated_timestamp = db.Column(db.Date, nullable=True) # removed based on the suggestion

    recipe = db.relationship('Recipe', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')


class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    ingredient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    # approver_id = db.Column(db.Integer, nullable=True) # removed based on the suggestion
    # created_timestamp = db.Column(db.Date, nullable=False) # removed based on the suggestion
    # updated_timestamp = db.Column(db.Date, nullable=True) # removed based on the suggestion

    recipeIngredient = db.relationship(
        'RecipeIngredientQty', back_populates='ingredient')


class RecipeIngredientQty(db.Model):
    __tablename__ = 'recipe_ingredient_qty'
    qty_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        'recipe.recipe_id', ondelete='SET NULL'), nullable=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey(
        'ingredient.ingredient_id', ondelete='SET NULL'), nullable=True)
    qty = db.Column(db.Float, nullable=False)
    metric = db.Column(db.String(20), nullable=False)

    ingredient = db.relationship(
        'Ingredient', back_populates='recipeIngredient')
    recipe = db.relationship('Recipe', back_populates='recipeIngredient')


# do not use feedback from the lecturer
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

# do not use feedback from the lecturer
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

# do not use feedback from the lecturer fornow
class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    link = db.Column(db.Text, nullable=False)

# do not use feedback from the lecturer fornow
class Image(db.Model):
    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    link = db.Column(db.Text, nullable=False)


# How to populate the database with data
# 1. Create the database
# 2. Create the tables
# 3. Insert data into the tables
# 4. Commit the transaction

# Insert data into the tables
# 1. Create the objects
# 2. Add the objects to the session
# 3. Commit the transaction
# 4. Close

# User Table
user1 = User(email="user1@test.com", username="user1", password="user1")
user2 = User(email="user2@test.com", username="user2", password="user2") 

# Ingredient Table
ingredient1 = Ingredient(name="Ingredient 1", description="Description 1")
ingredient2 = Ingredient(name="Ingredient 2", description="Description 2")
ingredient3 = Ingredient(name="Ingredient 3", description="Description 3")
ingredient4 = Ingredient(name="Ingredient 4", description="Description 4")

# Recipe Table
recipe1 = Recipe(user=user1, title="Recipe 1", description="Description 1", steps=' {"step1": "step 1", "step2": "step 2"} ', preparation_time="10 mins", cooking_time="20 mins", serving=2)
recipe2 = Recipe(user=user2, title="Recipe 2", description="Description 2", steps=' {"step1": "step 1", "step2": "step 2"}  ', preparation_time="15 mins", cooking_time="25 mins", serving=1)
recipe3 = Recipe(user=user1, title="Recipe 3", description="Description 3", steps=' {"step1": "step 1", "step2": "step 2"}  ', preparation_time="20 mins", cooking_time="30 mins", serving=1)
recipe4 = Recipe(user=user2, title="Recipe 4", description="Description 4", steps=' {"step1": "step 1", "step2": "step 2"}  ', preparation_time="25 mins", cooking_time="35 mins", serving=3)

# RecipeIngredientQty Table
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

# Review Table
review1 = Review(user=user1, recipe=recipe1, rating=5, feedback="Feedback 1")
review2 = Review(user=user2, recipe=recipe2, rating=4, feedback="Feedback 2")
review3 = Review(user=user1, recipe=recipe3, rating=3, feedback="Feedback 3")
review4 = Review(user=user2, recipe=recipe4, rating=2, feedback="Feedback 4")


db.session.add(user1)
db.session.add(user2)
db.session.add(ingredient1)
db.session.add(ingredient2)
db.session.add(ingredient3)
db.session.add(ingredient4)
db.session.add(recipe1)
db.session.add(recipe2)
db.session.add(recipe3)
db.session.add(recipe4)
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
db.session.add(review1)
db.session.add(review2)
db.session.add(review3)
db.session.add(review4)
db.session.commit()


