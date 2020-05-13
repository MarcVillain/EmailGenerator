from emails.fields import Field


class MessageField(Field):
    def __init__(self, fields):
        super().__init__(fields)

        self.greetings = "Bonjour,"
        self.body = "Ça va?"
        self.farewells = "Cordialement,"
        from_field = fields.get("FROM")
        self.signature = "{} {}".format(from_field.first, from_field.last)

    def __str__(self):
        return f"{self.greetings}\n\n{self.body}\n\n{self.farewells}\n\n-- \n{self.signature}"
