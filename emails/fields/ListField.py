import logging
import random

from emails.fields import Field
from helpers.FilesHelper import FilesHelper

logger = logging.getLogger()


class ListField(Field):
    """
    List field.
    """

    def __init__(self, email, elements_type):
        """
        Generate field content.
        Require fields: -
        :param email: Parent Email object.
        :param elements_type: Type of elements to hold.
        """
        super().__init__(email)
        self.elements_type = elements_type

        # We need to be able to access this value before generation
        # to be able to add fields
        self.values = []

    def generate(self):
        """
        Start the field generation process.
        """
        super().generate()

        for value in self.values:
            value.generate()

    def add(self, value):
        logger.debug(f"Adding list element")
        self.values.append(value)

    def __str__(self):
        """
        String representation of the list.
        :return: List joined with ", " or "" if empty.
        """
        if len(self.values) == 0:
            return ""

        values_str = [str(value) for value in self.values]
        return ", ".join(values_str)
