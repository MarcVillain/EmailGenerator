import random
from textwrap import wrap

import requests

from emails.fields import Field


class MessageField(Field):
    def __init__(self, email):
        super().__init__(email)

        from_field = email.get_field("FROM")

        self.greetings = self._generate_greetings()
        self.body = self._generate_body()
        self.farewells = self._generate_farewells()
        self.signature = "{} {}".format(from_field.first, from_field.last)

    def _generate_greetings(self):
        return random.choice([
            "Bonjour,",
            f"Bonjour {self.email.get_field('TO').first},",
            f"{self.email.get_field('TO').first},",
        ])

    def _generate_body(self):
        # Get content from website
        req = requests.get("http://enneagon.org/phrases")
        content = req.text

        # Filter out what we want
        content_list = content.split("\n")
        generated_text = content_list[44]
        first_paragraph = generated_text.split("  <br>")[0]
        eighty_almighty = "\n".join(wrap(first_paragraph, width=78))

        # Cleanup
        return eighty_almighty.replace("&nbsp;", " ")

    def _generate_farewells(self):
        return random.choice([
            "Cordialement,",
            "Bien cordialement,",
            "Bonne journée,",
            "Bonne soirée,",
            "Bon après-midi,",
            "Chaleureusement,",
            "Sincèrement,",
            "Salutations distinguées,",
            "Merci,",
            "Merci beaucoup,",
            "Merci bien,",
            "A bientôt,",
        ])

    def __str__(self):
        return f"{self.greetings}\n\n{self.body}\n\n{self.farewells}\n\n-- \n{self.signature}"
