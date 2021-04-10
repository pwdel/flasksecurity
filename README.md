# Flask Security

## About

Playing around with logins, best practices for security, etc.

## Objective

After having completed the [User Level Models Flask](https://github.com/pwdel/userlevelmodelsflask) project, the next steps are to:

* Improve security
* Add an administrative user
* Give the administrative user the capability to approve, disapprove, suspend users
* Create user view for if account is suspended
* Different login functionality that works for different parts and pages of the site
* Basically overall guard expensive server resources while still allowing access to the platform

## Note on Previous Work

When referring to, "past projects" or "previous work" on this document, I am likely referring to these projects:

* [Usermodels Flask](https://github.com/pwdel/userlevelmodelsflask)
* [Postgres Login API with Heroku/Docker/Flask](https://github.com/pwdel/postgresloginapiherokudockerflask)
* [Heroku/Docker/Flask](https://github.com/pwdel/herokudockerflask)

## Plan of Attack

0. Review Flask overall architecture (written above, in the comparison of Django vs. Flask).
1. Review more articles about securing flask applications in general, flask security considerations.
2. Activate and try out Flask-Principal with previous application to see if I can get user permissions working.
3. Attempt to build admin panel with the capability to set and approve user permissions using [Flask-Admin](https://flask-admin.readthedocs.io/en/latest/) rather than Flask-Unchained as a whole. This is an attempt to minimize the number of third party modules being used in the platform.
4. Any other security cleanup tasks, or a to-do list for security tasks.

## Evaluating Options

| Name               | Link                                         | Last Updated |
|--------------------|----------------------------------------------|--------------|
| Flask-Security     | https://pypi.org/project/Flask-Security/     | July 2017    |
| Flask-Security-Too | https://pypi.org/project/Flask-Security-Too/ | Jan 2021     |
| Flask-Principal    | https://pypi.org/project/Flask-Principal/    | July  2013   |
| Flask-Unchained    | https://pypi.org/project/Flask-Unchained/    | Jan 2021     |

## Reading Through Tutorials

Through the process of reading through various tutorials on modules, it became clear that what I'm doing is really working with an expanded architecture of the platform, rather than just, "adding on security."  A helpful read in understanding Flask's archetecture and how it's built is [this article from Testdriven.io](https://testdriven.io/blog/django-vs-flask/).

### Django vs. Flask Summarized

This article goes through and compares Django, a more out-of-the-box web application platform, to Flask.  Briefly summarized:

* Philosophy - Django is more stable and, "batteries included."  The release cycles are longer and more rigid, which means there are fewer, shiny new features but there is stronger backwards compatibility.  Flask is based on Werkzeuk, and handles the core scaffolding, but not a lot of features. You get URL routing, error handling, templating, cookies, support for unit testing, but other than that it's completely customizeable. There's less code to review if you crack open the hood.
* Database - Django has its own ORM that supports a number of existing relational databases.  Flask has many different modules it can work with, uses SQLAlchemy, as I have seen with previous projects. Flask allows for non-relational database options.
* Authentication - Django provides this functionality out of the box.  Flask-Login is used for account management and authentication, it is a module/add-on.
* Authorization - Flask-Principal is cited as being used for user level management, as is Flask-Security (which has been updated with Flask-Security-Too).
* Admin - Flask-Admin helps create an admin panel, while Django has its own admin panel.
* Routing and Views - Django has a couple of files, urls.py and views.py which architecture this out and processes requests, while Flask uses Werkzeug.
* Forms come packaged with Django, whereas flask uses Flask-WTF or other modules.
* Re-usable components - Django uses the concept of, "app" while flask has, "blueprints" embedded within it.
* Static files and templates in Django are done with its own templating engine, while Flask uses Jinja2, which Django can also use.
* [Asynchronous views](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous/Concepts) is supported within Django via async. The article doesn't mention it, but there is a flask plugin called, [aiohttp](https://flask-aiohttp.readthedocs.io/en/latest/) which can help make this happen.
* Testing on both platforms is done on Python's unittest framework.
* Django has other various features which can be mimiced in Flask, which include Atom and RSS, Caching, Bootstrapping/CLI, and sitemaps.
* Security in Django has a lot of built-ins, whereas Flask is more reliant on third party extensions. However Flask has a smaller attack surface area because it has less code.  Keeping flask up to date with the latest extensions is the most challenging, since each extension has its own development team. Keeping extensions and modules to a minimum is important, as they all have their own release cycles.

Ultimately though, since Flask allows any module to be used, it is the only web framework that can be utilized in larger machine learning projects.  Django would prevent certain modules from being used.

### Quick Side Note on Python Package Evaluation

[This article](https://packaging.python.org/guides/analyzing-pypi-package-downloads/) goes through how to analyze the quantity of Python package downloads with BigQuery.

### Flask-Security

Flask-Security seems to be somewhat deprecated.  It appears to still be in use, but is not as frequently updated.  The main criteria for modules is whether it fits into your specific project, which means taking stock of what parameters you are looking for and why, as well as evaluating each module on its merits.

This project is being built by one person for the time being, so customization of code is a problem.  Basically even if Flask-Security with customizations would provide better security, that would be not as desirable as something that is more plug and play.  What I'm trying to secure just isn't that valuable yet.

An alternative to Flask-Security is [Flask Praetorian](https://flask-praetorian.readthedocs.io/en/latest/), as well as Flask-Security-Too below.

### Flask-Principal

Flask Principal is for user authorization.  This appears to be a very old extension.  There appear to be a problem [at least one person has had with this extension](https://www.reddit.com/r/learnpython/comments/8pk6ao/what_are_good_alternatives_to_the_flaskextensions/), with the [lead maintainer not being active for a long time](https://github.com/mattupstate).

[Flask-Allows](https://github.com/justanr/flask-allows) appears to be more maintained, however at the time of writing the build was failing.

That being said, the code which makes up [Flask-Principal](https://github.com/mattupstate/flask-principal/blob/master/flask_principal.py) is fairly simple, so at the very least it may be something to try out or at least replicate.

### Flask-Security-Too

[Flask Security Too docs](https://flask-security-too.readthedocs.io/en/stable/) show that Flask-Security Too is an attempt to keep the flask-Security projet going.

Features within Flask-Security-Too include:

Features I Already Use:

* Flask-Login
* Flask-WTF

New Features:

* Flask-Mail
* Flask-Principal
* itsdangerous - allows, "signed" data
* passlib - password hashing
* PyQRCode - QR Code generator

Since Flask-Security-Too uses Flask-Principal, and without knowing whether Flask-Principal works well, it's unknown how well the package aas a whole would work. Since one of the main feature's I'm looking for is user permissions, it may make the most sense just to use Flask-Principal.

While Flask-Security-Too seems to provide "auth," authentication and authorization, it does not actually seem to cover a lot of the security loopholes inherent in Flask, which seem to need to be coded into the application itself.

### Flask-Unchained

[Flask-Unchained Docs](https://flask-unchained.readthedocs.io/en/latest/index.html) show that Unchained is basically a very light version of Django but in Flask form, hence the name, "Unchained."  However, Django includes all different sorts of bundles, while the bundles which are included in Unchained appear to be:

Modules we have:

* Integration with SQLAlchemy and Flask-Migrate
* Integratin with Flask-Login
* Integration with Flask-WTF

New modules:

* [Flask-Session](https://flask-session.readthedocs.io/en/latest/) stores user information on the server, rather than merely with cookies.
* Flask-Mail allows email support.
* [Flask-Admin](https://flask-admin.readthedocs.io/en/latest/) - seems active, last release October 2020.
* Flask-Marshmellow (SQLAlchemy model serialization)
* pytest and factory_boy

Basically, all of the normal things you would look for in an out-of-the-box webapp.

There is an [Unchained tutorial](https://flask-unchained.readthedocs.io/en/latest/index.html).

## Flask Principal

* [Flask Principal Documentation](https://pythonhosted.org/Flask-Principal/)
* [Flask Principal Implementation Blog](https://terse-words.blogspot.com/2011/06/flask-extensions-for-authorization-with.html)

### Breaking Down Flask Principal

* Identity, Needs, Permission and Identity Context

> The Identity represents the user, and is stored/loaded from various locations (eg session) for each request. The Identity is the user’s avatar to the system. It contains the access rights that the user has.

> A Need is the smallest grain of access control, and represents a specific parameter for the situation. For example “has the admin role”, “can edit blog posts”.  Needs are generally tuples.

> A Permission is a set of requirements, any of which should be present for access to a resource.

> An IdentityContext is the context of a certain identity against a certain Permission. It can be used as a context manager, or a decorator.

### Breaking Down Important Components

* [Python Decorators](https://realpython.com/primer-on-python-decorators/).

Basically, decorators can envelope or call a function, they have a special way of being called, and can perform actions previous to and after a function in sequence.  They are designed to be easily reused.  This article goes into all sorts of common examples of how functions are used and how to use decorators with them. For example, how to use a decorator which performs a function twice, when only one argument is passed into a function.  There are all sorts of applications for decorators, including timing functions, debugging code, slowing down code, registering plugins, changing function behavior, checking for logins, etc.

* [Python Context Managers](https://docs.python.org/3/library/stdtypes.html#context-manager-types)

* [Signal Set Handlers for Asynchronous Events](https://docs.python.org/3/library/signal.html)

### How to Implement Flask Principal

Set up permissions within the app context as shown:

```
from flask.ext.principal import Principal, Permission, RoleNeed

# calling Flask Principal
principals = Principal(app)

# setting up a sponsor role
sponsor_role = RoleNeed('sponsor')

# setting up a sponsor permission
sponsor_permission = Permission(sponsor_role)

whatever._init_app(app)

```
After this you can use a decorator to protect a route, such as "/" with a decorator:

```
# perform decorator action, give Forbidden response if not passed
@sponsor_permission.require(http_exception=403)
```

For example:

```
@app.route('/sponsor/dashboard/')
@sponsor_permission.require(http_exception=403)

```

Alternatively:

```
@app.route('/sponsor/dashboard/')
def dashboard():
    with sponsor_permission.require(http_exception=403)

```

If we don't have a 403 error handler, you can create it with:

```
@app.errorhandler(403)
def page_not_found(e):
    session['redirected_from'] = request.url
    return redirect(url_for('login'))
```

### Migrating the Project

* Started out by copying the entire project structure from [here](https://github.com/pwdel/userlevelmodelsflask)
* For development purposes, changed the name of the config variable, "DATABASE_URL_PROD" to "DATABASE_URL"

### Where to Put Flask Principal

To start off with, we can put the main function definition within __init__.py.

Dependencies must be added to requirements.txt.  The dependency file for [Flask-Principal](https://pypi.org/project/Flask-Principal/) can be found there at version 0.4.0

Adding Flask-Principal to requirements.txt resulted in no errors.

However, from the import, right away we get the error:

```
flask  |     from flask.ext.principal import Principal, Permission, RoleNeed
flask  | ModuleNotFoundError: No module named 'flask.ext'

```

I was able to get it working by replacing "ext" with underscore, [per this code repo](https://isgb.otago.ac.nz/infosci/nigel.stanger/INFORMS2/commit/9628eebb91ec2dca8f507e092d7e6722cb1c7b25):

```
from flask_principal import Principal, Permission, RoleNeed
```

ext must be a legacy method of calling out modules.

Within __init__.py we added the following, without issue:

```
# Activating Flask Principal
# calling Flask Principal
principals = Principal(app)

# setting up a sponsor role
sponsor_role = RoleNeed('sponsor')

# setting up a sponsor permission
sponsor_permission = Permission(sponsor_role)
```
### Setting Up within Route

```
@sponsor_bp.route('/sponsor/dashboard', methods=['GET','POST'])
@login_required
@sponsor_permission.require(http_exception=403)
def dashboard_sponsor():
```
By just decorating the above function without having imported we get an error. Within routes.py, the import from the init file happens with:

```
from . import sponsor_permission
```
However then we get:

```
flask  | ImportError: cannot import name 'sponsor_permission' from partially initialized module 'project' (most likely due to a circular import) (/usr/src/theapp/project/__init__.py)

```

To avoid the circular import, we put the following above the create_app() function within __init__.py

```
from flask_principal import Principal, Permission, RoleNeed

...

# Flask Principal
principals = Principal()
# setting up a sponsor role from Flask Principal
sponsor_role = RoleNeed('sponsor')
# setting up a sponsor permission
sponsor_permission = Permission(sponsor_role)

```
Note that we are using Principal() instead of Principal(app). It is not clear why Principal(app) would be needed as it's not envoked anywhere in our code yet.

Then within routes.py, we make sure the following is added:

```
@sponsor_bp.route('/sponsor/dashboard', methods=['GET','POST'])
@login_required
@sponsor_permission.require(http_exception=403)
def dashboard_sponsor():

```
The next step is to test this by attempting to log in as an editor, and then see if we can visit the /sponsor/dashboard...which indeed it does, however there is an attribute error, which suggests that it possibly doesn't even work for a sponsor - which after checking, we see we get the same error:

```

    File "/usr/local/lib/python3.9/site-packages/flask_principal.py", line 198, in _decorated

    with self:

    File "/usr/local/lib/python3.9/site-packages/flask_principal.py", line 205, in __enter__

    if not self.can():

    File "/usr/local/lib/python3.9/site-packages/flask_principal.py", line 193, in can

    return self.identity.can(self.permission)

    File "/usr/local/lib/python3.9/site-packages/flask_principal.py", line 188, in identity

    return g.identity

    File "/usr/local/lib/python3.9/site-packages/werkzeug/local.py", line 347, in __getattr__

    return getattr(self._get_current_object(), name)

    AttributeError: '_AppCtxGlobals' object has no attribute 'identity'


```
It was never clear how Flask-Principal was pulling these identities out of nowhere to decide how to take action.  First possibility, which doesn't really clear up the problem, but appears to perhaps make up for using Principal() rather than Principal(app) upon initializatin, is to add the following within our create_app() - which we had found [here at this code](https://isgb.otago.ac.nz/infosci/nigel.stanger/INFORMS2/commit/9628eebb91ec2dca8f507e092d7e6722cb1c7b25).

```
...

principals.init_app(app)
```
After doing this, we now get a better error, a 403 error, like we are expecting, printed out nicely on the browser:

```
Forbidden

<Permission needs={Need(method='role', value='sponsor')} excludes=set()>
```
We can come back and clean this up with a 403 handler in the future.  However for now, the problem is that somehow this function is looking for a value='sponsor', via method='role' but it's not clear where that is coming from and what that means, and how these attributes get assigned to our user type.

#### Using a Blog Tutorial on Demystifying Flask-Principal

Reading through [this tutorial on demystifying Flask-Principal](https://jupyterdata.medium.com/a-shot-at-demystifying-flask-principal-dda5aaeb6bc6), I observe the following code:

```
     def __init__(self, id):
         if not id in self.USERS:
             raise UserNotFoundError()
         self.id = id
         self.password = self.USERS[id]
         self.roles=self.ROLES[id]
```
Basically, within the __init__ function, you have self.roles created within the User class.

```
self.roles=self.ROLES[id]
```

Bear in mind, this is a class where in the UserMixin standard structure is an input, which constrasts to our db.Model input.

```
class User(UserMixin):
    '''Simple User class'''
```

There is significant documentation within the [Flask Principal Github](https://github.com/mattupstate/flask-principal/blob/master/flask_principal.py), within the flask_principal.py file, in the form of comments.  It may be even easier to look at this documentation and read through it rather than a tutorial.

Blinker was inspired by the Django signal API.

* [connect_via](https://github.com/jek/blinker/blob/b5e9f0629200d2b2f62e13e595b802948bb4fefb/blinker/base.py#L160) is a part of blinker which connects the decorated function as a receiver for *sender*.

Within blinker you can, among objects:

* Subscribe to signals
* Emit signals, send()
* Subscribe to specific senders
* Send and recieve data through signals
* Use annonymous signals
* Connect as a decorator
* Optimize Signals
* Use an API



#### Review of Blinker

[Blinker](https://pythonhosted.org/blinker/) is a python module which provides fast & simple object-to-object and broadcast signaling for Python objects.  Blinker is used to build flask_principal.

The source code for [Blinker can be found here](https://github.com/jek/blinker).

#### Flask-Principal Documentation - Identity - What is "Identity"?

class Identity(object):

>    The identity is used to represent the user's identity in the system. This object is created on login, or on the start of the request as loaded from the user's session. Once loaded it is sent using the `identity-loaded` signal, and should be populated with additional required information. Needs that are provided by this identity should be added to the `provides` set after loading.


#### Flask-Principal Documentation - identity_changed on Login for Sponsor

Signal sent when the identify for a request has been changed.

This signal, "identity-changed" should be sent when authentication has been performed.  Flask-Principal connects to this signal and cuases the identity to be saved in the session.

Example:

```
    from flaskext.principal import Identity, identity_changed

    def login_view(req):
        username = req.form.get('username')
        # check the credentials
        identity_changed.send(app, identity=Identity(username))
```

So basically, this should happen during authentication.

Another example is the function, "login_check()"

```
def login_check():
    # validate username and password
    user = User.get(request.form['username'])
    if (user and user.password == request.form['password']):
        login_user(user)
     identity_changed.send(current_app._get_current_object(), identity=Identity(user.roles))
    else:
        flash('Username or password incorrect')    return render_template('auth/index.html')
```
The above is just example code showing one example of a user login. Our application actually uses user.id to authenticate, rather than username.  This, "identity changed" signal doesn't really mean an identity was changed in the database, it just means a signal was sent to flask_principal, containing the Identity object.

```
identity_changed.send(current_app._get_current_object(), identity=Identity(user.roles))
```
The above should probably be changed to align with our platform, such that User.user_type is the role, on Login:

```
from flask import g, session, current_app, abort, request
from flask_principal import Identity, identity_changed
...

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

...

        if user and user.check_password(password=form.password.data):
            login_user(user)
            
            # user should already have a type since they logged-in in the past
            # use identity_changed to send signal to flask_principal showing identity, user_type
            identity_changed.send(current_app._get_current_object(), identity=Identity(user.user_type))

            next_page = request.args.get('next')
            if user.user_type=='sponsor':
                return redirect(url_for('sponsor_bp.dashboard_sponsor'))
            elif user.user_type=='editor':
                return redirect(url_for('editor_bp.dashboard_editor'))

...


```
* [current_app is a part of flask](https://flask.palletsprojects.com/en/1.1.x/api/#flask.current_app)
* [_get_current_object_() is a part of Flask](https://werkzeug.palletsprojects.com/en/1.0.x/local/#werkzeug.local.LocalProxy._get_current_object)

Once the above is implemented properly, there is no error or protest from the application, but there is no clear indication that it's working either. Logging into the flask shell won't really help because that user isn't an actual sponsor user so much as the server-user observing the flask application.

We can see if something happened successfully within flask by printing to console with app.logger.X() :

```
import sys

...

            # user should already have a type since they logged-in in the past
            # use identity_changed to send signal to flask_principal showing identity, user_type
            identity_changed.send(current_app._get_current_object(), identity=Identity(user.user_type))
            # placing identity_object into variable for print/display
            identity_object = Identity(user.user_type)
            # printing identity_object to console for verification
            print('Sent: ',identity_object,' ...to current_app', file=sys.stderr)

```
When we did this, we get the message that the following object was sent to current_app:

```
<Identity id="sponsor" auth_type="None" provides=set()>
```
So the identity really should be the user.id, the number, rather than the type.  The auth_type should be 'sponsor'.

From the [Flask-Principal documentation](https://pythonhosted.org/Flask-Principal/), we see it defines the following class:

```
 class flask_principal.Identity(id, auth_type=None)

    Represent the user’s identity.
    Parameters: 

        id – The user id
        auth_type – The authentication type used to confirm the user’s identity.

```
Putthing this within the proper place in the logic, we should get the user type, "sponsor" sent if the user is indeed a sponsor.

```
flask  | Sent:  <Identity id="1" auth_type="sponsor" provides=set()>  ...to current_app
```
So within the location in the logic that we're looking for, under sponsor, we place:

```
if user.user_type=='sponsor':
               # user should already have a type since they logged-in in the past
               # use identity_changed to send signal to flask_principal showing identity, user_type
               identity_changed.send(current_app._get_current_object(), identity=Identity(user.id,user.user_type))
               # placing identity_object into variable for print/display
               identity_object = Identity(user.id,user.user_type)
               # printing identity_object to console for verification
               print('Sent: ',identity_object,' ...to current_app', file=sys.stderr)
               # redirect to sponsor dashboard
               return redirect(url_for('sponsor_bp.dashboard_sponsor'))
```
Which should activate if the user.user_type is indeed sponsor.


##### provides=set()

What does provides=set() mean?

Within the [flask-principal github source code](https://github.com/mattupstate/flask-principal/blob/0b5cd06b464ae8b60939857784bda86c03dda1eb/flask_principal.py#L142), we see the lines of code:

```
    def __init__(self, id, auth_type=None):
        self.id = id
        self.auth_type = auth_type
        self.provides = set()
```

And within the commentary, it says:

>     Needs that are provided by this identity should be added to the `provides` set after loading.

Basically, self.provides is set as being equal to set(), which is a set object, an unordered list of items. What's in that set? It appears to be the tuple including, "id" and "auth."


#### Flask-Principal Documentation - identity_changed on Login for Editor

Basically, we can provide the above logic above the editor/sponsor conditional login, because it applies to either user type.

Once we do this and test by logging in as an editor, we get:

```
flask  | Sent:  <Identity id="2" auth_type="editor" provides=set()>  ...to current_app
```

#### Flask-Principal Documentation - identity_changed on Signup

Now that identity_changed has been successfully implemented within the login, it needs to also be implemented on signup.

We have two places for this:

@sponsor_bp.route('/signupsponsor', methods=['GET', 'POST'])

and

@editor_bp.route('/signupeditor', methods=['GET', 'POST'])

The same code used for /signin can be used for /signup, it goes after the, "login_user" function.

#### Flask-Principal Documentation - identity_changed  to AnnonymousIdentity on Logout

In our application, logouts for each user type exist within the routes.py individual user types.  For example:

```
from flask import g, current_app, abort, request
# for identifitaction and permission management
from flask_principal import Identity, identity_changed
# for printing system messages
import sys

...

@sponsor_bp.route("/sponsor/logout")
@login_required
def logoutsponsor():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))
```
For taking away the identity policy, we just have to put the following logic right before, "logout_user()" - this is because there has to be an existing user in order to take a policy away from it.

```
    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())
```

Once we do this and print to the console, we get:

```
flask  | Sent:  <AnonymousIdentity id="None" auth_type="None" provides=set()>  ...to current_app
```

#### Flask-Principal Documentation - identity_loaded

> User information providers should connect to the identity-loaded signal to add any additional information to the Identity instance such as roles. 

Basically, this is required for more grandular resource protection, for example - allowing a user to only edit and view their own document or article, rather than any document or article across the entire system.

We have to 1. Populate the identity object with the necessary authorization provisions. 2. Load any additional information.

After the identiy is loaded, flask_principal can use IdentityContext to compare the Identity to the Permission, which holds a set of Needs, and grant access if the Identity's attributes pass the logic of Permission according to what is stored in Needs.

The following would go in our __init__.py file, to define our, "on_identity_loaded() function:

```
# Identity Loading Function from flask_principal
# identity_loaded adds any additional information to the Identity instance such as roles.
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
        # print userid to console
        print('Providing ID: ',current_user.id,' ...to Identity', file=sys.stderr)
        # provide userid to identity
        identity.provides.add(UserNeed(current_user.id))
        # Query user type given user.id
        current_user_type = User.query.filter(User.id==current_user.id)[0].user_type
        # print user_type to console
        print('Providing Role: ',current_user_type,' ...to Identity', file=sys.stderr)
        # provide user_type to identity
        identity.provides.add(RoleNeed(current_user_type))

```

* "hasattr" is a python function that looks at a class, for its attributes and returns true/false based upon whether that class has the attribute.
* connect_via() is from the "blinker" dependency

With some previous code which had attempted to index the current_user for role, we get the error:

```
flask  |     for role in current_user.user_type
```
Basically, you can't query the current_user for a role or user_type.  The only [attributes that the user class for current_user](https://flask-login.readthedocs.io/en/latest/#your-user-class) has is the following:

* is_authenticated
* is_active
* is_annonymous
* get_id()

To get the role, we need to query the database for the user itself.  This query could basically filter for the user.id and pull the user_type.  The flask terminal can be useful in building this query.

Once we properly modify the code to align with above, we get the following printed out for the user every time they change pages:

```
flask  | Providing ID:  2  ...to Identity
flask  | Providing Role:  sponsor  ...to Identity
```

So basically the ID and the role is following them around, like an identification badge.


#### Flask-Principal Documentation - Need - What is a Need?

Needs and Permissions have to be loaded up based upon user role.

[From the source code](https://github.com/mattupstate/flask-principal/blob/0b5cd06b464ae8b60939857784bda86c03dda1eb/flask_principal.py#L79) -

```
Need = namedtuple('Need', ['method', 'value'])
```

> This is just a named tuple, and practically any tuple will do. The ``method`` attribute can be used to look up element 0, and the ``value`` attribute can be used to look up element 1.

So basically, it's a tuple that is labeled, "Need" with a "method" and a "value."  The method could be id, role or perhaps something else - role, type, or action. The value could be the id's value, or the actual role value, action, type, item etc.  It's basically a flexible way of holding values for roles, id's and other important attributes...it's a way of recording the "needs."


##### UserNeed

> A need with the method preset to `"id"`.

```
UserNeed = partial(Need, 'id')
UserNeed.__doc__ = 
```

##### RoleNeed

> A need with the method preset to "role"

##### TypeNeed

> A need with the method preset to "type"

##### ActionNeed

> A need with the method preset to "action"

#### Flask-Principal Documentation - ItemNeed

> An item need is just a named tuple, and practically any tuple will do. In addition to other Needs, there is a type, for example this could be specified as:

>    ItemNeed('update', 27, 'posts')
>    ('update', 27, 'posts') # or like this

> And that might describe the permission to update a particular blog post. In reality, the developer is free to choose whatever convention the permissions are.

#### Flask-Principal Documentation - Permission

Permission(object)

> Represents needs, any of which must be present to access a resource ... :param needs: The needs for this permission. 

Has several functions within the Permission class that allows processing of the object.  This is basically the, "logic function" of flask_principal.

* __init__(self,* needs) - a set of needs which must be present. Recall that needs are simply tuples which contain id, role, type or action and the value associated.
* _bool_(self) - just a boolean true/false, settable
* __nonzero__(self) - 
* __and__(self,other) - allows a union of itself and other
* __or__(self,other) - allows difference of itself and other
* __contains__(self, other) - allows checking if something is a subset of another
* __repr__(self) - performs the action specified by the above
* require(self,http_exception) - allows usage as a context manager or a decorator.  Raises permission denied if permission not present.
* test(self,http_exception) - does the same as require but just puts up a flag rather than running permission denied. Is useful for checking rather than performing.
* reverse(self) - returns the reverse of the current state.
* Also includes - union, difference, subset, allows.

#### Setting Up Needs & Permissions Functions

Next to be able to make use of this virtual ID card we have given each user, we have to be able to set up a permission, and then use that permission as a barrier to entry over a resource.

I will also need to add more logic into the identity_loaded signal handler.

The following Permissions and Needs should be added to our __init__.py prior to app registration:

```
from flask_principal import identity_loaded, Principal, Permission, UserNeed, RoleNeed

# Permissions and Needs
# setting up a sponsor role from Flask Principal
sponsor_role = RoleNeed('sponsor')
# setting up a sponsor permission
sponsor_permission = Permission(sponsor_role)

# setting up an editor role from Flask Principal
editor_role = RoleNeed('editor')
# setting up an editor permission
sponsor_permission = Permission(editor_role)
```
Then within the identity_loaded function covered in the last section, 

```
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
...

    # Add the UserNeed to the identity

    ...

    # For a given user type...
    # Add the needs to the identity based upon our logic
        # some kind of logic setting up needs with each user

```
We have to add some kind of logic below which attaches the needs to the 

```
    # this is set up in such a way that multiple needs can be added to the same user
    needs = []
    # append sponsor and editor roles depending upon user
    # if current_user_type is sponsor
    if current_user_type == 'sponsor':
        # add sponsor_role, RoleNeed to needs
        needs.append(sponsor_role)
    # if current_user_type is editor
    elif current_user_type == 'editor':
        # add editor_role, RoleNeed to needs
        needs.append(editor_role)
        
    print('appended to needs : ',needs, file=sys.stderr)
    # add all of the listed needs to current_user
    for n in needs:
        g.identity.provides.add(n)

```
Once those needs are added, decorations can be added to function to approve or deny access.

Which appears to be approximately what we are looking for - however we have an error that, "g" is not defined.  What is "g" and what was it supposed to be?  It appears to be from the [flask-principal source code](https://github.com/mattupstate/flask-principal/blob/0b5cd06b464ae8b60939857784bda86c03dda1eb/flask_principal.py#L373), and it's not clear why it was being used in a tutorial, but if we eliminate "g" we get an expected output:

```
flask  | appended to needs :  [Need(method='role', value='sponsor')]
```
Our overall finalized, "Identity and Needs Loader Factory" looks like the following:

```
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
        # print userid to console
        print('Providing ID: ',current_user.id,' ...to Identity', file=sys.stderr)
        # provide userid to identity
        identity.provides.add(UserNeed(current_user.id))
        # Query user type given user.id
        current_user_type = User.query.filter(User.id==current_user.id)[0].user_type
        # print user_type to console
        print('Providing Role: ',current_user_type,' ...to Identity', file=sys.stderr)
        # provide user_type to identity
        identity.provides.add(RoleNeed(current_user_type))

    # this is set up in such a way that multiple needs can be added to the same user
    needs = []
    # append sponsor and editor roles depending upon user
    # if current_user_type is sponsor
    if current_user_type == 'sponsor':
        # add sponsor_role, RoleNeed to needs
        needs.append(sponsor_role)
    # if current_user_type is editor
    elif current_user_type == 'editor':
        # add editor_role, RoleNeed to needs
        needs.append(editor_role)      
    print('appended to needs : ',needs, file=sys.stderr)
    # add all of the listed needs to current_user
    for n in needs:
        identity.provides.add(n)
```

And the output looks like:

```
flask  | Providing ID:  1  ...to Identity
flask  | Providing Role:  sponsor  ...to Identity
flask  | appended to needs :  [Need(method='role', value='sponsor')]

```

##### Logout Error - UnboundLocalError

```
UnboundLocalError

UnboundLocalError: local variable 'current_user_type' referenced before assignment


File "/usr/src/theapp/project/__init__.py", line 118, in on_identity_loaded

if current_user_type == 'sponsor':


```

What is an UnboundLocalError?  Here's an example.

```
>>> y=10
>>> def foo():
...     print(y)                                                                            
...     y += 1

>>> bar()
UnboundLocalError: local variable 'y' referenced before assignment

```
This is because when you make an assignment to a variable in a scope, that variable becomes local to that scope and shadows any similarly named variable in the outer scope.

Basically, we need to re-write our  on_identity_loaded() function to ensure that current_user_type is available to all if statements within the entire function.

```
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    # basically pass current_user object to identity.user
    identity.user = current_user
    # Query user type given user.id

    current_user_type = User.query.filter(User.id==current_user.id)[0].user_type

...

```

##### 'AnonymousUserMixin' object has no attribute 'id'

Basically, if we hit any condition where the user is annonymous, such as hitting the front page for the first time, without having created a user in the database, we're going to lack any user attributes.

So basically, prior to authentication, we need some kind of conditional which prevents a database query from even occuring, because it's always going to come up with a blank ID for current_user.id.

```
File "/usr/src/theapp/project/__init__.py", line 99, in on_identity_loaded

current_user_type = User.query.filter(User.id==current_user.id)[0].user_type
```

We could build a conditional.  What kind of conditional do we want?

* try/except/final - would be if we want to check for an error, after checking for an attribute. This might be too overly broad, because it might catch any error at all, rather than precisely checking whether the id exists.
* hassattr() checks for whether a class has an attribute.  This is more precise because we are asking exactly whether this class has this specified attribute.

hasattr() works as follows:

```
>>> class Big(object):                                                             
...     def __init__(self,x,y):                                                         
...             self.x=x                                                                    
...             self.y=y   

>>> f=Big(100,"hi") 

>>> hasattr(f,'x')                                                                          
True

```
Note that the attribute input must be a string. So we can build a conditional statement for current_user:

```
if hassattr(current_user,'id'):
    # do the database lookup and user 

```
So our final logic looks like the following:

```
def on_identity_loaded(sender, identity):
    # Set the identity user object
    # basically pass current_user object to identity.user
    identity.user = current_user
    # Add the UserNeed to the identity
    # ensure current_user has attribute identity "id"
    if hasattr(current_user, 'id'):
        # specifically, need to have current_user.id
            # Query user type given user.id
        current_user_type = User.query.filter(User.id==current_user.id)[0].user_type
        # print userid to console
        print('Providing ID: ',current_user.id,' ...to Identity', file=sys.stderr)
        # provide userid to identity
        identity.provides.add(UserNeed(current_user.id))
        # print user_type to console
        print('Providing Role: ',current_user_type,' ...to Identity', file=sys.stderr)
        # provide user_type to identity
        identity.provides.add(RoleNeed(current_user_type))

        # this is set up in such a way that multiple needs can be added to the same user
        needs = []
        # append sponsor and editor roles depending upon user
        # if current_user_type is sponsor
        if current_user_type == 'sponsor':
            # add sponsor_role, RoleNeed to needs
            needs.append(sponsor_role)
        # if current_user_type is editor
        elif current_user_type == 'editor':
            # add editor_role, RoleNeed to needs
            needs.append(editor_role)      
        print('appended to needs : ',needs, file=sys.stderr)
        # add all of the listed needs to current_user
        for n in needs:
            identity.provides.add(n)
```


#### Flask-Principal Documentation - Principal

##### set_identity(self, identity):

##### identity_loader(self, f):

##### identity_saver(self, f):

##### set_thread_identity(self, identity): g.identity = identity

##### on_identity_changed(self, app, identity):

##### on_before_request(self):

##### is_static_route(self):

#### Adding the Permission Into the Route as Decorator

Within the sponsor dashboard, it is important to add the @sponsor_permission as a decorator.:

```
@sponsor_bp.route('/sponsor/dashboard', methods=['GET','POST'])
@login_required
@sponsor_permission.require(http_exception=403)
def dashboard_sponsor():

```
However, how is sponsor_permission getting information about the user to know that said user is allowed in?
Per the [documentation on Principal here](https://pythonhosted.org/Flask-Principal/):

```
# Create a permission with a single Need, in this case a RoleNeed.
admin_permission = Permission(RoleNeed('admin'))
```
Which, the analog to in our code is, at the top of the __init__.py file:

```
# Permissions and Needs
# setting up a sponsor role from Flask Principal
sponsor_role = RoleNeed('sponsor')
# setting up a sponsor permission
sponsor_permission = Permission(sponsor_role)
```
Which could be re-written:

```
sponsor_permission = Permission(RoleNeed('sponsor'))
```

So, if we add:

```
@sponsor_permission.require(http_exception=403)
```
To our dashboard_sponsor() route, and then try to log in as a sponsor we get the following on our console/webpage:

```
flask  | 172.20.0.1 - - [30/Mar/2021 17:20:11] "POST /login HTTP/1.1" 302 -
flask  | Providing ID:  1  ...to Identity
flask  | Providing Role:  sponsor  ...to Identity
flask  | appended to needs :  [Need(method='role', value='sponsor')]
flask  | 172.20.0.1 - - [30/Mar/2021 17:20:11] "GET /sponsor/dashboard HTTP/1.1" 403 -

```
With message on the webpage:

```
Forbidden

<Permission needs={Need(method='role', value='editor')} excludes=set()>
```
So for some reason, we're seeing the role, 'editor' as a requirement rather than sponsor.

This was simply because we had over-written our permission names incorrectly, basically over-writing sponsor_permission twice.  The correct permissions, established in __init__.py are shown below:

```
# Permissions and Needs
# setting up a sponsor role from Flask Principal
sponsor_role = RoleNeed('sponsor')
# setting up a sponsor permission
sponsor_permission = Permission(sponsor_role)

# setting up an editor role from Flask Principal
editor_role = RoleNeed('editor')
# setting up an editor permission
editor_permission = Permission(editor_role)

```
After this was updated, we get a different error dealing with a database query, we get "TypeError: 'BaseQuery' object is not callable."

This has to do with a login/logout problem we have established and is debugged below under the section:

"Going Back And Fixing User_Type Logic for Login"

Testing whether this permission setting works, I logged in as an editor, then attempted to access the /sponsor/dashboard and got a, "Forbidden" message, as expected.

#### Protecting Other Routes for Other User Types

There are several other routes for sponsors and editors which require protection. The protection can be achieved by decorating the routes as follows:

```
@~route-decorator
@login_required
@role_permission.require(http_exception=403)
def route_function(input):

```
The current routes in need of protection and testing are:

##### Sponsor Routes

Decorate with:

@sponsor_permission.require(http_exception=403)

* /sponsor/documents/<document_id>
* /sponsor/documents
* /sponsor/newdocument
* /sponsor/logout
* /sponsor/dashboard

Testing each of these routes can be done by logging in as a sponsor, and visiting all of the pages. If there is a 403 error as a sponsor, that's bad. Then, logout and login as an editor, if there's not a 403 error as an editor, that's bad.

* After testing all of the routes as a sponsor - they all work.
* After testing all of the routes as an editor - 

* /sponsor/documents/<document_id> - Forbidden
* /sponsor/documents - Forbidden
* /sponsor/newdocument - Forbidden
* /sponsor/logout - Forbidden
* /sponsor/dashboard - Forbidden

* Note, a 404 error is recieved if a trailing / is placed at the end of the URL.
* If attempting to visit, "/" as an editor, we are redirected to, "forbidden."  This can be easily fixed by adding a function under, "/" as follows:

```
# when any user goes to /, they get redirected to /login
@main_bp.route('/', methods=['GET'])
@login_required
# redirect to login page if logged in, to be re-routed to appropriate location
def logindefault():
    # redirect to login page
    return redirect(url_for('auth_bp.login'))
```

##### Editor Routes

Decorate with:

@editor_permission.require(http_exception=403)

After decorating all of the routes, the console prints out error:

```
flask  | NameError: name 'editor_permission' is not defined
```
This was from not importing the "editor_permission" module. On editor:

* /editor/logout
* /editor/dashboard
* /editor/documents
* /editor/documents/<document_id>

On sponsor mode:

* /editor/logout - Forbidden
* /editor/dashboard - Forbidden
* /editor/documents - Forbidden
* /editor/documents/<document_id> - Forbidden

...all of which are expected values.

##### 403 Error Handling

For 403 Error Handling, we just keep everything simple and redirect the user to the main page with no error messages.  This can be improved with more feedback in the future.

I added this to the routes.py file.

```
# Send everything to the login page, don't worry about a message yet.

@sponsor_bp.errorhandler(403)
def sponsor_page_not_found(e):
    # note that we set the 404 status explicitly
    return redirect(url_for('auth_bp.login'))

@editor_bp.errorhandler(403)
def sponsor_page_not_found(e):
    # note that we set the 404 status explicitly
    return redirect(url_for('auth_bp.login'))
```

#### Protecting Individual Assets by User Number - Sponsor Side

Protecting Individual Assets by User Number gets a little more fine-grained, in that if we are a sponsor, we can still view other sponsor documents, and if we are an editor, we can still see other editor documents under:

* /sponsor/documents/<document_id>
* /editor/documents/<document_id>

While a document list view will not be generated that mixes up documents between the different sponsors, individual documents could be accessed through a guess-and-check methodology and through manually typing in URL's.  The server must be explicitly configured to prohibit user id's from not accessing documents they do not have access to.

##### Protecting the Endpoint at the Route on route.py

Looking at the current route for the sponsor/documents/<document_id>:

```
@sponsor_bp.route('/sponsor/documents/<document_id>', methods=['GET','POST'])
@login_required
@sponsor_permission.require(http_exception=403)
def documentedit_sponsor(document_id):


...

    return render_template(
        'documentedit_sponsor.jinja2',
        form=form,
        document=document,
        editor=editor
        )

```

"document_id" is given as an input.  I can write a custom function which dynamically places a permission on this document_id, thereby protecting the endpoint sort of like this:

```
...
def documentedit_sponsor(document_id):
    permission = SponsorEditDocumentPermission(document_id)

    if permission.can():
        # do the edit
        return render_template( stuff )

```
In this case, the function is not a decorator but a regular function call.

The trick is, there must be a Need, which is a named tuple, and a specific class defined to be able to call that permission above.

##### Setting Up Grandular Needs and Permissions on principalmanager.py

On __init__.py:

```

SponsorDocumentNeed = namedtuple('sponsor_document', ['method', 'value'])
SponsorEditDocumentNeed = partial(SponsorDocumentNeed, 'edit')

class SponsorEditDocumentPermission(Permission):
    def __init__(self, document_id):
        need = SponsorEditDocumentNeed(str(document_id))
        super(SponsorEditDocumentPermission, self).__init__(need)

```
What do some of these functions mean, "super" and "namedtuple" and where do they come from?  In order to be able to do a named tuple, we have to import:

```
import collections
from colletions import namedtuple
```
Named tuples work like this:

```
>>> Point = namedtuple('Point', ['x', 'y'])                                            

>>> Point
<class '__main__.Point'>

>>> p=Point(11,22)                                                                          

>>> p0]+p[1]
33                                                                                          
>>> x,y=p

>>> x,y 
(11, 22)

>>> p
Point(x=11, y=22)  
```
The above also makes use of partials.  Partials return a partial object which behave like a function.  Partial freezes some aspects of a function's arguments or keywords resulting in a new object with a simplified signature.

```
# normal function

def f(a,b):                                                                             
...     return a+b

>>> g=partial(f,1)

>>> print(g(1))

2

>>> print(g(2))

3

>>> g=partial(f,1,1)

>>> print(g())

2

```
This also makes use of super() which is used for calling a method of a parent class.  super() basically allows for multiple classes to implement the same method.

##### Checking for Attributes, Checking for Permissions Every Access in __init__.py

Once we have the Permissions and Needs set up properly, it's necessary for check for these needs/permissions upon access within the __init__.py function, as with the sponsor permissions.

This will be done something along the lines of the following:

```
def on_identity_loaded(sender, identity):
    ...

    # if we are a sponsor
        # and if we are in an individual document page that has a document_id
            # if the user has documents
                # query the documents list
                # for document in the current user's documents
                    # add a custom need, an editing/viewing document need to each document
                    identity.provides.add(SponsorEditDocumentNeed(str(document_id)))

```
That's a decent amount to digest. Why am I setting things up in this format?  Basically, I want to avoid querying the database too much, basically optimizing database usage, which means only query when we need to get a list of the documents that belong to a particular user.  This is the reason for the, "if we are an individual document page that has a document_id" - I don't even want to make a query if we are not even using this document id.

Another strategy could be to generate long, random and unguessable strings for document-id's or rather for document-URLs, which could perhaps another layer of security.  But for now, just adding permissions to those individual documents so other users of the same type can't even access each other's documents is an acceptable way to go.

It's probably a better idea to first build the functionality, then optimize for database usage.  Starting out, we come up with the following:

```
from .principalmanager import SponsorDocumentNeed, SponsorEditDocumentNeed

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
        print('Querying Database!', file=sys.stderr)
        current_user_type = User.query.filter(User.id==current_user.id)[0].user_type
        # print userid to console
        print('Providing ID: ',current_user.id,' ...to Identity', file=sys.stderr)
        # provide userid to identity
        identity.provides.add(UserNeed(current_user.id))
        # print user_type to console
        print('Providing Role: ',current_user_type,' ...to Identity', file=sys.stderr)
        # provide user_type to identity
        identity.provides.add(RoleNeed(current_user_type))
        # this is set up in such a way that multiple needs can be added to the same user
        needs = []
        # append sponsor and editor roles depending upon user
        # if current_user_type is sponsor
        if current_user_type == 'sponsor':
            # add sponsor_role, RoleNeed to needs
            needs.append(sponsor_role)
            # query user's documents, filter documents by current sponsor user
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
                identity.provides.add(SponsorEditDocumentNeed(str(document_objects[counter].document_id)))
            # after for loop, show document id's appended to needs
            print('appended document_ids to needs : ',document_id_list, file=sys.stderr)
        # if current_user_type is editor
        elif current_user_type == 'editor':
            # add editor_role, RoleNeed to needs
            needs.append(editor_role)      

        # print everything appended to needs, documents and others
        print('appended to needs : ',needs, file=sys.stderr)
        # add all of the listed needs to current_user

        for n in needs:
            identity.provides.add(n)

```

The key new part of this is:

```
            # query user's documents, filter documents by current sponsor user
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
                identity.provides.add(SponsorEditDocumentNeed(str(document_objects[counter].document_id)))
            # after for loop, show document id's appended to needs
            print('appended document_ids to needs : ',document_id_list, file=sys.stderr)


```
Which basically queries the current_user's documents, creates a list of id's while adding those custom needs, those document id's to the custom function, "SponsorEditDocumentNeed."

Attempting to give some console feedback on what I'm least attempting to do, after logging in as a sponsor and creating a couple different documents, I get:

```
flask  | Querying Database for user_type!
flask  | Providing ID:  3  ...to Identity
flask  | Providing Role:  sponsor  ...to Identity
flask  | Querying Database for document_ids!
flask  | appended document_ids to needs :  [3, 4]
flask  | appended to needs :  [Need(method='role', value='sponsor')]
flask  | 172.20.0.1 - - [31/Mar/2021 16:56:51] "GET /sponsor/documents HTTP/1.1" 200 -
```
So while the above shows that a list of documents, [3,4] is showing for this particular sponsor, which are that particular sponsor's documents, nothing seems to be changing in terms of the specific resource permission.

Looking further at the Flask-Principal documentation, it appears there might need to be another if function to allow the route functionality to work.  The example given shows:

```
@app.route('/posts/<post_id>', methods=['PUT', 'PATCH'])
def edit_post(post_id):
    permission = EditBlogPostPermission(post_id)

    if permission.can():
        # Save the edits ...
        return render_template('edit_post.html')

    abort(403)  # HTTP Forbidden
```

So evidently some kind of, "if permission.can()" function is needed, in lieu of the decorator.

After activating this, including the abort(403) after our main logic, it works, sending the user back to their dashboard per our 403 error.

#### Protecting Individual Assets by User Number - Editor Side

While writing the above permissions aimed at sponsors, I assumed that there would need to be two different permission functions for two different user types - editors and sponsors.

Now I can look at the first section of code written for sponsors and determine if there is some code repeatability that can be built-in.

Here are the main elements that have been built using flask-principal to make this work...basically put:

* DocumentNeed
* EditNeed
* Permission

DocumentNeed is the most fundamental, with input, 'sponsor_document' being arbitrary, and it could be written as follows:

```
SponsorDocumentNeed = namedtuple('document', ['method', 'value'])
```
EditNeed inherits from SponsorDocumentNeed and is used in __init__.py, there is nothing sponsor-specific about EditNeed.

Finally, EditDocumentPermission() is called in the route.py, defined in principalmanager.py and is not toucehd in __init__.py.  The only input here is document_id, and there is nothing specific to the sponsor.  I can go through and re-write everything, coming up with:

```
principalmanager.py

# Individual Document Permissions
# create named tuple for custom permission for accessing individual documents
DocumentNeed = namedtuple('document', ['method', 'value'])
# partial function, freezing 'document' as the method
EditDocumentNeed = partial(DocumentNeed, 'document')

class EditDocumentPermission(Permission):
    def __init__(self, document_id):
        # format input of document_id as a string
        # input to partial function, "SponsorDocumentNeed" which has pre-filled input, "sponsor" as method
        need = EditDocumentNeed(str(document_id))
        # give capability to call this method from other classes with, "super"
        super(EditDocumentPermission, self).__init__(need)

-----

 __init__.py

from .principalmanager import EditDocumentNeed

...

identity.provides.add(EditDocumentNeed(str(document_objects[counter].document_id)))

-----

routes.py

from .principalmanager import EditDocumentPermission

...

permission = EditDocumentPermission(document_id)


```
After making the above edits, the code itself still works flawlessly. Hence, I can use the same set of DocumentNeed, EditNeed and Permission for the editor user_type version of the code, because it's now generalized in natural language.

One tweak that is needed in the __init__.py file to ensure that the functionality works is to change the database lookup.  Basically, since the app is now looking up the editor rather than the sponsor, the query should now look like the following:

```
document_objects = db.session.query(Retention.editor_id,User.id,Retention.document_id,).join(Retention, User.id==Retention.editor_id).join(Document, Document.id==Retention.document_id).order_by(Retention.editor_id).filter(Retention.editor_id == current_user.id)

```
Since this is an editor, there should be an expanded list of documents specifically assigned to that editor which get listed in the document_id needs, as shown below:

```
flask  | Querying Database for user_type!
flask  | Providing ID:  1  ...to Identity
flask  | Providing Role:  editor  ...to Identity
flask  | Querying Database for document_ids!
flask  | appended document_ids to needs :  [1, 2, 3, 4]
flask  | appended to needs :  [Need(method='role', value='editor')]
flask  | 172.20.0.1 - - [31/Mar/2021 17:44:46] "GET /editor/documents HTTP/1.1" 200 -
```
To finalize this, since we no longer have to write any new code under principalmanager.py, we just have to protect the editor individual document route the same way I did with the sponsor individual document routes.

```
    # setup permission for individual document_id
    permission = EditDocumentPermission(document_id)

    # run route function if permission condition satisfied
    if permission.can():

        # stuff

    # abort if permission not satisfied
    # should send back to dashboard
    abort(403)

```
After I checked whether this work...I found that it does!


#### Flask-Principal Documentation - IdentityContext

> The principal behaves as either a context manager or a decorator. The permission is checked for provision in the identity, and if available the flow is continued (context manager) or the function is executed (decorator).


```
    def identity(self):
        """The identity of this principal
        """
        return g.identity

    def can(self):
        """Whether the identity has access to the permission
        """
        return self.identity.can(self.permission)
```

Basically, IdentityContext takes the Identity, compares it to the Permission, which contains Needs, and if the appropriate Needs are found within the logic of Permission, access is granted.

#### Flask-Principal Documentation - Denial

Shortcut for not allowing permission.


#### Going Back And Fixing User_Type Logic for Login

The following logic appears not to work. This appears to be something we could diagnose with the Flask Shell to understand how to print out the user_type as a string rather than an object.

```
        user_type = User.query(User.user_type)
        print(user_type)

        # based upon user type, route to location
        if user_type=='sponsor':
            return redirect(url_for('sponsor_bp.dashboard_sponsor'))
        elif user_type=='editor':
            return redirect(url_for('editor_bp.dashboard_editor'))
```

This code fix could be back-populated into our previous project to ensure workability.

The error we get due to this code, when a user is logged in and then goes off the page and tries to re-visit, is:

```

    File "/usr/src/theapp/project/auth.py", line 33, in login

    user_type = User.query(User.user_type)

    TypeError: 'BaseQuery' object is not callable
```
Basically, we have to filter for the id, and then query for the type from the database, similar to how we do in the __init__.py function.  This function looks like the following:

```
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
        else:
            return redirect(url_for('auth_bp.login'))
    else:
        return redirect(url_for('auth_bp.login'))

```
However, this creates a continuous redirect problem for annonymous users, or users without an id, every time there is a logout.

Basically, we can just eliminate the "redirect()" functions and do nothing for the annonymous user.  After all, this is for a route where the user is already visiting, "login()" so there is no need to redirect them anywhere again.


## Flask Admin

### Background

After successfully completing the above section implementing editor and sponsor permissions, I began the long and greuling task of building an administrative panel.  Ultimately, this admin panel was built based upon a house of cards, and this section will go through what that house of cards was, why it was a poor design for what I'm trying to achieve, and what a better direction would be.

Basically, I had concieved of an idea that I thought would be great for building a highly secure login.  Rather than rely on the, "User" class and risking allowing any instance of, "User" accessing the admin panel, I thought creating a completely different, "kind" of User class, an "Admin" class with one instance or perhaps multiple instances of admins having access to the admin dashboard, with a seperate login, would be a great way to keep things completely seperate and even more secure than the standard model, which is to assign roles to users.

While this is technically possible, and hypothetically more secure if done correctly, it takes a huge amount of work to do it right, increasing the codebase, which actually may in fact decrease rather than increase security, particularly since this is a small project with few resources (e.g. just myself at this point).

Documentation and code for this previous branch attempt has been stored [here](https://github.com/pwdel/flasksecurity/tree/adminuserclass).  Some of the views and methodologies from that codebase can be re-adapted.

The better direction is to simply create a new role, and create permissions for that role in the same way that was done for editor and sponsor. Part of the reason is because some of the existing modules I'm using, such as flask_login, rely on a class called current_user, which requires the user class name to be, "User," and if not, there is a requirement to switch the, "login type" within the session, which gets complicated in terms of it being tricky to sort for the, "session user type" based upon what dashboard a user is logging into and out of, and also assigning user-id's to admins and those user-id's being the same as a user, which allows one instance of User to log into the Admin dashboard.

Simpler would be to just go ahead and create another user, an Admin user, with fixed capabilities, username, and password, and without the capability to create another admin, and set permissions digligently for that admin.

### Objective of Admin Panel

The purpose of an admin panel within this app would be primarily to approve and deny users. The crux of this step of the application building process is to focus on security and permissions. A crucial part of security and permissions is being able to have a high-level account which can provide or deny access.


### Saved States

Saved design states will be kept at the following branches:

* Clean, raw design state with only editor/user working permissions functionality will be saved at :

https://github.com/pwdel/flasksecurity/tree/sponsoreditorpermissions


* Attempt at creating a completely different admin user class functionality, failed will be saved at :

https://github.com/pwdel/flasksecurity/tree/adminuserclass

#### About Reverting and Saving States

Informatin on how to revert and save states using Git was found here:

1. [Seeing All Recent Commits on Branches](https://stackoverflow.com/questions/33926874/in-github-is-there-a-way-to-see-all-recent-commits-on-all-branches)
2. [Git Commit ID](https://stackoverflow.com/questions/29106996/what-is-a-git-commit-id)
3. [Restore a Previous Version of a Git Commit](https://stackoverflow.com/questions/44727750/how-do-i-restore-a-previous-version-as-a-new-commit-in-git)
4. [Forcing Git Commands](https://stackoverflow.com/questions/39399804/updates-were-rejected-because-the-tip-of-your-current-branch-is-behind-its-remot)


### Admin Username, Password and Role Creation

The username and password can still come from an environmental variable, just as we had done with our "adminuserclass" build-out.  Within development mode, a simple shell command can be used to create the user for testing purposes. In production, we could hypothetically do the same, or create a function that automatically creates the first admin user upon deployment.

This can be the only set way to create said user, increasing security by allowing no user registration on the admin side or admin view, only log-in.

#### Authorization with Environmental Variables

So what do we do if we want to store a username and password as an environmental variable? We can set this up in the a new, "adminsettings.py" file.

```
# administrative username and password for development
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'password'
    ADMIN_TYPE = 'admin'
    # for production
    # ADMIN_USERNAME = 'environ.get('ADMIN_USERNAME')
    # ADMIN_PASSWORD = 'environ.get('ADMIN_PASSWORD')
    # ADMIN_TYPE = 'environ.get('ADMIN_TYPE')
```

### Admin Authentication and Login

* To ofuscate the fact that an admin even exists, this user could login within the standard login page at the front of the app itself, with nothing prompting nor hinting that an admin exists. Rather, if the appropriate username and password is entered, then the auth.py route can send the user to the appropriate dashboard for the 'admin' type of User.
* An admin login can be its own route and blueprint, essentially an admin dashboard. Permissions can be set up to prevent other types of users from accessing admin, just as is currently working with, "sponsor" and "editor."

#### Admin Type Login

The crux of the login for any user type is the login validation:

```
    # Validate login attempt
    if form.validate_on_submit():
        
        ...

            # check user type, if sponsor go to sponsor dashboard
            if user.user_type=='sponsor':
                # redirect to sponsor dashboard
                return redirect(url_for('sponsor_bp.dashboard_sponsor'))
            # if user type is editor, send to editor dashboard
            elif user.user_type=='editor':
                # redirect to editor dashboard
                return redirect(url_for('editor_bp.dashboard_editor'))
```
To validate for an admin login, I can simply add:

```

...

            # check user type, if sponsor go to sponsor dashboard
            if user.user_type=='sponsor':
                # redirect to sponsor dashboard
                return redirect(url_for('sponsor_bp.dashboard_sponsor'))
            # if user type is editor, send to editor dashboard
            elif user.user_type=='editor':
                # redirect to editor dashboard
                return redirect(url_for('editor_bp.dashboard_editor'))
            elif user.user_type=='admin':
                # redirect to editor dashboard
                return redirect(url_for('admin_bp.dashboard_admin'))



```
Of course the admin user must have the admin type in order for this to work.

#### Admin Bypass Login

Similar to above, the admin user type can bypass login:

```
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
            elif current_user_type=='admin':
                return redirect(url_for('admin_bp.dashboard_admin'))

```

#### Signing Up Admin Route

There is no sign up for admin - the should only be one way to set up an admin, basically by a direct entry into the database through a shell command (or upon startup using stored environmental variables).


#### Admin Blueprints

Above in the auth.py file, the following was added:

```
    return redirect(url_for('admin_bp.dashboard_admin'))
```
This means an admin_bp as well as page views for dashboard_admin should be created, along with a folder.

1. Need to register those blueprints on __init__.py at "app.register_blueprint(routes.admin_bp)"
2. Add the blueprint to route.py at the top near the editor and sponsor blueprint.
3. Within auth.py add "from .routes import sponsor_bp, editor_bp, admin_bp"

Hypothetically, if all of the above are in place, then the blueprint shuold work.

#### Simplified Admin Dashboard Page View, route and Admin Logout Logic

The dashboard can be a very simple .jinja2 file with just a logout button to start off with, discussed below.  The route for this can be:

```
@admin_bp.route('/admin/dashboard', methods=['GET','POST'])
@login_required
# @admin_permission.require(http_exception=403)
def dashboard_admin():
    """Logged-in User Dashboard."""
    return render_template(
        'dashboard_admin.jinja2',
        title='Admin Dashboard',
        template='layout',
        body="Welcome to the Admin Dashboard."
    )
```

The Admin dashboard page can be the following:

```
      <a href="{{ url_for('admin_bp.logoutadmin') }}">Log Out.</a>
```

However then a route is needed to achieve that logout function.  For now we can create the admin logout route without anything else special, and forgo permissions as we have not builg permissions logic for admin yet.

```
@admin_bp.route("/admin/logout")
@login_required
# @admin_permission.require(http_exception=403)
def logoutadmin():
    """User log-out logic."""
    logout_user()
    # tell flask principal the user is annonymous
    identity_changed.send(current_app._get_current_object(),identity=AnonymousIdentity())
    # print annonymousidentity to console
    identity_object = AnonymousIdentity()
    # printing identity_object to console for verification
    print('Sent: ',identity_object,' ...to current_app', file=sys.stderr)
    return redirect(url_for('auth_bp.login'))
```

#### Starting Up and Adding Admin User to Test

We do the ol' "sudo docker exec -it flask /bin/bash" and then, "flask shell" to gain entry to the shell.


To start off with, before being fancy and using any environmental variables, which would need to be imported into the shell in one way or another, a new user of type admin can be created like so:

```
user = User(name='Person Admin', email='admin@test.com', organization='WhateverCo', user_type='admin')
# use our set_password method
user.set_password('password')
# commit our new user record and log the user in
db.session.add(user)
db.session.commit()  

```

Then to verify that the user has been entered into the database, login to the databse itself to be able to enter in some of the ol' SQL...

```
---+--------------+------------+------------                                                                                    
  1 | Person Admin | admin     | admin@test.com 
```

And we can see above that the user exists, so we can attempt to log in with this user...and everything works as expected!

### Admin Permissions

Viewing the output from the console, the following can be viewed:

```
flask  | Querying Database for user_type!
flask  | Providing ID:  1  ...to Identity
flask  | Providing Role:  admin  ...to Identity
flask  | appended to needs :  []

```

So, identity assignment already appears to be working, and it may only be a matter of using a decorator assignment to add the proper permissions.

First, to make sure permissions are open, I simply created a new sponsor user and then visited /admin/dashboard - sure enough, I was able to view the dashboard for the admin, even logged in as a sponsor rather than as an admin.

Permissions are handed out via flask_principal on an ongoing basis at the __init__.py function.

For needs,

```
        print('Querying Database for user_type!', file=sys.stderr)
        current_user_type = User.query.filter(User.id==current_user.id)[0].user_type
        # print userid to console
        print('Providing ID: ',current_user.id,' ...to Identity', file=sys.stderr)
        # provide userid to identity
        identity.provides.add(UserNeed(current_user.id))
        # print user_type to console
        print('Providing Role: ',current_user_type,' ...to Identity', file=sys.stderr)
        # provide user_type to identity
        identity.provides.add(RoleNeed(current_user_type))
        # this is set up in such a way that multiple needs can be added to the same user
        needs = []
```
Admin doesn't have individual documents seperates by individual users, so there is no need to create complex if statements assigning invididual needs to each admin user - there is only one admin user.

These roles are defined at the top of __init__.py, and I can add a new admin permission and role as follows:

```
# setting up admin permission
admin_role = RoleNeed('admin')
# setting up an admin permission
admin_permission = Permission(admin_role)

```

Having done that, the decorator now has access to the admin role/permission type, assuming it was imported correctly:

```
from . import sponsor_permission, editor_permission, admin_permission

...

@admin_permission.require(http_exception=403)

```

The above decorator gets added to all relevant admin routes.  After testing with an alternate, sponsor type account, it works, throwing up a forbidden 403 error.  This can of course be handled by a 403 handler within the routes.py file.

```

@admin_bp.errorhandler(403)
def admin_page_not_found(e):
    # note that we set the 404 status explicitly
    return redirect(url_for('auth_bp.login'))

```

### Designing The Admin Dashboard





## Reviewing Flask Security Considerations

Many security recommendations are largely identified and called out within the [Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/security/).

### XSS

From [this article](https://smirnov-am.github.io/securing-flask-web-applications/). Also covered [here](https://flask.palletsprojects.com/en/1.1.x/security/#x-xss-protection).

Cross-Site scripting (XSS) are a type of injection, in which malicious scripts are injected into other wise trusted websites.

Basically, attackers could put scripts that involve javascript alerts, which if later displayed on a user's view in a different context, could execute javascript on their browser.

For example, an attacker could put the following into a form, which would pull up an alert:

```
<script>alert(1)</script>
```

#### Mitigation

> When rendering templates Flask configures Jinja2 to automatically escape all values unless explicitly told otherwise.

> Templates loaded from a string will have auto-escaping disabled.

1. You can provide an [X-XSS Header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-XSS-Protection) for old browsers which don't have it by default.
2. Use {{ url_for('endpoint')}} when rendering template. This has additional benefit of automatically building proper URLs if endpoint path changes.
3. Create a Content-Security-Policy header and add it to the routes.  Also covered in [Flask Content Security Policy](https://flask.palletsprojects.com/en/1.1.x/security/#content-security-policy-csp).

#### Analsis

I'm already rendering templates by endpoint, but don't have a Content-Security-Policy header.  Need to create something like the following and perhaps import it for every route.

```
@app.route('/', methods=['GET', 'POST'])
def tweet_feed():
if request.method == 'POST':
    tweet = request.form['tweet']
    tweets.append(tweet)
response = make_response(render_template('tweet_feed.html', tweets=tweets))
response.headers['Content-Security-Policy'] = "default-src 'self'"
return response
```

### CSRF

From [this article](https://smirnov-am.github.io/securing-flask-web-applications/).

Cross-Site Request Forgery attack basically captures a user cookie from another website and sends it back to the hacker's server. In this attack, a user is tricked to visiting a hacker's website, perhaps via a spam message which says, "transaction approved" or something like that. The hacker's website then redirects the user over to a bank account site, for example, "Bank X," which is perhaps a very common bank.  If the user is logged in at Bank X, after the redirect, the hacker's server can capture the user's cookie by having that user's browser send it back to the hacker server, thereby allowing the hacker to log in under ther user's bank account (as an example).

#### Mitigation

* Avoid using the POST method at all costs, and only use GET if possible.  This would basically mean that if only GET is allowed within a function/method/page, then malicious scripts can't be loaded via POST.
* Or alternatively, use dynamic tokens which change upon each POST, or gets a random token as a form's hidden field when a form is POSTed.  In Flask this is already implemented in Flask-WTF plugin.
* Use CSRF tokens.

#### Analysis

* We already seem to be using the above mitigation methods.

### SQL Injection

From [this article](https://smirnov-am.github.io/securing-flask-web-applications/).

> Often occurs when using string formatting or concatenation to build queries.

#### Mitigation

Basically, use ORM's, rather than low level SQL Executables.

#### Analysis

Within SQLAlchemy, so far we are using ORM's and not low-level executables.

### Directory Traversal

From [this article](https://smirnov-am.github.io/securing-flask-web-applications/).

> Directory traversal may happen when for example an attacker uploads a file with a filename like ../../../etc/passwd. If he guessed the number of .. right he might overwrite the file.

#### Mitigation

Basically, sanitize filename extensions on the upload form, and don't upload files directly to the server, use a relational database and point to an external service such as S3 for file uploads.

### XSS Uploaded Files

From [this article](https://smirnov-am.github.io/securing-flask-web-applications/).

> This is not particularly related to Flask, but malicious javascript might appear not only in reflected output or stored in database (see general XSS attack), but it can also be embedded in images.For example, this blog post uses that code to embed javascript in GIF image file. CSP won’t help here - so the only way is to serve the images from separate subdomain (that’s what actually Facebook does)

### JSON Security

From [this Flask Security Considerations](https://flask.palletsprojects.com/en/1.1.x/security/#security-headers)

Only extremely old browsers are vulnerable.

### Flask Security Headers

> Browsers recognize various response headers in order to control security. We recommend reviewing each of the headers below for use in your application. The Flask-Talisman extension can be used to manage HTTPS and the security headers for you.

From [this Flask Security Considerations](https://flask.palletsprojects.com/en/1.1.x/security/#json-security)

[Flask Talisman can be used to manage headers](https://github.com/GoogleCloudPlatform/flask-talisman).


### Cookie Protection - Secure

> Basically, if an attacker controls network equipment between a user and the server (or an ISP), the attacker can read the cookies.  Setting Cookie=Secure will instruct the browser to send a cookie only over HTTPS.

From [this article](https://smirnov-am.github.io/securing-flask-web-applications/).

[Flask Talisman can be used to manage headers](https://github.com/GoogleCloudPlatform/flask-talisman).


### Cookie Protection - HTTP Only

This will instruct a browser to hide the cookie from javascript code.

From [this article](https://smirnov-am.github.io/securing-flask-web-applications/).

### Cookie Protection - SameSite

Similar to the CSRF attack, a user's cookie was sent from an attacking site, creates an open door. Setting SameSite=strict will mitigate this attack.  Another option is, "lax" which won't allow sending cookies from other sites at all when doing any type of request other than GET.

From [this article](https://smirnov-am.github.io/securing-flask-web-applications/). Also covered [here](https://flask.palletsprojects.com/en/1.1.x/security/#set-cookie-options).


```
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)


response.set_cookie('username', 'flask', secure=True, httponly=True, samesite='Lax')
```

Can also set the cookie to expire in 10 mins.

```
# cookie expires after 10 minutes
response.set_cookie('snakes', '3', max_age=600)
```

### X Content Type Options

> Forces the browser to honor the response content type instead of trying to detect it, which can be abused to generate a cross-site scripting (XSS) attack.

From [here](https://flask.palletsprojects.com/en/1.1.x/security/#x-content-type-options).

### X-Frame Options

> Prevents external sites from embedding your site in an iframe. This prevents a class of attacks where clicks in the outer frame can be translated invisibly to clicks on your page’s elements. This is also known as “clickjacking”.

From [here](https://flask.palletsprojects.com/en/1.1.x/security/#x-frame-options)

```
response.headers['X-Frame-Options'] = 'SAMEORIGIN'
```

    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options


### X-XSS-Protection

> The browser will try to prevent reflected XSS attacks by not loading the page if the request contains something that looks like JavaScript and the response contains the same data.

```
response.headers['X-XSS-Protection'] = '1; mode=block'
```

    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-XSS-Protection


### HTTP Public Key Pinning

> This tells the browser to authenticate with the server using only the specific certificate key to prevent MITM attacks.

From [here](https://flask.palletsprojects.com/en/1.1.x/security/#http-public-key-pinning-hpkp).

Warning

Be careful when enabling this, as it is very difficult to undo if you set up or upgrade your key incorrectly.


### Copy/Paste to Terminal

From [here](https://flask.palletsprojects.com/en/1.1.x/security/#copy-paste-to-terminal)

> Most modern terminals will warn about and remove hidden characters when pasting, so this isn’t strictly necessary. It’s also possible to craft dangerous commands in other ways that aren’t possible to filter. Depending on your site’s use case, it may be good to show a warning about copying code in general.

## Overall Analysis

At this point in our application evolution, we don't have super strict security requirements, as we don't even have a large number of users on the site, and there isn't really anything valueable to protect - it's just a demo.

Longer-term, probably the most urgent security needs will deal with gaining access to valuable and expensive server resources, which probably means having strict user authorization and authentication protocols, and a well-organized user role system.

If we implement a REST-API we need to be careful about that as well.  Basically we don't want to eat up valuable Machine Learning server dollars for any proof of concepts that we happen to building.

Other Ideas:

* [Prevent a Route from Being Accessed Unless Another Route Had Been Visited First](https://stackoverflow.com/questions/42450813/in-flask-how-do-i-prevent-a-route-from-being-accessed-unless-another-route-has)
* [Limit Access to Flask to IP Address](https://stackoverflow.com/questions/22251038/how-to-limit-access-to-flask-for-a-single-ip-address)
* [Restrict Acceess to Website API with Flask-CORS](https://stackoverflow.com/questions/54171101/restrict-access-to-a-flask-rest-api)
* [X-Frame Options](https://flask.palletsprojects.com/en/1.1.x/security/#x-frame-options)

Other than standard security loopholes, there is also inner-app security loopholes which involve protecting user's assets from each other.  This is more of an interference-restriction or resource access practice than a pure security practice, however it could also be adopted as an, "exterior" security feature in the future.  Basically:

* For individual documents or assets owned by a user, generate URLs which are obscured by highly unguessable, long-form URL's on a per-post basis, rather than /document/1, /document/2, etc., which are highly guessable and have a pattern.  This is a sort of, "security by obscurity" practice that could be adopted to share assets with the open web if that is a user/customer need.

## Security Possible To Do List for Review

* Content-Security-Policy header should be provided on every route.
* Add [Flask Talisman](https://github.com/GoogleCloudPlatform/flask-talisman)
* Cookie Protection - HTTP Only, From [this article](https://smirnov-am.github.io/securing-flask-web-applications/).
* Cookie Protection - SameSite From [this article](https://smirnov-am.github.io/securing-flask-web-applications/).


## Future Work - Possible To Do List

### Postgres Query Optimization

Currently, every time an identity is loaded, which is basically every user action, we query the database for the user type.

```
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):

...

# Query user type given user.id
        # printing the fact that we are querying db
        print('Querying Database!', file=sys.stderr)
        current_user_type = User.query.filter(User.id==current_user.id)[0].user_type

```
With one or two users performing a few simple actions, this may not matter.  However long-term, with an app that has a number of users, we may want to find a way to simply persist the user credentials in the session rather than querying the database every time.

### Decide How to Treat Strict Slashes

The following will treat slashes non-strictly, if added under the route.  Otherwise, Werkzeug interprets as an explicit rule to not match a trailing slash.

* strict_slashes=False

Otherwise, explicitly list all slash conditions for each route.


### Setting Up a .env File

Per [this article](https://itnext.io/start-using-env-for-your-flask-project-and-stop-using-environment-variables-for-development-247dc12468be).


## References

* [Demystifying Flask Principal](https://jupyterdata.medium.com/a-shot-at-demystifying-flask-principal-dda5aaeb6bc6)
* [Securing Flask Web Applications](https://smirnov-am.github.io/securing-flask-web-applications/)
* [Flask Security Considerations](https://flask.palletsprojects.com/en/1.1.x/security/)
* [Django vs Flask](https://testdriven.io/blog/django-vs-flask/)
* [Flask Principal Documentation](https://pythonhosted.org/Flask-Principal/)
* [Flask Principal Implementation Blog](https://terse-words.blogspot.com/2011/06/flask-extensions-for-authorization-with.html)
