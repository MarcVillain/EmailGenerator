from fields import Field


class SubjectField(Field):
    def __init__(self, fields):
        self.value = "Test subject"

    def __str__(self):
        return self.value
