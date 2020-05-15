import os
import pathlib


class FilesHelper:
    """
    All methods and variables to help manipulate files and folders.
    """

    # Base directory
    base_dir = pathlib.Path(__file__).parent.absolute().parent

    # Emails directories
    data_dir = os.path.join(base_dir, "emails", "data")
    templates_dir = os.path.join(base_dir, "emails", "templates")

    # Globally loaded content
    content = dict()

    @classmethod
    def load_list_from_file(cls, name, path):
        """
        Load list from file. Each line is an element of the list.

        The loaded content will be added to the FilesHelper.content
        dictionary.

        :param name: Unique key for loaded content access.
        :param path: Path to the file to load.
        """
        with open(path, "r") as file:
            cls.content[name] = [line.strip() for line in file.readlines()]
