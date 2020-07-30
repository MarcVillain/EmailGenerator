import logging
import random
from textwrap import wrap

import requests

from emails.fields import Field
from helpers.FilesHelper import FilesHelper


logger = logging.getLogger()


class MessageField(Field):
    """
    Message Field.
    """

    def __init__(self, email):
        """
        Generate field content.
        Require fields: FROM
        :param email: Parent Email object.
        """
        super().__init__(email)

    def generate(self):
        """
        Start the field generation process.
        """
        super().generate()

        if not hasattr(self, "greetings"):
            self.greetings = self._generate_greetings()

        if not hasattr(self, "body"):
            self.body = self._generate_body()

        if not hasattr(self, "farewells"):
            self.farewells = self._generate_farewells()

        if not hasattr(self, "signature"):
            from_field = self.email.get_field("FROM")
            self.signature = "{} {}".format(from_field.first, from_field.last)

        if not hasattr(self, "footer"):
            self.footer = None  # Can only be set manually

    def _generate_greetings(self):
        """
        Generate random greetings from 'greetings' data list.
        :return: Random greetings followed by a coma.
        """
        greetings = FilesHelper.content.get("greetings").copy()
        greetings = [
            self._substitute_fields(greeting) for greeting in greetings
        ]

        return random.choice(greetings) + ","

    def _generate_body(self):
        """
        Generate random body by loading it from http://enneagon.org/phrases.
        :return: Randomly generated message body.
        """
        # Get content from website
        req = requests.get("http://enneagon.org/phrases")
        content = req.text

        # Filter out what we want
        content_list = content.split("\n")
        generated_text = content_list[44]
        paragraphs = generated_text.split("  <br> ")
        text = ""
        for i, paragraph in enumerate(paragraphs):
            # Randomize number of paragraphs
            if i % 2 == 1 and random.choice([True, False]):
                break
            # Randomize paragraph size
            paragraph_list = paragraph.split(".")
            sentences_count = random.randint(1, len(paragraph_list))
            paragraph = ". ".join(paragraph_list[:sentences_count]) + "."
            eighty_almighty = "\n".join(wrap(paragraph, width=78))
            if text != "":
                text += "\n\n"
            text += eighty_almighty

        # Cleanup
        return (
            text.replace("&nbsp;", " ")
            .replace(". .", "..")
            .replace(". .", "..")
        )

    def _generate_farewells(self):
        """
        Generate random farewells from 'farewells' data list.
        :return: Random farewells followed by a coma.
        """
        return random.choice(FilesHelper.content.get("farewells")) + ","

    def __str__(self):
        """
        String representation of the message.
        :return: Message field string representation.
        """
        # The footer is a weird case at it is only set manually
        footer = getattr(self, "footer", None)
        footer = "" if footer is None else f"\n\n{self.footer}"

        return f"{self.greetings}\n\n{self.body}\n\n{self.farewells}\n\n-- \n{self.signature}{footer}"
