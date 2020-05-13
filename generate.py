import argparse
import logging
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


def main(args):
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger_console_stream.setLevel(logging.DEBUG)

    # FIXME


def cli():
    parser = argparse.ArgumentParser()

    # Options
    parser.add_argument(
        "--debug", help="Display debug information.", action="store_true"
    )
    parser.add_argument("-o", "--output", metavar="FOLDER", help="Output folder.")

    # Arguments
    parser.add_argument("TEMPLATE", help="EML template file.")

    return parser.parse_args()


if __name__ == "__main__":
    args = cli()
    main(args)
