import os

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_smorest import Api

from db import db
from resources.items import blp as ItemBlueprint
from resources.stores import blp as StoreBlueprint
from resources.tags import blp as TagBlueprint
from resources.users import blp as UserBlueprint


def create_app(db_url=None):
    app = Flask(__name__)
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['API_TITLE'] = 'Stores REST API'
    app.config['API_VERSION'] = 'v1'
    app.config['OPENAPI_VERSION'] = '3.0.3'
    app.config['OPENAPI_URL_PREFIX'] = '/'
    app.config['OPENAPI_SWAGGER_UI_PATH'] = '/'
    app.config['OPENAPI_SWAGGER_UI_URL'] = (
        'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
    )

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or os.getenv(
        'DATABASE_URL', 'sqlite:///data.db'
    )
    app.config['PROPAGATE_EXCEPTIONS'] = True

    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')
    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)
    return app
