import inspect
import logging
import os
import pathlib
from abc import ABC
from string import Template

from emails.fields import Field
from helpers.FilesHelper import FilesHelper

logger = logging.getLogger()


class Fields:
    """
    Email fields manipulator.
    """

    def __init__(self, email):
        """
        Initialize necessary variables.
        :param email: Parent Email object.
        """
        self.email = email

        self.values = dict()

    def add(self, name, value):
        """
        Add a field.
        :param name: Name of the field.
        :param value: Class to instantiate or already instantiated class.
        """
        logger.debug(f"Adding field '{name}'")
        if inspect.isclass(value):
            self.values[name] = value(self.email)
        else:
            self.values[name] = value

    def get(self, name):
        """
        Get a field.
        :param name: Name of the field.
        :return: The Field object.
        """
        return self.values[name]

    def as_str_dict(self):
        """
        Return the fields as a directory of key: str(value).
        :return: Directory of the fields in string representation.
        """
        return {key: str(value) for key, value in self.values.items()}


class Email(ABC):
    """
    Email object.
    """

    def __init__(self, template):
        """
        Initialize necessary variables.
        :param template: Name of the template to use.
        """
        logger.debug(f"Generate {template} email")

        self.template = template
        self.fields = Fields(self)

    def get_field(self, name):
        """
        Get a field.
        :param name: Name of the field.
        :return: The Field object.
        """
        return self.fields.get(name)

    def __str__(self):
        """
        String representation of the email.
        The template is loaded and all fields are replaced
        with the earlier generated values.
        :return: Email string representation.
        """
        content = ""
        template_path = os.path.join(FilesHelper.templates_dir, self.template)

        logger.debug(f"Apply {self.template} template")
        with open(template_path, "r") as input_file:
            content = Template(input_file.read())
            content = content.substitute(self.fields.as_str_dict())

        return content
