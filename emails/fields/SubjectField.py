import re

import requests

from emails.fields import Field


class SubjectField(Field):
    """
    Subject field.
    """

    def __init__(self, email):
        """
        Generate field content.
        Require fields: MESSAGE
        :param email: Parent Email object.
        """
        super().__init__(email)

    def generate(self):
        """
        Start the field generation process.
        """
        super().generate()

        if not hasattr(self, "subject"):
            self.subject = self._generate_subject()

    def _generate_subject(self):
        """
        Generate subject by extracting the first line
        of the email's message body.
        :return: The generated subject.
        """
        # Filter out first sentence (max length of 40 characters)
        words = re.split(r"(\W+)", self.email.get_field("MESSAGE").body)
        sentence = words[0]
        for word in words[1:]:
            extended_sentence = sentence + word
            if len(extended_sentence) > 40:
                break
            sentence = extended_sentence

        # Cleanup
        return sentence.strip().capitalize()

    def __str__(self):
        """
        String representation of the subject.
        :return: Subject field string representation.
        """
        return self.subject
