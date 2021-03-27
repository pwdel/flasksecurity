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

## Flask Admin





















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



## Security Possible To Do List for Review

* Content-Security-Policy header should be provided on every route.
* Add [Flask Talisman](https://github.com/GoogleCloudPlatform/flask-talisman)
* Cookie Protection - HTTP Only, From [this article](https://smirnov-am.github.io/securing-flask-web-applications/).
* Cookie Protection - SameSite From [this article](https://smirnov-am.github.io/securing-flask-web-applications/).



## References

* [Demystifying Flask Principal](https://jupyterdata.medium.com/a-shot-at-demystifying-flask-principal-dda5aaeb6bc6)
* [Securing Flask Web Applications](https://smirnov-am.github.io/securing-flask-web-applications/)
* [Flask Security Considerations](https://flask.palletsprojects.com/en/1.1.x/security/)
* [Django vs Flask](https://testdriven.io/blog/django-vs-flask/)
* [Flask Principal Documentation](https://pythonhosted.org/Flask-Principal/)
* [Flask Principal Implementation Blog](https://terse-words.blogspot.com/2011/06/flask-extensions-for-authorization-with.html)
