import logging
import random

from emails import Email
from emails.fields.ContactField import ContactField
from emails.fields.DateField import DateField
from emails.fields.IdField import IdField
from emails.fields.MessageField import MessageField
from emails.fields.SubjectField import SubjectField


class BaseEmail(Email):
    """
    Base email with minimum required fields.

    Fields: FROM, SENDER, TO, DATE, MESSAGE_ID, MESSAGE, SUBJECT
    """

    def __init__(self, template="base", fields_values=None, **kwargs):
        """
        Generate base email upon class instantiation.
        :param template: Name of the template to use.
        :param fields_values: (Optional) Name and value fields preset.
        """
        super().__init__(
            template=template, fields_values=fields_values, **kwargs
        )

        # Be careful when changing these, order matters
        from_field = ContactField
        self.fields.add("FROM", from_field)

        sender_field = (
            ContactField if random.randint(1, 20) == 1 else from_field
        )
        self.fields.add("SENDER", sender_field)

        self.fields.add("TO", ContactField)
        self.fields.add("DATE", DateField)
        self.fields.add("MESSAGE_ID", IdField)
        self.fields.add("MESSAGE", MessageField)
        self.fields.add("SUBJECT", SubjectField)
