"""Cook-Book application.

This module initializes and configures the Flask application, including the
SQLAlchemy database, caching, CLI commands, and URL converters.
"""
import os
from flask import Flask
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

# from cookbookapp.config import Config

db = SQLAlchemy()
cache = Cache()
# cache = Cache(config={
#     'CACHE_TYPE': 'simple',
#     'CACHE_DEFAULT_TIMEOUT': 300
# })

def create_app(test_config=None):
    """
    Create and configure the Flask application.

    :param test_config: Optional dictionary with configuration values for testing.
    :return: Configured Flask application instance.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, "pwp_cb.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        # CACHE_TYPE="FileSystemCache",
        # CACHE_DIR=os.path.join(app.instance_path, "cache"),
        CACHE_TYPE="simple",
        CACHE_DEFAULT_TIMEOUT=36000
    )
    print(app.instance_path)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    cache.init_app(app)

    # Initialize Swagger with security scheme
    Swagger(app,
            template={
                "swagger": "2.0",
                "basePath": "/api",
                "info": {
                    "title": "Cookbook API",
                    "description": """This is a Cookbook API Server that provides a 
                    comprehensive set of endpoints for managing cooking recipes, 
                    ingredients, and user interactions. The API is designed to facilitate 
                    recipe management, ingredient handling, and user reviews.

You can find out more about this API at [https://github.com/random-Amanda/PWP-CookBook]
(https://github.com/random-Amanda/PWP-CookBook). 
The API follows RESTful principles and implements proper authentication using API keys.

Some useful links:
- [The Cookbook Repository](https://github.com/random-Amanda/PWP-CookBook)
- [API Documentation](http://localhost:5000/apidocs/)
- [API Specification](http://localhost:5000/apispec_1.json)

Key Features:
- Recipe Management: Create, read, update, and delete recipes
- Ingredient Handling: Manage ingredients and their quantities
- User Reviews: Handle user feedback and ratings

Getting Started:
1. Initialize the database: `flask init-db`
2. Generate API key: `flask init-apikey`
3. Add test data: `flask gen-test-data`

For support or questions, please contact the development team.""",
                             "version": "1.0.0"
                         },
                         "securityDefinitions": {
                             "ApiKeyAuth": {
                                 "type": "apiKey",
                                 "in": "header",
                                 "name": "API-KEY",
                                 "description": "API key for authentication"
                             }
                         }
                     })

    from . import models
    from . import api
    from cookbookapp.utils import (
        ReviewConverter,
        UserConverter,
        IngredientConverter,
        RecipeConverter)

    app.cli.add_command(models.init_db_command)
    app.cli.add_command(models.drop_db_command)
    app.cli.add_command(models.init_apikey_command)
    app.cli.add_command(models.gen_test_data_command)
    app.cli.add_command(models.clear_test_data_command)

    app.url_map.converters["review"] = ReviewConverter
    app.url_map.converters["user"] = UserConverter
    app.url_map.converters["ingredient"] = IngredientConverter
    app.url_map.converters["recipe"] = RecipeConverter
    # app.url_map.converters["ingredientqty"] = RecipeIngredientQtyConverter

    app.register_blueprint(api.api_bp)

    with app.app_context():  # Create tables inside the app context
        db.create_all()

    return app
