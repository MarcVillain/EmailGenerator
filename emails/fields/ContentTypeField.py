import uuid
from datetime import datetime

from emails.fields import Field


class ContentTypeField(Field):
    """
    ContentType field.
    """

    def __init__(self, email):
        """
        Generate field content.
        Require fields: -
        :param email: Parent Email object.
        """
        super().__init__(email)

    def generate(self):
        """
        Start the field generation process.
        """
        super().generate()

        if not hasattr(self, "type"):
            self.type = 'text/plain; charset="iso-8859-1"'

    def __str__(self):
        """
        String representation of the ContentType.
        :return: ContentType field string representation, double-quoted.
        """
        return self.type
