#!/usr/bin/env python

import logging
import sys
import os
import argparse


def main(): # pragma: nocover
    desc = "Deterministic data generator."
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("-v", "--verbose", action="store_true", \
        help="Increase output verbosity")
    parser.add_argument("-d", "--debug", action="store_true", \
        help="If true, include python interpreter warnings.")
    parser.add_argument("-p", "--project", default=os.getcwd(), \
        help="The project directory to build (must contain pyproject.toml).")
    parser.add_argument("lifecycle", nargs='?', default="install", \
        help="Supported: clean and build")

    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s::%(levelname)s::%(module)s::%(message)s')

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug('Verbose mode activated.')


if __name__ == '__main__': # pragma: nocover
    main()

