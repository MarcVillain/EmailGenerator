import random

from emails.fields import Field
from helpers.FilesHelper import FilesHelper


class ContactField(Field):
    """
    Contact field.
    """
    def __init__(self, email):
        """
        Generate field content.
        Require fields: -
        :param email: Parent Email object.
        """
        super().__init__(email)

        self.first = self._generate_first_name()
        self.last = self._generate_last_name()
        self.email_addr = "{}.{}@fic.com".format(self.first.lower(), self.last.lower())

    def _generate_first_name(self):
        """
        Generate random first_name from 'first_name' data list.
        :return: Random first_name, with first letter in uppercase
                 and others in lowercase.
        """
        return random.choice(FilesHelper.content.get("first_names")).title()

    def _generate_last_name(self):
        """
        Generate random last_name from 'last_name' data list.
        :return: Random last_name in full uppercase.
        """
        return random.choice(FilesHelper.content.get("last_names")).upper()

    def __str__(self):
        """
        String representation of the contact.
        :return: Contact field as 'First LAST <first.last@fic.com>'.
        """
        return f"{self.first} {self.last} <{self.email_addr}>"
