import logging
import os
import re
from os import listdir
from string import Template

import unidecode as unidecode

from emails.BaseEmail import BaseEmail
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

    def generate(self):
        """
        Generate an email.
        """
        email = BaseEmail()

        pattern_whitespaces = re.compile(r"\s+")
        clean_subject = unidecode.unidecode(email.get_field("SUBJECT").subject)
        output_filename = re.sub(pattern_whitespaces, "_", clean_subject) + ".eml"
        output_path = os.path.join(self.output, output_filename)

        logger.debug("Write output file")
        with open(output_path, "w") as output_file:
            output_file.write(str(email))
