from datetime import datetime

from emails.fields import Field


class DateField(Field):
    def __init__(self, email):
        super().__init__(email)

        self.date = datetime.now()

    def __str__(self):
        return str(self.date)
