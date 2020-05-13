from emails.fields import Field


class ContactField(Field):
    def __init__(self, fields):
        super().__init__(fields)

        self.first = "Barbe"
        self.last = "Rouge"
        self.email = "{}.{}@fic.com".format(self.first.lower(), self.last.lower())

    def __str__(self):
        return f"{self.first} {self.last} <{self.email}>"
