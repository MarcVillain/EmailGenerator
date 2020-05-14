import random

from emails import Email
from emails.fields.ContactField import ContactField
from emails.fields.DateField import DateField
from emails.fields.IdField import IdField
from emails.fields.MessageField import MessageField
from emails.fields.SubjectField import SubjectField


class BaseEmail(Email):
    def __init__(self):
        super().__init__("base")

        # Be careful when changing these, order matters
        from_field = ContactField
        self.fields.add("FROM", from_field)

        sender_field = ContactField if random.randint(1, 20) == 1 else from_field
        self.fields.add("SENDER", sender_field)

        self.fields.add("TO", ContactField)
        self.fields.add("DATE", DateField)
        self.fields.add("MESSAGE_ID", IdField)
        self.fields.add("MESSAGE", MessageField)
        self.fields.add("SUBJECT", SubjectField)
