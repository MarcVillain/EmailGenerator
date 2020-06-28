import logging
import random

from emails.BaseEmail import BaseEmail
from emails.fields.ContactField import ContactField
from emails.fields.DateField import DateField
from emails.fields.IdField import IdField
from emails.fields.MessageField import MessageField
from emails.fields.SubjectField import SubjectField

logger = logging.getLogger()


class ReplyEmail(BaseEmail):
    """
    Reply email with minimum required fields.

    Fields: BaseEmail + REPLY_TO
    """

    def __init__(
        self, prev_email, template="reply", fields_values=None, **kwargs
    ):
        """
        Generate reply email upon class instantiation.
        :param prev_email: Previous Email object.
        :param template: Name of the template to use.
        :param fields_values: (Optional) Name and value fields preset.
        """
        super().__init__(
            template=template, fields_values=fields_values, **kwargs
        )

        if prev_email is None:
            logger.error(
                "Trying to create a ReplyEmail without a previous email"
            )
            return

        self.prev_email = prev_email

        # Be careful when changing these, order matters
        prev_message = "> " + str(prev_email.get_field("MESSAGE")).replace(
            "\n", "\n> "
        )
        self.fields.update("PREV_MESSAGE", prev_message)
