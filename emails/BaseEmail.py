from emails import Email
from emails.fields.ContactField import ContactField
from emails.fields.DateField import DateField
from emails.fields.IdField import IdField
from emails.fields.MessageField import MessageField
from emails.fields.SubjectField import SubjectField


class BaseEmail(Email):
    def __init__(self):
        super().__init__("base")

        self.fields.add("FROM", ContactField)
        self.fields.add("SENDER", ContactField)
        self.fields.add("TO", ContactField)
        self.fields.add("SUBJECT", SubjectField)
        self.fields.add("DATE", DateField)
        self.fields.add("MESSAGE_ID", IdField)
        self.fields.add("MESSAGE", MessageField)
