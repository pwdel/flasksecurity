"""Logged-in page routes."""
from flask import Blueprint, redirect, render_template, flash, request, session, url_for
from flask import g, current_app, abort, request
from flask_login import current_user, login_required
from flask_login import logout_user
from .forms import DocumentForm
from .models import db, Document, User, Retention
from wtforms_sqlalchemy.orm import QuerySelectField
from . import sponsor_permission, editor_permission
# for identifitaction and permission management
from flask_principal import Identity, identity_changed, AnonymousIdentity
# for printing system messages
import sys


# Blueprint Configuration
# we define __name__ as the main blueprint, and the templates/static folder.
main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

# Sponsor Blueprint
sponsor_bp = Blueprint(
    'sponsor_bp', __name__,
    template_folder='templates_sponsors',
    static_folder='static'
)

# Editor Blueprint
editor_bp = Blueprint(
    'editor_bp', __name__,
    template_folder='templates_editors',
    static_folder='static'
)


# when any user goes to /, they get redirected to /login
@main_bp.route('/', methods=['GET'])
@login_required
# redirect to login page if logged in, to be re-routed to appropriate location
def logindefault():
    # redirect to login page
    return redirect(url_for('auth_bp.login'))

# ---------- sponsor user routes ----------

@sponsor_bp.route("/sponsor/logout")
@login_required
@sponsor_permission.require(http_exception=403)
def logoutsponsor():
    """User log-out logic."""
    logout_user()
    # tell flask principal the user is annonymous
    identity_changed.send(current_app._get_current_object(),identity=AnonymousIdentity())
    # print annonymousidentity to console
    identity_object = AnonymousIdentity()
    # printing identity_object to console for verification
    print('Sent: ',identity_object,' ...to current_app', file=sys.stderr)
    return redirect(url_for('auth_bp.login'))

@sponsor_bp.route('/sponsor/dashboard', methods=['GET','POST'])
@login_required
@sponsor_permission.require(http_exception=403)
def dashboard_sponsor():
    """Logged-in User Dashboard."""
    return render_template(
        'dashboard_sponsor.jinja2',
        title='Sponsor Dashboard',
        template='layout',
        body="Welcome to the Sponsor Dashboard."
    )

@sponsor_bp.route('/sponsor/newdocument', methods=['GET','POST'])
@login_required
@sponsor_permission.require(http_exception=403)
def newdocument_sponsor():
    
    # new document form
    form = DocumentForm()

    # display choices from list of editors
    form.editorchoice.query = User.query.filter(User.user_type == 'editor')

    if form.validate_on_submit():

        # Add New Document ------------
        # take new document
        # create new document
        newdocument = Document(
            document_name=form.document_name.data,
            document_body=form.document_body.data
            )

        # add and commit new document
        db.session.add(newdocument)
        db.session.commit()

        # after this document has just been added to the database, add retention
        # query all documents in order, put into a python object
        all_documents_ordered = Document.query.order_by(Document.id)
        # query count of all documents, subtract 1 because python index starts at 0
        document_index = Document.query.count() - 1
        # last document object is document index, or count-1
        last_document = all_documents_ordered[document_index]
        # new document id for retentions database is indexed last documentid integer
        newdocument_id = last_document.id


        # Add Sponsor Retention ------------
        # get the current userid
        user_id = current_user.id

        # extract the selected editor choice from the form
        selected_editor_id=int(form.editorchoice.data.id)

        # create a new retention entry
        newretention = Retention(
            sponsor_id=user_id,
            editor_id=selected_editor_id,
            document_id=newdocument_id
            )
        
        # add retention to session and commit to database
        db.session.add(newretention)
        db.session.commit()

         # message included in the route python function
        message = "New Document saved. Create another document if you would like."
        # if everything goes well, they will be redirected to documents list
        return redirect(url_for('sponsor_bp.documentlist_sponsor'))

    return render_template('newdocument_sponsor.jinja2',form=form)


@sponsor_bp.route('/sponsor/documents', methods=['GET','POST'])
@login_required
@sponsor_permission.require(http_exception=403)
def documentlist_sponsor():
    """Logged-in Sponsor List of Documents."""
    # get the current user id
    user_id = current_user.id
    
    # Document objects list which includes editors for all objects
    # this logic will only work if document_objects.count() = editor_objects.count()
    # get document objects filtered by the current user
    document_objects=db.session.query(Retention.sponsor_id,User.id,Retention.editor_id,Retention.document_id,User.name,Document.document_name,Document.document_body).\
    join(Retention, User.id==Retention.editor_id).\
    join(Document, Document.id==Retention.document_id).\
    order_by(Retention.sponsor_id).\
    filter(Retention.sponsor_id == user_id)

    # get a count of the document objects
    document_count = document_objects.count()
    
    # blank list to append to for documents and editors
    document_list=[]

    # loop through document objects
    for counter in range(0,document_count):
        document_list.append(document_objects[counter])

    # show list of document names
    documents = document_list

    return render_template(
        'documentlist_sponsor.jinja2',
        documents=documents,
    )


