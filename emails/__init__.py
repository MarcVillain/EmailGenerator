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

    def __init__(self, email, values=None):
        """
        Initialize necessary variables.
        :param email: Parent Email object.
        :param values: (Optional) Name and value fields preset.
        """
        if values is None:
            values = dict()

        self.email = email
        self.values = values

    def _build(self, value):
        """
        Build a value based on its type.
        :param value: Class to instantiate or already instantiated class.
        :return: Instance of a Field object.
        """
        # TODO: Add check for Field type
        if inspect.isclass(value):
            return value(self.email)
        else:
            return value

    def add(self, name, value):
        """
        Add a field. A field cannot be added twice.
        :param name: Name of the field.
        :param value: Class to instantiate or already instantiated class.
        """
        if self.get(name):
            logger.debug(f"Field '{name}' already added")
            return

        logger.debug(f"Adding field '{name}'")
        self.values[name] = self._build(value)

    def update(self, name, value):
        """
        Update a field's value. If the field does not exists, it will be added.
        :param name: Name of the field.
        :param value: Class to instantiate or already instantiated class.
        """
        logger.debug(f"Updating field '{name}'")
        old_value = self.get(name)
        if not old_value:
            self.add(name, value)
            return

        self.values[name] = self._build(value)

    def get(self, name, default=None):
        """
        Get a field.
        :param name: Name of the field.
        :param default: Default Field class or object if not found.
        :return: The Field object if found else default.
        """
        value = self.values.get(name)
        if value is None:
            logger.debug(f"Field '{name}' not found")
            return None if default is None else self._build(value)

        return value

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

    def __init__(self, template, fields_values=None, **kwargs):
        """
        Initialize necessary variables.
        :param template: Name of the template to use.
        :param fields_values: (Optional) Name and value fields preset.
        """
        logger.debug(f"Generate {self.__class__.__name__} with {template} template")

        self.template = template
        self.fields = Fields(self, values=fields_values)

    def get_field(self, name, default=None):
        """
        Get the value of a field.
        :param name: Name of the field.
        :param default: Default Field class or object if not found.
        :return: The Field object.
        """
        return self.fields.get(name, default=default)

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
