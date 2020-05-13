from datetime import datetime

from fields import Field


class DateField(Field):
    def __init__(self, fields):
        self.date = datetime.now()

    def __str__(self):
        return str(self.date)