@sponsor_bp.route('/sponsor/documents/<document_id>', methods=['GET','POST'])
@login_required
@sponsor_permission.require(http_exception=403)
def documentedit_sponsor(document_id):

    # new document form
    form = DocumentForm()


    # Getting the Document Object
    # query for the document_id in question to get the object
    document = db.session.query(Document).filter_by(id = document_id)[0]

    # Getting the Retention Object to Filter  for Editor ID
    # join query to get and display current editor id via the retention object
    retention_object = db.session.query(Retention).join(User, User.id == Retention.editor_id).filter(Retention.document_id == document_id)[0]
    # get current editor_id from retention object
    current_editor_id = retention_object.editor_id
    
    # Getting the Editor Object
    # use this current editor object
    current_editor_object = db.session.query(User).filter(User.id == current_editor_id)[0]
    # simplify variable name to pass to view
    editor = current_editor_object

    # display choices from list of editors
    form.editorchoice.query = User.query.filter(User.user_type == 'editor')

    if form.validate_on_submit():
        # take new document
        # edit document parameters
        # index [0], which is the row in question for document name
        document.document_name = form.document_name.data
        document.document_body = form.document_body.data

        # grab the selected_editor_id from the form
        selected_editor_id=int(form.editorchoice.data.id)

        # add new retention
        retention_object.editor_id = selected_editor_id

        # commit changes
        db.session.commit()

        # redirect to document list after change
        return redirect(url_for('sponsor_bp.documentlist_sponsor'))


    return render_template(
        'documentedit_sponsor.jinja2',
        form=form,
        document=document,
        editor=editor
        )



# ---------- editor user routes ----------

@editor_bp.route("/editor/logout")
@login_required
@editor_permission.require(http_exception=403)
def logouteditor():
    """User log-out logic."""
    logout_user()
    # tell flask principal the user is annonymous
    identity_changed.send(current_app._get_current_object(),identity=AnonymousIdentity())
    # print annonymousidentity to console
    identity_object = AnonymousIdentity()
    # printing identity_object to console for verification
    print('Sent: ',identity_object,' ...to current_app', file=sys.stderr)
    return redirect(url_for('auth_bp.login'))

@editor_bp.route('/editor/dashboard', methods=['GET'])
@login_required
@editor_permission.require(http_exception=403)
def dashboard_editor():
    """Logged-in User Dashboard."""
    return render_template(
        'dashboard_editor.jinja2',
        title='Editor Dashboard',
        template='layout',
        body="Welcome to the Editor Dashboard."
    )

@editor_bp.route('/editor/documents', methods=['GET','POST'])
@login_required
@editor_permission.require(http_exception=403)
def documentlist_editor():
    """Logged-in Sponsor List of Documents."""
    # get the current user id
    user_id = current_user.id
    
    # Document objects and list, as well as Editor objects and list
    # this logic will only work if document_objects.count() = editor_objects.count()
    # get document objects filtered by the current user
    document_objects = db.session.query(Document).join(Retention, Retention.document_id == Document.id).filter(Retention.editor_id == user_id)

    # get a count of the document objects
    document_count = document_objects.count()
    
    # blank list to append to for documents and editors
    document_list=[]
    
    # loop through document objects
    for counter in range(0,document_count):
        document_list.append(document_objects[counter])
    
    # show list of document names
    documents = document_list

    
    return render_template(
        'documentlist_editor.jinja2',
        documents=documents,
    )


@editor_bp.route('/editor/documents/<document_id>', methods=['GET','POST'])
@login_required
@editor_permission.require(http_exception=403)
def documentedit_editor(document_id):

    # new document form
    form = DocumentForm()

    # Getting the Document Object
    # query for the document_id in question to get the object
    document = db.session.query(Document).filter_by(id = document_id)[0]
    
    if form.validate_on_submit():
        # take new document
        # edit document parameters
        # index [0], which is the row in question for document name
        document.document_name = form.document_name.data
        document.document_body = form.document_body.data

        # commit changes
        db.session.commit()

        # redirect to document list after change
        return redirect(url_for('editor_bp.documentlist_editor'))


    return render_template(
        'documentedit_editor.jinja2',
        form=form,
        document=document,
        )


# ---------- Page Access Restrictions ----------

# ---------- Error Handling ----------

# Send everything to the login page, don't worry about a message yet.

@sponsor_bp.errorhandler(403)
def sponsor_page_not_found(e):
    # note that we set the 404 status explicitly
    return redirect(url_for('auth_bp.login'))

@editor_bp.errorhandler(403)
def sponsor_page_not_found(e):
    # note that we set the 404 status explicitly
    return redirect(url_for('auth_bp.login'))