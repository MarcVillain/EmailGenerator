import logging
import os
import re
from string import Template

from fields.ContactField import ContactField
from fields.DateField import DateField
from fields.Fields import Fields
from fields.IdField import IdField
from fields.MessageField import MessageField
from fields.SubjectField import SubjectField

logger = logging.getLogger()


class Generator:
    def __init__(self, template, output):
        self.template = template
        self.output = output

    def generate(self):
        # Generate email fields
        fields = Fields()
        fields.add("FROM", ContactField)
        fields.add("SENDER", ContactField)
        fields.add("TO", ContactField)
        fields.add("SUBJECT", SubjectField)
        fields.add("DATE", DateField)
        fields.add("MESSAGE_ID", IdField)
        fields.add("MESSAGE", MessageField)

        # Generate output file from template
        content = ""

        with open(self.template, "r") as input_file:
            logger.debug("Reading template")
            content = Template(input_file.read())
            content = content.substitute(fields.as_str_dict())

        pattern_whitespaces = re.compile(r"\s+")
        output_filename = (
            re.sub(pattern_whitespaces, "_", str(fields.get("SUBJECT"))) + ".eml"
        )
        output_path = os.path.join(self.output, output_filename)
        with open(output_path, "w") as output_file:
            logger.debug("Writing output")
            output_file.write(content)
