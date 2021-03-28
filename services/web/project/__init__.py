
from flask import Flask, jsonify, render_template, Response
from flask_sqlalchemy import SQLAlchemy
import os
# import flask LoginManager
from flask_login import LoginManager
# import flask_assets
from flask_assets import Environment, Bundle
# import compile assets from assets.py
from .assets import compile_static_assets
# Importing Flask Principal
from flask_principal import Principal, Permission, RoleNeed

port = int(os.environ.get("PORT", 5000))

# activate SQLAlchemy
db = SQLAlchemy()
# set login manager name from flask_login
login_manager = LoginManager()

# setup Flask Principal
principals = Principal()
# setting up a sponsor role from Flask Principal
sponsor_role = RoleNeed('sponsor')
# setting up a sponsor permission
sponsor_permission = Permission(sponsor_role)


def create_app():
    # construct core app object, __name__ is the default value.
    app = Flask(__name__)
    # pull the config file, per flask documentation
    # Application configuration
    app.config.from_object("project.config.Config")
    # auto reload templates
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    # Set environment for assets
    assets = Environment()

    # initialize database plugin
    db.init_app(app)

    # initialize asset plugin
    assets.init_app(app)

    # initialize login manager plugin
    login_manager.init_app(app)

    # initialize principals/roles plugin
    principals.init_app(app)

    # initialize routes
    with app.app_context():
        from . import routes
        from . import auth
        from .assets import compile_static_assets
        # Register Blueprints
        app.register_blueprint(routes.main_bp)
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(routes.sponsor_bp)
        app.register_blueprint(routes.editor_bp)

        # import model class
        from . import models

        # Create Database Models
        db.create_all()

        # Compile static assets
        compile_static_assets(assets)
      
    return app

# Physically create the app now
app = create_app()

from .models import db, Document, User, Retention
# python shell context processor
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Document': Document, 'Retention': Retention}

if __name__ == "__main__":
   app.run(host='0.0.0.0',port=port)
