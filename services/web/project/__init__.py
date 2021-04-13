
from flask import Flask, jsonify, render_template, Response
from flask_sqlalchemy import SQLAlchemy
import os
# import flask LoginManager
from flask_login import LoginManager, current_user
# import flask_assets
from flask_assets import Environment, Bundle
# import compile assets from assets.py
from .assets import compile_static_assets
# Importing Flask Principal
from flask_principal import identity_loaded, Principal, Permission, UserNeed, RoleNeed
# individual document access permission
from .principalmanager import EditDocumentNeed

# for printing to console
import sys

port = int(os.environ.get("PORT", 5000))

# activate SQLAlchemy
db = SQLAlchemy()
# set login manager name from flask_login
login_manager = LoginManager()

# setup Flask Principal
principals = Principal()
# Permissions and Needs
# setting up a sponsor role from Flask Principal
sponsor_role = RoleNeed('sponsor')
# setting up a sponsor permission
sponsor_permission = Permission(sponsor_role)
# setting up an editor role from Flask Principal
editor_role = RoleNeed('editor')
# setting up an editor permission
editor_permission = Permission(editor_role)
# setting up admin roleneed
admin_role = RoleNeed('admin')
# setting up an admin permission
admin_permission = Permission(admin_role)
# setting up admin roleneed
approved_role = RoleNeed('approved')
# setting up an approved permission
approved_permission = Permission(approved_role)
# setting up admin roleneed
notapproved_role = RoleNeed('notapproved')
# setting up an approved permission
notapproved_permission = Permission(notapproved_role)



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
        app.register_blueprint(routes.admin_bp)

        # import model class
        from . import models

        # Create Database Models
        db.create_all()

        # Compile static assets
        compile_static_assets(assets)
      
    return app

# Physically create the app now
app = create_app()


# Identity Loading Factory from flask_principal
# identity_loaded adds any additional information to the Identity instance such as roles.
# then, needs are added and brought along with that user for various permissions functions
# Signal sent when the identity has been initialised for a request.
# @identity_loaded is a decorator, connect_via sender "app" with weak signals via blinker
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):

    # Set the identity user object
    # basically pass current_user object to identity.user
    identity.user = current_user

    # Add the UserNeed to the identity
    # ensure current_user has attribute identity "id"
    if hasattr(current_user, 'id'):
        # specifically, need to have current_user.id
        # Query user type given user.id
        # printing the fact that we are querying db
        print('Querying Database for user_type!', file=sys.stderr)
        current_user_type = User.query.filter(User.id==current_user.id)[0].user_type

        print('Querying Database for user_status!', file=sys.stderr)
        current_user_status = User.query.filter(User.id==current_user.id)[0].user_status

        # print userid to console
        print('Providing ID: ',current_user.id,' ...to Identity', file=sys.stderr)
        # provide userid to identity
        identity.provides.add(UserNeed(current_user.id))

        # print user_type to console
        print('Providing Role: ',current_user_type,' ...to Identity', file=sys.stderr)
        # provide user_type to identity
        identity.provides.add(RoleNeed(current_user_type))

        # print user_status to console
        print('Providing Role: ',current_user_status,' ...to Identity', file=sys.stderr)
        # provide user_type to identity
        identity.provides.add(RoleNeed(current_user_status))

        # this is set up in such a way that multiple needs can be added to the same user
        needs = []
        
        # append approved or notapproved roles depending upon status
        # approved status role - pending and rejected goes to notapproved
        if current_user_status == 'approved':
            # append approved role to needs
            needs.append(approved_role)
        elif current_user_status == 'pending' or current_user_status == 'rejected':
            # append approved role to needs
            needs.append(notapproved_role)

        # append sponsor and editor roles depending upon user
        # if current_user_type is sponsor
        if current_user_type == 'sponsor':
            # add sponsor_role, RoleNeed to needs
            needs.append(sponsor_role)
            # query user's documents, filter documents by current sponsor user
            # printing the fact that we are querying db
            print('Querying Database for document_ids!', file=sys.stderr)
            document_objects = db.session.query(Retention.sponsor_id,User.id,Retention.document_id,).join(Retention, User.id==Retention.sponsor_id).join(Document, Document.id==Retention.document_id).order_by(Retention.sponsor_id).filter(Retention.sponsor_id == current_user.id)
            # get a count of the document objects
            document_count = document_objects.count()
            # blank list to fill with documentid's
            document_id_list=[]
            # loop through document objects to generate filled document_id_list
            for counter in range(0,document_count):
                # loop through document objects and append to list
                document_id_list.append(document_objects[counter].document_id)
                # provide the need mapping to the document for each document
                identity.provides.add(EditDocumentNeed(str(document_objects[counter].document_id)))
            # after for loop, show document id's appended to needs
            print('appended document_ids to needs : ',document_id_list, file=sys.stderr)
        # if current_user_type is editor
        elif current_user_type == 'editor':
            # add editor_role, RoleNeed to needs
            needs.append(editor_role)
            # query user's documents, filter documents by current sponsor user
            # printing the fact that we are querying db
            print('Querying Database for document_ids!', file=sys.stderr)
            document_objects = db.session.query(Retention.editor_id,User.id,Retention.document_id,).join(Retention, User.id==Retention.editor_id).join(Document, Document.id==Retention.document_id).order_by(Retention.editor_id).filter(Retention.editor_id == current_user.id)
            # get a count of the document objects
            document_count = document_objects.count()
            # blank list to fill with documentid's
            document_id_list=[]
            # loop through document objects to generate filled document_id_list
            for counter in range(0,document_count):
                # loop through document objects and append to list
                document_id_list.append(document_objects[counter].document_id)
                # provide the need mapping to the document for each document
                identity.provides.add(EditDocumentNeed(str(document_objects[counter].document_id)))
            # after for loop, show document id's appended to needs
            print('appended document_ids to needs : ',document_id_list, file=sys.stderr)

        # print everything appended to needs, documents and others
        print('appended to needs : ',needs, file=sys.stderr)
        # add all of the listed needs to current_user

        for n in needs:
            identity.provides.add(n)


# create shell context processor
from .models import db, Document, User, Retention
# python shell context processor
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Document': Document, 'Retention': Retention}

# Apply Content Security Policy to All 
@app.after_request
def add_security_headers(resp):
    resp.headers['Content-Security-Policy']='default-src \'self\''
    return resp


if __name__ == "__main__":
   app.run(host='0.0.0.0',port=port)
