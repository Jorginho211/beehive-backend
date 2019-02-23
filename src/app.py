from flask import Flask, g #flask
from flasgger import Swagger
from flasgger.utils import swag_from
from .config import app_config #app config
from .exts import db, app
from .api.devices import devices_api

def register_extensions():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/beehive'
    app.app_context().push()
    db.init_app(app)

def register_apis():
    app.register_blueprint(devices_api, url_prefix='/api/v1/') #registering devices

# Creating app
def create_app(env_name):
    """Create app
    Keyword arguments:
    env_name -- enviroment ('development or production')
    """

    # app init
    app.config.from_object(app_config[env_name])
    app.config['SWAGGER'] = {
        'title': 'Beehive API'
    }
    # Swagger init
    Swagger(app)
    
    register_extensions()
    register_apis()
    
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    return app