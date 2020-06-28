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

    def generate(self):
        """
        Start the field generation process.
        """
        pass

    def _substitute_fields(self, text):
        """
        Substitute field's attributes in template.
        Fields are represented by ${NAME} or ${NAME__ATTRIBUTE}.
        :param text: Template string.
        :return: Resulting string after substitution.
        """

        template = Template(text)
        return template.substitute(self.email.fields.template_fields)
