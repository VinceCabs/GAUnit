import argparse

from colorama import Fore, Style, init

import gaunit

from .__about__ import __version__

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
        help="print all expected events with their status and all actual events recorded",
        action="store_true",
        dest="verbose",
    )
    parser.add_argument(
        "--version",
        help="print GAUnit version",
        action="version",
        version="GAUnit %s" % __version__,
    )

    args = parser.parse_args()

    r = gaunit.check_har(args.test_case, args.tracking_plan, har_path=args.har_file)
    if args.verbose:
        r.pprint_expected_events()
        print(80 * "=")
        r.pprint_actual_events()
    else:
        print(r.checklist_expected)
