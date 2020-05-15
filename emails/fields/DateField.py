from datetime import datetime

from emails.fields import Field
from helpers.DatesHelper import DatesHelper


class DateField(Field):
    def __init__(self, email):
        super().__init__(email)

        date_from = datetime.strptime("1/1/2020 01:00 AM", "%d/%m/%Y %I:%M %p")
        date_to = datetime.strptime("31/12/2020 11:00 PM", "%d/%m/%Y %I:%M %p")
        self.date = DatesHelper.random_between(date_from, date_to).astimezone()

    def __str__(self):
        return str(self.date.strftime("%a, %d %b %Y %H:%M:%S %z"))
