from collections import namedtuple
from functools import partial

from flask_login import current_user
from flask_principal import identity_loaded, Permission, RoleNeed, UserNeed


# Permissions and Needs
# setting up a sponsor role from Flask Principal
sponsor_role = RoleNeed('sponsor')
# setting up a sponsor permission
sponsor_permission = Permission(sponsor_role)

# setting up an editor role from Flask Principal
editor_role = RoleNeed('editor')
# setting up an editor permission
sponsor_permission = Permission(editor_role)


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
        identity.provides.add(UserNeed(current_user.id))

    # Assuming the User model has a user_type, update the
    # identity with the user_type that the user provides
    if hasattr(current_user, 'user_type'):
        for role in current_user.user_type
        	# add user_type as a role name
            identity.provides.add(RoleNeed(role.name))
