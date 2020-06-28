import logging
import random
import uuid

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
            "SENDER", None if random.randint(1, 20) == 1 else from_field
        )
        self.fields.add("TO")
        self.fields.add("DATE")
        self.fields.add("MESSAGE_ID")
        self.fields.add("MESSAGE")
        self.fields.add("SUBJECT")
        self.fields.add("CONTENT_TYPE")
        self.fields.add("PRE_MESSAGE", "")
        self.fields.add("POST_MESSAGE", "")

    def add_attachment(self, filename):
        """
        Add an attachment.
        :param filename: The name of the attachment file.
        """
        if not hasattr(self, "attachment_boundary"):
            self.attachment_boundary = str(uuid.uuid4())

        old_content_type = self.get_field("CONTENT_TYPE").type
        self.get_field(
            "CONTENT_TYPE"
        ).type = f'multipart/mixed; boundary="{self.attachment_boundary}"'

        fileid = str(uuid.uuid4())
        attachment_message = (
            f'Content-Type: text/plain; charset="iso-8859-1"; name="{filename}"\n'
            + f'Content-Disposition: attachment; filename="{filename}"\n'
            + "Content-Transfer-Encoding: base64\n"
            + f"X-Attachment-Id: {fileid}\n"
        )

        if str(self.get_field("PRE_MESSAGE")) == "":
            self.fields.update(
                "PRE_MESSAGE",
                f"--{self.attachment_boundary}\nContent-type: {old_content_type}\n",
            )
        if str(self.get_field("POST_MESSAGE")) == "":
            self.fields.update(
                "POST_MESSAGE", f"--{self.attachment_boundary}--\n"
            )

        old_post_message = self.get_field("POST_MESSAGE")
        new_post_message = f"--{self.attachment_boundary}\n{attachment_message}\n{old_post_message}"
        self.fields.update("POST_MESSAGE", new_post_message)
