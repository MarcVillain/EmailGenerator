import logging
import os
import pathlib
from abc import ABC
from string import Template

logger = logging.getLogger()


class Fields:
    def __init__(self):
        self.values = dict()

    def add(self, name, value):
        self.values[name] = value(self)

    def get(self, name):
        return self.values[name]

    def as_str_dict(self):
        return {key: str(value) for key, value in self.values.items()}


class Email(ABC):
    def __init__(self, template):
        logger.debug("Generate {template} email")

        self.template = template
        self.fields = Fields()

    def get_field(self, name):
        return str(self.fields.get(name))

    def __str__(self):
        this_file_path = pathlib.Path(__file__).parent.absolute()
        template_path = os.path.join(this_file_path, "templates", self.template)

        content = ""

        logger.debug(f"Apply {self.template} template")
        with open(template_path, "r") as input_file:
            content = Template(input_file.read())
            content = content.substitute(self.fields.as_str_dict())

        return content
