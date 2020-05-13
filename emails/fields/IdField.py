import uuid
from datetime import datetime

from emails.fields import Field


class IdField(Field):
    def __init__(self, email):
        super().__init__(email)

        self.id = uuid.uuid4()

    def __str__(self):
        return f'"{self.id}"'
