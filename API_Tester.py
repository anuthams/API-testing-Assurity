"""
Date: 25/9/23
Author: Anutham Suresh
Module for Testing API, and generating log files with test outcomes.

Changelog:
    -Separated functions for setup and batching of tests from the API tests.

TODO:
    - add readme including installation steps.

"""

# Top-level imports

# Builtin packages
import argparse
import logging
import sys
import os
import time
from datetime import datetime

# Third-party packages
from pytz import utc

# In-house packages
import tests


# create a folder named 'logs' in the current directory by default.
DEFAULT_LOGPATH = os.path.join(".", "logs")

# Add a logger for the module
logger = logging.getLogger("API_Test_log")


def get_cmdline_args() -> argparse.Namespace:
    """Parses command line arguments passed to the script and
    returns a Namespace containing commandline args as attributes.
    """

    # Create an argument parser instance and parse arguments from stdin.
    parser = argparse.ArgumentParser(
        description="Run a series of tests on an API.")

    # Add two mutually exclusive arguments, one for single url, one for batch of URLs
    required_args = parser.add_mutually_exclusive_group(required=True)
    required_args.add_argument("-u", "--url", help="URL to be tested")
    required_args.add_argument(
        "-f", "--file",
        help="Path to a .txt file containing a list of URLs to be tested. Note: URLs must each be on a new line.")
    parser.add_argument(
        "-l", "--logpath",
        help="Path to folder for log files. Defaults to ./logs")

    return parser.parse_args()


def create_folder(path: os.PathLike) -> None:
    """Function makes a folder when given a path if it doesn't exist.
    Will notify on stdout if the supplied path already exists.
    Will exit with a message on stdout if the supplied path is invalid.

    Args:
        path (os.PathLike): Path of file or folder to make.
    """

    try:
        os.makedirs(path)
    except FileExistsError:
        print(f'Found {path}')
    except FileNotFoundError as err:
        logger.error(f"Invalid filepath for logs {path}")
        sys.exit(1)


def run_single_test(url: str) -> None:
    """Run tests provided by TestLogger on a single URL.

    Args:
        url (str): URL to be tested.
    """
    tester = tests.Tester(url)
    tester.run_test()


def run_batch_test(filepath: str) -> None:
    """Run tests provided by TestLogger on a group of URLs in a given text file.

    Args:
        filepath (str): filepath of the file to the tested. (Usually in same directory as the script)
    """
    with open(filepath, 'r') as file:
        for url in file.read().split('\n'):
            tester = tests.Tester(url)
            tester.run_test()  # TODO: produce a log at this scope??


def setup_logger(log_file: os.PathLike) -> None:
    """Set up logger
    """

    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(filename=log_file)
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    formatter.converter = time.gmtime  # set timestamps to UTC
    file_handler.setFormatter(formatter)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)


def run() -> None:
    """Get commandline arguments, set up logs and run tests.
    """

    # Get commandline arguments and assign to local variables.
    args = get_cmdline_args()
    url = args.url
    url_file = args.file

    # optional argument, if not provided, defaults to /logs from present directory.
    path = args.logpath

    # default to /logs if no path is provided
    if path is None:
        log_path = DEFAULT_LOGPATH
    else:
        log_path = os.path.join(path)

    create_folder(log_path)  # make the log folder

    # Create the log file, timestamps in UTC
    log_name = datetime.now(utc).strftime("%d-%m-%Y--%H.%M.%S.%f") + ".log"
    log_file = os.path.join(log_path, log_name)

    # If for some reason the log file already exists, then print a message to stdout and exit.
    if os.path.exists(log_file):
        logger.error("Log file already exists. Please remove existing copies.")
        sys.exit(1)

    # Setup the logger to output to appropriate log file & stdout.
    setup_logger(log_file)

    if url is not None:
        run_single_test(url)  # If given a url, run in single mode
    elif url_file is not None:
        run_batch_test(url_file)  # If given a file, run in batch mode
    else:
        # We shouldn't be able to get here.
        raise (Exception("Error running tests."))


if __name__ == "__main__":
    run()
