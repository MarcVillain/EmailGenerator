import re

import requests

from emails.fields import Field


class SubjectField(Field):
    def __init__(self, email):
        super().__init__(email)

        self.subject = self._generate_subject()

    def _generate_subject(self):
        # Filter out first sentence (max length of 40 characters)
        words = re.split(r"\W+", self.email.get_field("MESSAGE").body)
        sentence = words[0]
        for word in words[1:]:
            extended_sentence = f"{sentence} {word}"
            if len(extended_sentence) <= 40:
                sentence = extended_sentence

        # Cleanup
        return re.sub("[^a-zA-Z _-]+", "", sentence).capitalize()

    def __str__(self):
        return self.subject
