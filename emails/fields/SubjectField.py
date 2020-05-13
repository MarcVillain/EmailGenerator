import requests

from emails.fields import Field


class SubjectField(Field):
    def __init__(self, fields):
        super().__init__(fields)

        self.subject = self._generate_subject()

    def _generate_subject(self):
        # Get content from website
        req = requests.get("http://enneagon.org/phrases")
        content = req.text

        # Filter out what we want
        content_list = content.split("\n")
        generated_text = content_list[44]
        sentences = generated_text.split(".")
        first_sentence = sentences[0]
        if len(first_sentence) > 40:
            first_sentence = first_sentence[:40]
            words_without_last = first_sentence.split(" ")[:-1]
            first_sentence = " ".join(words_without_last)

        # Cleanup
        return f"{first_sentence}.".replace("&nbsp;", " ")

    def __str__(self):
        return self.subject
