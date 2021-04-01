"""Routes for user authentication."""
from flask import Blueprint, redirect, render_template, flash, request, session, url_for
from flask import g, current_app, abort, request
from flask_login import login_required, current_user, login_user
from .forms import LoginForm, SignupForm, AdminLoginForm
from .models import db, User
from . import login_manager
from .routes import sponsor_bp, editor_bp, admin_bp
# for identifitaction and permission management
from flask_principal import Identity, identity_changed
# for printing system messages
import sys
# for admin password
from .adminsettings import ADMIN_USERNAME, ADMIN_PASSWORD

# Blueprint Configuration
auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

# Blueprint Configuration
adminauth_bp = Blueprint(
    'adminauth_bp', __name__,
    template_folder='templates_admins',
    static_folder='static'
)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log-in page for registered users.

    GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard.
    """
    # Bypass if user is logged in already
    if current_user.is_authenticated:
        # if current user actually has id, which they all should
        if hasattr(current_user, 'id'):
            # get user id number
            user_id = current_user.id
            # filter for user to get user type as a string
            current_user_type = User.query.filter(User.id==current_user.id)[0].user_type
            # based upon user type, route to location
            if current_user_type=='sponsor':
                return redirect(url_for('sponsor_bp.dashboard_sponsor'))
            elif current_user_type=='editor':
                return redirect(url_for('editor_bp.dashboard_editor'))

    form = LoginForm()
    # Validate login attempt
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
             # send to next page
            next_page = request.args.get('next')

            # user should already have a type since they logged-in in the past
            # use identity_changed to send signal to flask_principal showing identity, user_type
            identity_changed.send(current_app._get_current_object(), identity=Identity(user.id,user.user_type))
            # placing identity_object into variable for print/display
            identity_object = Identity(user.id,user.user_type)
            # printing identity_object to console for verification
            print('Sent: ',identity_object,' ...to current_app', file=sys.stderr)

            # check user type, if sponsor go to sponsor dashboard

            if user.user_type=='sponsor':
                # redirect to sponsor dashboard
                return redirect(url_for('sponsor_bp.dashboard_sponsor'))
            # if user type is editor, send to editor dashboard
            elif user.user_type=='editor':
                # redirect to editor dashboard
                return redirect(url_for('editor_bp.dashboard_editor'))
        # otherwise flash invalid username/password combo
        flash('Invalid username/password combination')
        return redirect(url_for('auth_bp.login'))
    return render_template(
        'login.jinja2',
        form=form,
        title='Log in.',
        template='login-page',
        body="Log in with your User account."
    )

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login'))

# ---------- sponsor routes ----------

@sponsor_bp.route('/signupsponsor', methods=['GET', 'POST'])
def signupsponsor():
    """
    Sponsor sign-up page.

    GET requests serve sign-up page.
    POST requests validate form & user creation.
    """
    form = SignupForm()
    # validate if the user filled out the form correctly
    # validate_on_submit is a built-in method
    if form.validate_on_submit():
        # make sure it's not an existing user
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            # create a new user
            user = User(
                name=form.name.data,
                email=form.email.data,
                organization=form.organization.data,
                user_type='sponsor'
            )
            # use our set_password method
            user.set_password(form.password.data)
            # commit our new user record and log the user in
            db.session.add(user)
            db.session.commit()  # Create new user
            login_user(user, remember=False, duration=None, force=False, fresh=True)
            # if everything goes well, they will be redirected to the main application

            # new user now has a type, extract and send to permissions signal
            # use identity_changed to send signal to flask_principal showing identity, user_type
            identity_changed.send(current_app._get_current_object(), identity=Identity(user.id,user.user_type))
            # placing identity_object into variable for print/display
            identity_object = Identity(user.id,user.user_type)
            # printing identity_object to console for verification
            print('Sent: ',identity_object,' ...to current_app', file=sys.stderr)


            return redirect(url_for('sponsor_bp.dashboard_sponsor'))
        flash('A user already exists with that email address.')
    return render_template(
        'signup_sponsor.jinja2',
        title='Create a Sponsor Account.',
        form=form,
        template='signup-page',
        body="Sign up for a Sponsor account."
    )

# ---------- editor routes ----------

@editor_bp.route('/signupeditor', methods=['GET', 'POST'])
def signupeditor():
    """
    Editor sign-up page.

    GET requests serve sign-up page.
    POST requests validate form & user creation.
    """
    form = SignupForm()
    # validate if the user filled out the form correctly
    # validate_on_submit is a built-in method
    if form.validate_on_submit():
        # make sure it's not an existing user
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            # create a new user
            user = User(
                name=form.name.data,
                email=form.email.data,
                organization=form.organization.data,
                user_type='editor'
            )
            # use our set_password method
            user.set_password(form.password.data)
            # commit our new user record and log the user in
            db.session.add(user)
            db.session.commit()  # Create new user

            # new user now has a type, extract and send to permissions signal
            # use identity_changed to send signal to flask_principal showing identity, user_type
            identity_changed.send(current_app._get_current_object(), identity=Identity(user.id,user.user_type))
            # placing identity_object into variable for print/display
            identity_object = Identity(user.id,user.user_type)
            # printing identity_object to console for verification
            print('Sent: ',identity_object,' ...to current_app', file=sys.stderr)

            login_user(user, remember=False, duration=None, force=False, fresh=True)
            # if everything goes well, they will be redirected to the main application
            return redirect(url_for('editor_bp.dashboard_editor'))
        flash('A user already exists with that email address.')
    return render_template(
        'signup_editor.jinja2',
        title='Create an Editor Account.',
        form=form,
        template='signup-page',
        body="Sign up for a Sponsor account."
    )

# ---------- admin routes ----------

@adminauth_bp .route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():

    # login form
    form = AdminLoginForm()

    # Validate login attempt
    if form.validate_on_submit():
        user=1
        # we don't need a userid, there is only one user.
        # check password against our environmental variable
        if ADMIN_PASSWORD==form.password.data:
            login_user(user)
            # send to next page
            next_page = request.args.get('next')
            return redirect(url_for('admin_bp.dashboard_admin'))

        # otherwise flash invalid username/password combo
        flash('Invalid username/password combination')
        return redirect(url_for('adminauth_bp.adminlogin'))
    
    return render_template(
        'login_admin.jinja2',
        form=form,
        title='Log in.',
        template='login-page',
        body="Log in with administration credentials."
    )