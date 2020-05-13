import argparse
import logging
import os
import re
import shutil
from string import Template
import sys

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
    print(message, "[y/N]", end="")
    choice = input().lower()
    return choice in ["y", "yes"]


def create_dir(path):
    # Ask for cleanup if necessary
    if os.path.exists(path):
        print(f"Folder {path} already exists.")
        if not ask_yes_no("Do you want to replace it?"):
            return False
        shutil.rmtree(path)

    # Create directory
    try:
        os.mkdir(path)
    except OSError as e:
        logger.error(f"Creation of the directory {path} failed")
        return False

    return True


def generate_email(template, output):
    # Generate email fields
    values = dict()
    values["FROM"] = "Test"
    values["SENDER"] = "Test"
    values["TO"] = "Test"
    values["SUBJECT"] = "Test"
    values["DATE"] = "Test"
    values["MESSAGE_ID"] = "Test"
    values["MESSAGE"] = "Test"

    # Generate output file from template
    content = ""

    with open(template, "r") as input_file:
        logger.debug("Reading template")
        content = Template(input_file.read())
        content = content.substitute(values)

    pattern_whitespaces = re.compile(r"\s+")
    output_filename = re.sub(pattern_whitespaces, "_", values.get("SUBJECT")) + ".eml"
    output_path = os.path.join(output, output_filename)
    with open(output_path, "w") as output_file:
        logger.debug("Writing output")
        output_file.write(content)


def main(args):
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger_console_stream.setLevel(logging.DEBUG)

    if create_dir(args.output):
        max_num_str = str(args.number)
        max_num_str_len = len(max_num_str)
        for i in range(0, args.number):
            num_str = str(i + 1).rjust(max_num_str_len)
            logger.info(f"Generating email ({num_str}/{max_num_str})")
            generate_email(args.template, args.output)


def cli():
    parser = argparse.ArgumentParser()

    # Options
    parser.add_argument(
        "--debug", help="Display debug information.", action="store_true"
    )

    parser.add_argument(
        "-o", "--output", metavar="FOLDER", help="Output folder.", default="emails",
    )

    parser.add_argument(
        "-t",
        "--template",
        metavar="FILE",
        help="EML template file.",
        default="template.eml",
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
