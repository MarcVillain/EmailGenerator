import uuid
from datetime import datetime

from emails.fields import Field


class IdField(Field):
    """
    Id field.
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

        if not hasattr(self, "id"):
            self.id = uuid.uuid4()

    def __str__(self):
        """
        String representation of the id.
        :return: Id field string representation, double-quoted.
        """
        return f'"{self.id}"'
