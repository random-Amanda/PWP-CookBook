import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from cookbookapp.config import Config

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, "pwp_cb.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    print(app.instance_path)
    
    # if test_config is None:
    #     app.config.from_pyfile("config.py", silent=True)
    # else:
    #     app.config.from_mapping(test_config)
        
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass
    
    db.init_app(app)

    from . import models
    from . import api
    from cookbookapp.utils import ReviewConverter, IngredientConverter

    app.cli.add_command(models.init_db_command)
    app.cli.add_command(models.drop_db_command)
    app.cli.add_command(models.gen_test_data_command)
    app.cli.add_command(models.clear_test_data_command)

    app.url_map.converters["review"] = ReviewConverter
    app.url_map.converters["ingredient"] = IngredientConverter
    
    app.register_blueprint(api.api_bp)

    # with app.app_context():  # Create tables inside the app context
    #     db.create_all()
    
    return app