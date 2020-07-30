import random

from emails.fields.ContactField import ContactField
from emails.fields.ListField import ListField
from helpers.FilesHelper import FilesHelper


class ContactListField(ListField):
    """
    Contact list field.
    """

    def __init__(self, email):
        """
        Generate field content.
        Require fields: -
        :param email: Parent Email object.
        """
        super().__init__(email, elements_type=ContactField)
