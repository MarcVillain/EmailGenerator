from emails.fields import Field


class SubjectField(Field):
    def __init__(self, fields):
        super().__init__(fields)

        self.value = "Test subject"

    def __str__(self):
        return self.value
