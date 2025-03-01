from werkzeug.routing import BaseConverter
from werkzeug.exceptions import NotFound

from cookbookapp.models import *

class ReviewConverter(BaseConverter):
    def to_python(self, value):
        db_review = Review.query.filter_by(review_id=value).first()
        if db_review is None:
            raise NotFound
        return db_review

    def to_url(self, value):
        return str(value)
    
class UserConverter(BaseConverter):
    def to_python(self, username):
        db_user = User.query.filter_by(username=username).first()
        if db_user is None:
            raise NotFound
        return db_user

    def to_url(self, db_user):
        return db_user.username

    
class IngredientConverter(BaseConverter):
    def to_python(self, ingredient_name):
        db_ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
        if db_ingredient is None:
            raise NotFound
        return db_ingredient

    def to_url(self, db_ingredient):
        return db_ingredient.name