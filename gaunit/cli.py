import argparse
import logging
import pprint
from colorama import init, Fore, Style
import json

import gaunit

# to run : gaunit home_engie tests/home_engie.har -t tests/tracking_plan.json


def main():

    check_har()


def check_har():
    parser = argparse.ArgumentParser()
    parser.add_argument("test_case", type=str, help="name of test case")
    parser.add_argument("har_file", type=str, help="path to HAR file")
    parser.add_argument(
        "-t",
        "--tracking_plan",
        type=str,
        help="path to tracking plan",
        default="./tracking_plan.json",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="print all trackers with their status and all hits recorded",
        action="store_false",
        dest="verbose",
    )

    args = parser.parse_args()

    r = gaunit.check_har(args.test_case, args.tracking_plan, har_path=args.har_file)
    r.pprint_trackers()
    # r.pprint_hits()
    print(80 * "=")

    r.pprint_hits()
