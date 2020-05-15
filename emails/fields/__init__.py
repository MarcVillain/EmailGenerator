from abc import ABC
from string import Template


class Field(ABC):
    """
    Field object.
    """
    def __init__(self, email):
        """
        Initialize necessary variables.
        :param email: Parent Email field.
        """
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
        """
        Substitute field's attributes in template.
        Fields are represented by ${NAME} or ${NAME__ATTRIBUTE}.
        :param text: Template string.
        :return: Resulting string after substitution.
        """
        template = Template(text)
        return template.substitute(self.template_fields)
