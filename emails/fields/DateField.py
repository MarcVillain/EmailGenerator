from datetime import datetime

from emails.fields import Field


class DateField(Field):
    def __init__(self, fields):
        super().__init__(fields)

        self.date = datetime.now()

    def __str__(self):
        return str(self.date)
