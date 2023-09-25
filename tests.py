"""
Date: 25/9/23
Author: Anutham Suresh
Module for Testing API, provides the TestRunner class that performs checks that
the given URL matches the specified criteria.

Changelog:
    -Updated README and requirements.txt
    -Removed unneeded imports.

"""

# Top-level imports

# Builtin packages
import logging
import sys

# Third-party packages
import requests

# Add the API_Test_log logger to the module.
logger = logging.getLogger("API_Test_log")


class Tester():
    """Tester class that provides functions for automated testing of an API.
    """

    def __init__(self, url: str) -> None:
        """Intantiates a Tester object with a target url & perfroms a GET 
        request on it and stores the JSON content in the response.

        Args:
            url (str): URL that will be tested.
        """
        self.target_url = url
        # run
        self.json = self.get_JSON(self.target_url)

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
            response = requests.get(url_to_get, timeout=5, **kwargs)
        except requests.exceptions.RequestException as err:
            logger.error(err)  # TODO: log the error and exit nicely
            sys.exit(1)

        #TODO: Would be nice to have more error handling around responses containing
        #status codes.

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
        assert entry_name == "Carbon credits", f"FAILED: Category Name incorrect, expected Carbon credits, but got {entry_name} instead.\n"

    def test_relistable(self) -> None:
        """Tests if the entry has a CanRelist element at the top level that is True.
        Raises AssertionError if the test fails.
        """
        is_relistable = self.json.get("CanRelist")
        assert is_relistable is True, f"FAILED Expected CanRelist to be True but got {is_relistable} instead.\n"

    def test_promo_gallery_desc(self) -> None:
        """Tests if there is a Promotions element with a Name property 'Gallery' which has a  
        Description containing the text 'Good position in category.
        Note that this will ignore any subsequent Gallery elements beyond the first 
        within the Promotions in an entry.
        Raises an AssersionError if the test fails.
        """
        entry_promotions: list[dict] | None = self.json.get("Promotions")
        assert entry_promotions is not None, f"FAILED Expected to find a Promotions element but got {entry_promotions} instead.\n"
        gallery: dict | None = None
        for promo in entry_promotions:
            if promo.get("Name") == "Gallery":
                # this will ignore any subsequent Gallery elements within the Promotions in an entry.
                gallery = promo
                break

        assert gallery is not None, f"FAILED Expected to find a Promotion with the name Gallery but failed.\n"

        description: str | None = gallery.get("Description")
        assert "Good position in category" in description, f"FAILED: Expected to find 'Good position in category' in description but got {description}\n"

    def run_test(self) -> None:
        """Runs each test on the API.
        """
        logger.info(f"Testing {self.target_url}")
        try:
            self.test_name()
            self.test_relistable()
            self.test_promo_gallery_desc()
        except AssertionError as err:
            logger.info(err)
            return  # exit this function
        logger.info("All tests passed")


if __name__ == "__main__":
    print("Please run API_Tester.py instead.")
