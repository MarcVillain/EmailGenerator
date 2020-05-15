import argparse
import logging
import os
import re
import shutil
from string import Template
import sys

from generator import Generator

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger_formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
)
logger_console_stream = logging.StreamHandler(sys.stdout)
logger_console_stream.setFormatter(logger_formatter)
logger_console_stream.setLevel(logging.INFO)
logger.addHandler(logger_console_stream)


def ask_yes_no(message):
    """
    Ask a yes/no question, default being no.
    :param message: The message to display.
    :return: True if input is case insensitive "y" or "yes" else False.
    """
    print(message, "[y/N]", end="")
    choice = input().lower()
    return choice in ["y", "yes"]


def create_dir(path):
    """
    Create a directory. If it already exists, ask for override.
    :param path: Path of the directory to create.
    :return: True if created else False.
    """
    # Ask for cleanup if necessary
    if os.path.exists(path):
        print(f"Folder '{path}' already exists.")
        if not ask_yes_no("Do you want to replace it?"):
            return False
        shutil.rmtree(path)

    # Create directory
    try:
        os.mkdir(path)
    except OSError as e:
        logger.error(f"Creation of the directory '{path}' failed")
        return False

    return True


def main(args):
    """
    Setup logging and start email generation.
    :param args: Dictionary of command line arguments.
    """
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger_console_stream.setLevel(logging.DEBUG)

    if create_dir(args.output):
        max_num_str = str(args.number)
        max_num_str_len = len(max_num_str)

        generator = Generator(args.output)

        for i in range(0, args.number):
            num_str = str(i + 1).rjust(max_num_str_len)
            logger.info(f"Generate email ({num_str}/{max_num_str})")
            generator.generate()


def cli():
    """
    Handle command line.
    :return: Dictionary of parsed arguments.
    """
    parser = argparse.ArgumentParser()

    # Options
    parser.add_argument(
        "--debug", help="Display debug information.", action="store_true"
    )

    parser.add_argument(
        "-o", "--output", metavar="FOLDER", help="Output folder.", default="output",
    )

    parser.add_argument(
        "-n",
        "--number",
        metavar="COUNT",
        help="Number of emails to generate.",
        type=int,
        default=10,
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = cli()
    main(args)
