"""Routes for user authentication."""
from flask import Blueprint, redirect, render_template, flash, request, session, url_for
from flask_login import login_required, current_user, login_user
from .forms import LoginForm, SignupForm
from .models import db, User
from . import login_manager
from .routes import sponsor_bp, editor_bp

# Blueprint Configuration
auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log-in page for registered users.

    GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard.
    """
    # Bypass if user is logged in
    if current_user.is_authenticated:
        # get user number
        user_type = User.query(User.user_type)
        print(user_type)

        # based upon user type, route to location
        if user_type=='sponsor':
            return redirect(url_for('sponsor_bp.dashboard_sponsor'))
        elif user_type=='editor':
            return redirect(url_for('editor_bp.dashboard_editor'))

    form = LoginForm()
    # Validate login attempt
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if user.user_type=='sponsor':
                return redirect(url_for('sponsor_bp.dashboard_sponsor'))
            elif user.user_type=='editor':
                return redirect(url_for('editor_bp.dashboard_editor'))
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