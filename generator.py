import logging
import os
import re
import uuid
from os import listdir
from string import Template

import unidecode as unidecode

from emails.BaseEmail import BaseEmail
from emails.ReplyEmail import ReplyEmail
from helpers.FilesHelper import FilesHelper

logger = logging.getLogger()


class Generator:
    def __init__(self, output):
        """
        Initialize the generator and pre-load the data files
        that will be used for email generation.
        :param output: Output folder.
        """
        self.output = output

        # Pre-load data files
        self.data = dict()
        for file in listdir(FilesHelper.data_dir):
            path = os.path.join(FilesHelper.data_dir, file)
            if os.path.isfile(path):
                FilesHelper.load_list_from_file(file, path)

    def _generate_single(self, email_type, fields_values=None, **kwargs):
        """
        Generate an email.
        :param email_type: Email class.
        :param fields_values: (Optional) Name and value fields preset.
        :return: Generated Email object.
        """
        email = email_type(**kwargs)
        email.preset(fields_values)
        email.gen_fields()

        pattern_whitespaces = re.compile(r"[:\s]+")
        clean_subject = unidecode.unidecode(
            email.get_field("SUBJECT").subject
        )
        output_filename = (
            re.sub(pattern_whitespaces, "_", clean_subject) + "_" + str(uuid.uuid4())[:6] + ".eml"
        )
        output_path = os.path.join(self.output, output_filename)

        logger.debug("Write output file")
        with open(output_path, "w") as output_file:
            output_file.write(str(email))

        return email

    def generate(self, amount=1, scenario=None):
        """
        Generate multiple emails.
        :param amount: Number of emails to generate. (1 BasicEmail and n-1 ReplyEmail)
        :param scenario: (Optional) Current scenario to use.
        """
        if amount < 0:
            logger.error("Unable to generate a negative amount of emails")
            return

        if scenario is None:
            scenario = dict()

        # Load settings from scenario
        amount = scenario.get("amount", amount)

        # Remove settings from scenario so that the only things left
        # are the fields values
        scenario.pop("amount", None)

        prev_email = None
        count = 0
        while count < amount:
            # Generate field values
            fields_values = dict()
            for name, value in scenario.items():
                if isinstance(value, list):
                    # This allows for multiple emails field scripting
                    if count < len(value) and value[count] is not None:
                        fields_values[name] = value[count]
                elif count == 0 and value is not None:
                    # No list == list of one element
                    fields_values[name] = value

                # Remove None fields
                if fields_values.get(name) is not None:
                    fields_values[name] = { n:v for n, v in fields_values.get(name).items() if v is not None }
                    # Delete field if empty
                    if not fields_values.get(name):
                        del fields_values[name]

            # Send proper email type depending on count
            email_type = BaseEmail if count == 0 else ReplyEmail
            prev_email = self._generate_single(
                email_type, prev_email=prev_email, fields_values=fields_values
            )
            count += 1
