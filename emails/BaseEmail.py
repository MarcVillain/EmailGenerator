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

    def __init__(self, template="base", **kwargs):
        """
        Generate base email upon class instantiation.
        :param template: Name of the template to use.
        :param fields_values: (Optional) Name and value fields preset.
        """
        super().__init__(template=template, **kwargs)

    def gen_fields(self):
        """
        Generate fields.
        ! Be careful when changing this, order matters.
        """
        super().gen_fields()
 
        from_field = self.fields.add("FROM")
        self.fields.add(
            "SENDER",
            None if random.randint(1, 20) == 1 else from_field
        )
        self.fields.add("TO")
        self.fields.add("DATE")
        self.fields.add("MESSAGE_ID")
        self.fields.add("MESSAGE")
        self.fields.add("SUBJECT")
