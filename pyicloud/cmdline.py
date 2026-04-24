#! /usr/bin/env python
"""
A Command Line Wrapper to allow easy use of pyicloud for
command line scripts, and related.
"""
import argparse
import pickle
import sys

from click import confirm

from pyicloud import PyiCloudService
from pyicloud.exceptions import PyiCloudFailedLoginException
from . import utils

DEVICE_ERROR = "Please use the --device switch to indicate which device to use."


def create_pickled_data(idevice, filename):
    """
    This helper will output the idevice to a pickled file named
    after the passed filename.

    This allows the data to be used without resorting to screen / pipe
    scrapping.
    """
    pass


def main(args=None):
    """Main commandline entrypoint."""
    pass


if __name__ == "__main__":
    main()
