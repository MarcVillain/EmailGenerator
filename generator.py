import logging
import os
import re
from os import listdir
from string import Template

from emails.BaseEmail import BaseEmail
from helpers.FilesHelper import FilesHelper

logger = logging.getLogger()


class Generator:
    def __init__(self, output):
        self.output = output

        # Pre-load data files
        self.data = dict()
        for file in listdir(FilesHelper.data_dir):
            path = os.path.join(FilesHelper.data_dir, file)
            if os.path.isfile(path):
                FilesHelper.load_list_from_file(file, path)

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
