# API-testing-Assurity
Submission for Assurity's API test.

This package runs a series of tests on either a single URL or a batch of URLs to verify whether the API meets the criteria specified by Assurity.

## Criteria


- Name = "Carbon credits"
- CanRelist = true
- The Promotions element with ``Name = "Gallery"`` has a ``Description`` that contains the text ``"Good position in category"``



# Installation
This guide assumes that you have a working Python 3.9 or greater environment.

See: https://docs.python.org/3.10/using/index.html

Once your python environment is setup, pull down this repository.

In command line run the following from the root folder of the repo:

``pip install -r requirements.txt``


# Usage

For Usage options, from the root directory of the repo run:

``python API_Tester.py -h``

```
usage: API_Tester.py [-h] (-u URL | -f FILE) [-l LOGPATH]

Run a series of tests on an API.

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL to be tested
  -f FILE, --file FILE  Path to a .txt file containing a list of URLs to be tested. Note: URLs must each be on a new line.
  -l LOGPATH, --logpath LOGPATH
                        Path to folder for log files. Defaults to ./logs
```