import uuid
from datetime import datetime

from emails.fields import Field


class IdField(Field):
    def __init__(self, fields):
        super().__init__(fields)

        self.id = uuid.uuid4()

    def __str__(self):
        return f'"{self.id}"'
