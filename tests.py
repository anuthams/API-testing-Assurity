#TODO: set up tests and logging
#TODO: add module docstring

import requests
import argparse
import logging


class TestRunner():
    """Tester that provides functions for automated testing of an API.
    get_URL
    get_JSON
    run_test()
    """

    def __init__(self, url:str) -> None:
        self.target_url = url
        self.test_logs = None #TODO: figure out a way to generate logs as tests
                              #run
        self.json = self.get_JSON(self.target_url)


    def set_URL(self) -> None:
        """Gets a user-defined URL and returns a string.
        Returns:
            str: URL of the API to be tested.
        """

        #Prompt user for URL from somewhere (cmdline for now) and return it.
        user_input = input("Please enter a URL: ")
        if 'https://' not in user_input:
            raise ValueError("URL is invalid. Please enter a valid URL.")
        
        self.target_url = user_input


    def get_JSON(self, url_to_get:str, **kwargs) -> dict:
        """_summary_

        Args:
            url_to_get (str): _description_

        Returns:
            dict: _description_
        """

        #do a GET request on the URL
        try:
            response = requests.get(url_to_get, **kwargs)
        except requests.exceptions.RequestException as err:
            pass #TODO: log the error and exit nicely
        
        #Then return the JSON as a dict
        try:
            entry_json = response.json()
        except requests.exceptions.JSONDecodeError as err:
            pass #TODO: log the error and exit nicely
        return entry_json

    def show_entry(self) -> None:
        print(type(self.json))
        print(self.json)

    def run_test(self):
        pass


def run():
    #Get url from command line
    url = "https://api.tmsandbox.co.nz/v1/Categories/6327/Details.json?catalogue=false"
    tester = TestRunner(url)
    tester.show_entry()


if __name__ == "__main__":
    run()