import os
import pathlib


class FilesHelper:
    # Base directory
    base_dir = pathlib.Path(__file__).parent.absolute().parent

    # Emails directories
    data_dir = os.path.join(base_dir, "emails", "data")
    templates_dir = os.path.join(base_dir, "emails", "templates")

    # Globally loaded content
    content = dict()

    @classmethod
    def load_list_from_file(cls, name, path):
        with open(path, "r") as file:
            cls.content[name] = [line.strip() for line in file.readlines()]
