# TODO: set up logging
# TODO: finish docstrings

import requests
import argparse
import logging
import sys


class TestRunner():
    """Tester that provides functions for automated testing of an API.
    get_URL()
    get_JSON
    run_test()
    """

    def __init__(self, url: str, log:) -> None:
        self.target_url = url
        self.test_logs = None  # TODO: figure out a way to generate logs as tests
        # run
        self.json = self.get_JSON(self.target_url)

    def set_URL(self) -> None:
        """Gets a user-defined URL and returns a string.
        Returns:
            str: URL of the API to be tested.
        """

        # Prompt user for URL from somewhere (cmdline for now) and return it.
        user_input = input("Please enter a URL: ")
        if 'https://' not in user_input:
            raise ValueError("URL is invalid. Please enter a valid URL.")

        self.target_url = user_input

        self.json = None  # reset any existing JSON in the test runner

    def get_JSON(self, url_to_get: str, **kwargs) -> dict:
        """Returns a dictionary object from the JSON content provided in the
        response to a get request from the provided url.
        Raises RequestException if there is no response to the request or 
        JSONDecodeError if there is no JSON content in the reponse.

        Args:
            url_to_get (str): URL to test.

        Returns:
            dict: dictionary of decoded JSON content provided in the response from the URL.
        """
        # do a GET request on the URL
        try:
            response = requests.get(url_to_get, **kwargs)
        except requests.exceptions.RequestException as err:
            print(err)  # TODO: log the error and exit nicely
            sys.exit(1)

        # Then return the JSON as a dict
        try:
            entry_json = response.json()
        except requests.exceptions.JSONDecodeError as err:
            pass  # TODO: log the error and exit nicely
        return entry_json

    def test_name(self) -> None:
        """Tests if the entry has a Name element with the value "Carbon credits".
        Raises AssersionError if the test fails.
        """
        entry_name = self.json.get("Name")
        assert entry_name == "Carbon credits", f"Category Name incorrect, expected Carbon credits, but got {entry_name} instead.\n"

    def test_relistable(self) -> None:
        """Tests if the entry has a CanRelist element at the top level that is True.
        Raises AssertionError if the test fails.
        """
        is_relistable = self.json.get("CanRelist")
        assert is_relistable is True, f"Expected CanRelist to be True but got {is_relistable} instead.\n"

    def test_promo_gallery_desc(self) -> None:
        """Tests if there is a Promotions element with a Name property 'Gallery' which has a  
        Description containing the text 'Good position in category.
        Note that this will ignore any subsequent Gallery elements beyond the first 
        within the Promotions in an entry.
        Raises an AssersionError if the test fails.
        """
        entry_promotions: list[dict] | None = self.json.get("Promotions")
        assert entry_promotions is not None, f"Expected to find a Promotions element but got {entry_promotions} instead.\n"
        gallery: dict | None = None
        for promo in entry_promotions:
            if promo.get("Name") == "Gallery":
                # this will ignore any subsequent Gallery elements within the Promotions in an entry.
                gallery = promo
                break

        assert gallery is not None, f"Expected to find a Promotion with the name Gallery but failed.\n"

        description: str | None = gallery.get("Description")
        assert "Good position in category" in description, f"Expected to find 'Good position in category' in description but got {description}\n"

    def run_test(self) -> None:
        """Runs each test on the API.
        """
        try:
            self.test_name()
            self.test_relistable()
            self.test_promo_gallery_desc()
        except AssertionError as err:
            print(err)
            return  # exit this function
        print("All tests passed!")


def get_cmdline_args() -> argparse.Namespace:
    """Parses command line arguments passed to the script and
    returns a Namespace containing commandline args as attributes.
    """

    # Create an argument parser instance and parse arguments from stdin.
    parser = argparse.ArgumentParser(
        description="Run a series of tests on an API.")

    # Add two mutually exclusive arguments, one for single url, one for batch of URLs
    required_args = parser.add_mutually_exclusive_group(required=True)
    required_args.add_argument("--url", help="URL to be tested")
    required_args.add_argument(
        "--file", "-f",
        help="Path to a .txt file containing a list of URLs to be tested. Note: URLs must each be on a new line.")

    return parser.parse_args()


def run_single_test(url: str) -> None:
    """Run tests provided by TestLogger on a single URL.

    Args:
        url (str): URL to be tested.
    """
    tester = TestRunner(url)
    print(f"Testing {url}")
    tester.run_test()


def run_batch_test(filepath: str) -> None:
    """Run tests provided by TestLogger on a group of URLs in a given text file.

    Args:
        filepath (str): filepath of the file to the tested. (Usually in same directory as the script)
    """
    with open(filepath, 'r') as file:
        for url in file.readlines():
            tester = TestRunner(url)
            print(f"Testing {url}")
            tester.run_test()  # TODO: produce a log at this scope??


def run() -> None:
    """Get commandline arguments and run tests.
    """

    args = get_cmdline_args()
    url = args.url
    url_file = args.file

    if url is not None:
        run_single_test(url)  # If given a url, run in single mode
    elif url_file is not None:
        run_batch_test(url_file)  # If given a file, run in batch mode
    else:
        # We shouldn't be able to get here.
        raise (Exception("Error running tests"))


if __name__ == "__main__":
    run()
