import random

from emails.fields import Field
from helpers.FilesHelper import FilesHelper


class ContactField(Field):
    def __init__(self, fields):
        super().__init__(fields)

        self.first = self._generate_first_name()
        self.last = self._generate_last_name()
        self.email = "{}.{}@fic.com".format(self.first.lower(), self.last.lower())

    def _generate_first_name(self):
        return random.choice(FilesHelper.content.get("first_names")).title()

    def _generate_last_name(self):
        return random.choice(FilesHelper.content.get("last_names")).upper()

    def __str__(self):
        return f"{self.first} {self.last} <{self.email}>"
