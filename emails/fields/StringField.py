import re

import requests

from emails.fields import Field


class StringField(Field):
    """
    String field.
    """

    def __init__(self, value, email):
        """
        Generate field content.
        :param email: Parent Email object.
        """
        super().__init__(email)

        # This special field requires pre-initialization of the the field
        if not hasattr(self, "value"):
            self.value = value

    def generate(self):
        """
        Start the field generation process.
        """
        super().generate()

    def __str__(self):
        """
        String representation of the string field.
        :return: String field string representation.
        """
        return self.value
