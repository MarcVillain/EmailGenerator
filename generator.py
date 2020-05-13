import logging
import os
import re
from string import Template

from emails.BaseEmail import BaseEmail

logger = logging.getLogger()


class Generator:
    def __init__(self, output):
        self.output = output

    def generate(self):
        email = BaseEmail()

        pattern_whitespaces = re.compile(r"\s+")
        output_filename = (
            re.sub(pattern_whitespaces, "_", email.get_field("SUBJECT")) + ".eml"
        )
        output_path = os.path.join(self.output, output_filename)

        logger.debug("Write output file")
        with open(output_path, "w") as output_file:
            output_file.write(str(email))
