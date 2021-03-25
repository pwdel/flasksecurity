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

## Evaluating Options

| Name               | Link                                         | Last Updated |
|--------------------|----------------------------------------------|--------------|
| Flask-Security     | https://pypi.org/project/Flask-Security/     | July 2017    |
| Flask-Security-Too | https://pypi.org/project/Flask-Security-Too/ | Jan 2021     |
| Flask-Principal    | https://pypi.org/project/Flask-Principal/    | July  2013   |
| Flask-Unchained    | https://pypi.org/project/Flask-Unchained/    | Jan 2021     |

## Reading Through Tutorials

### Flask-Security

Flask-Security seems to be somewhat deprecated.  It appears to still be in use, but is not as frequently updated.  The main criteria for modules is whether it fits into your specific project, which means taking stock of what parameters you are looking for and why, as well as evaluating each module on its merits.

This project is being built by one person for the time being, so customization of code is a problem.  Basically even if Flask-Security with customizations would provide better security, that would be not as desirable as something that is more plug and play.  What I'm trying to secure just isn't that valuable yet.

### Flask-Principal

Flask-Principal seems to be even more deprecated than Flask-Security, so the same rationale applies.

### Flask-Security-Too

[Flask Security Too docs](https://flask-security-too.readthedocs.io/en/stable/) show that Flask-Security Too is an attempt to keep the flask-Security projet going.

Features within Flask-Security-Too include:


* Flask-Login
* Flask-Mail
    Flask-Principal
    Flask-WTF
    itsdangerous
    passlib
    PyQRCode


### Flask-Unchained

[Flask-Unchained Docs](https://flask-unchained.readthedocs.io/en/latest/index.html) show that Unchained is basically a very light version of Django but in Flask form, hence the name, "Unchained."  However, Django includes all different sorts of bundles, while the bundles which are included in Unchained appear to be:

Modules we have:

* Integration with SQLAlchemy and Flask-Migrate
* Integratin with Flask-Login
* Integration with Flask-WTF

New modules:

* Flask-Session
* Flask-Mail
* Flask-Admin
* Flask-Marshmellow (SQLAlchemy model serialization)
* pytest and factory_boy

Basically, all of the normal things you would look for in an out-of-the-box webapp.

There is an [Unchained tutorial](https://flask-unchained.readthedocs.io/en/latest/index.html).

### 