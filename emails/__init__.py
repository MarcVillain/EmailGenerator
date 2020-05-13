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
    def __init__(self, email):
        self.email = email

        self.values = dict()

    def add(self, name, value):
        if inspect.isclass(value):
            self.values[name] = value(self.email)
        else:
            self.values[name] = value

    def get(self, name):
        return self.values[name]

    def as_str_dict(self):
        return {key: str(value) for key, value in self.values.items()}


class Email(ABC):
    def __init__(self, template):
        logger.debug(f"Generate {template} email")

        self.template = template
        self.fields = Fields(self)

    def get_field(self, name):
        return self.fields.get(name)

    def __str__(self):
        content = ""
        template_path = os.path.join(FilesHelper.templates_dir, self.template)

        logger.debug(f"Apply {self.template} template")
        with open(template_path, "r") as input_file:
            content = Template(input_file.read())
            content = content.substitute(self.fields.as_str_dict())

        return content
