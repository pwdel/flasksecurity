# Importing Flask Principal Stuff
from flask_principal import identity_loaded, Principal, Permission, UserNeed, RoleNeed

from collections import namedtuple
from functools import partial

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


