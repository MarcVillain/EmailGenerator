from abc import ABC
from string import Template


class Field(ABC):
    def __init__(self, email):
        self.email = email

        # Save template fields key and value for easier templating
        # See _substitute_fields
        self.template_fields = {}
        for key, value in self.email.fields.values.items():
            for field_key, field_value in value.__dict__.items():
                if field_key == "email":
                    continue
                self.template_fields[key + "__" + str(field_key)] = field_value

    def _substitute_fields(self, text):
        template = Template(text)
        return template.substitute(self.template_fields)
