import logging
import random

from datetime import timedelta

from emails.BaseEmail import BaseEmail
from emails.fields.StringField import StringField

logger = logging.getLogger()


class ReplyEmail(BaseEmail):
    """
    Reply email with minimum required fields.

    Fields: BaseEmail
    """

    def __init__(self, prev_email, template="base", **kwargs):
        """
        Generate reply email upon class instantiation.
        :param prev_email: Previous Email object.
        :param template: Name of the template to use.
        :param fields_values: (Optional) Name and value fields preset.
        """
        if prev_email is None:
            logger.error(
                "Trying to create a ReplyEmail without a previous email"
            )
            return

        super().__init__(template=template, **kwargs)

        self.prev_email = prev_email


    def gen_fields(self):
        """
        Generate fields.
        ! Be careful when changing this, order matters.
        """
        prev_from = self.prev_email.get_field("FROM")
        prev_to = self.prev_email.get_field("TO")
        prev_subject = self.prev_email.get_field("SUBJECT")
        prev_date = self.prev_email.get_field("DATE")
    
        prev_subject.subject = f"Re: {prev_subject.subject}"
        # Add random time to previous answer
        d = random.randint(0, 7)
        h = random.randint(0, 24)
        m = random.randint(1, 60)
        prev_date.date += timedelta(days=d, hours=h, minutes=m)

        self.fields.add("FROM", prev_to)
        self.fields.add("TO", prev_from)
        self.fields.add("SUBJECT", prev_subject)
        self.fields.add("SENDER", prev_to)
        self.fields.add("DATE", prev_date)

        super().gen_fields()

        message = self.get_field("MESSAGE")
        prev_message = "> " + str(self.prev_email.get_field("MESSAGE")).replace(
            "\n", "\n> "
        )
        self.fields.update("MESSAGE", f"{message}\n\n{prev_message}")