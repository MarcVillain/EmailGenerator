import inspect
import logging
import os
import pathlib
from abc import ABC
from string import Template

from emails.fields import Field
from emails.fields.ContactField import ContactField
from emails.fields.DateField import DateField
from emails.fields.IdField import IdField
from emails.fields.MessageField import MessageField
from emails.fields.StringField import StringField
from emails.fields.SubjectField import SubjectField
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
        self.template_fields = dict()

        self.name_to_class = {
            "FROM": ContactField,
            "SENDER": ContactField,
            "TO": ContactField,
            "DATE": DateField,
            "MESSAGE_ID": IdField,
            "MESSAGE": MessageField,
            "SUBJECT": SubjectField,
        }

    def _build(self, value, generate=True):
        """
        Build a value based on its type.
        :param value: Class to instantiate or already instantiated class.
        :param generate: Should we call generate?
        :return: Instance of a Field object.
        """
        if isinstance(value, str):
            value = StringField(value, self.email)

        elif inspect.isclass(value):
            if not issubclass(value, Field):
                logger.error("Trying to build a non-Field class")
                return StringField("TYPE_ERROR", self.email)
            value = value(self.email)
        elif not isinstance(value, Field):
            logger.error("Trying to build a non-Field object")
            return StringField("TYPE_ERROR", self.email)

        if generate:
            value.generate()

        return value

    def _update_template_field(self, name, value):
        """
        Save template field name and value for further use
        """
        self.template_fields[name] = str(value)
        for field_name, field_value in value.__dict__.items():
            if field_name == "email":
                continue
            self.template_fields[
                name + "__" + str(field_name)
            ] = field_value

    def preset_values(self, values):
        """
        Preset values.
        :param values: (Optional) Name and value fields preset.
        """
        # Values is a dictionnary of name/value set which are both strings.
        # We need to convert them to actual Field objects before use.
        for name, value in values.items():
            if name in self.name_to_class.keys():
                field_type = self.name_to_class.get(name)
                self.values[name] = field_type(self.email)
                for n, v in value.items():
                    setattr(self.values[name], n, v)
            else:
                self.values[name] = self._build(str(value), generate=False)

    def add(self, name, value=None):
        """
        Add a field. A field cannot be added twice.
        :param name: Name of the field.
        :param value: (Optional) Class to instantiate or already instantiated class.
        :return: The added Field object.
        """
        if value is None:
            value = self.name_to_class.get(name)

        if self.get(name):
            logger.debug(f"Field '{name}' already added")
            value = self.get(name)
            value.generate()  # Generate all missing attributes
            self._update_template_field(name, value)
            return value

        logger.debug(f"Adding field '{name}'")
        self.values[name] = self._build(value)

        value = self.get(name)
        self._update_template_field(name, value)
        return value

    def update(self, name, value):
        """
        Update a field's value. If the field does not exists, it will be added.
        :param name: Name of the field.
        :param value: Class to instantiate or already instantiated class.
        :return: The updated Field object.
        """
        old_value = self.get(name)
        if not old_value:
            return self.add(name, value)

        logger.debug(f"Updating field '{name}'")
        self.values[name] = self._build(value)

        value = self.get(name)
        self._update_template_field(name, value)
        return value

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

    def __init__(self, template, **kwargs):
        """
        Initialize necessary variables.
        :param template: Name of the template to use.
        :param fields_values: (Optional) Name and value fields preset.
        """
        logger.debug(
            f"Generate {self.__class__.__name__} with {template} template"
        )

        self.template = template
        self.fields = Fields(self)

    def preset(self, fields_values):
        """
        Preset necessary variables.
        :param fields_values: (Optional) Name and value fields preset.
        """
        self.fields.preset_values(fields_values)

    def gen_fields(self):
        """
        Generate fields.
        ! Be careful when changing this, order matters.
        """
        pass

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
