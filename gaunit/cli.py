import argparse
import pprint
import sys

from colorama import Fore, Style, init

import gaunit
from gaunit.models import Result
from gaunit.utils import get_py_version

from .__about__ import __version__


def main():
    check_har()


def check_har():
    parser = argparse.ArgumentParser()
    parser.add_argument("har_file", type=str, help="path to HAR file")
    parser.add_argument(
        "test_case",
        type=str,
        help="name of test case if more than one test in tracking plan",
    )
    parser.add_argument(
        "-t",
        "--tracking-plan",
        type=str,
        help="path to tracking plan",
        default="./tracking_plan.json",
    )
    parser.add_argument(
        "-a",
        "--all",
        help="print all expected events (missing and found)",
        action="store_true",
        dest="all",
    )
    parser.add_argument(
        "--version",
        help="print GAUnit version",
        action="version",
        version="GAUnit %s" % __version__,
    )

    args = parser.parse_args()

    # TODO : test_case should be optionnal if tracking plan has only one test_case
    # if args.tracking_plan:
    #  ..
    # else:
    #     if 1 test case in tracking plan
    #         r = gaunit.check_har(args.test_case, args.tracking_plan, har_path=args.har_file)
    #     # N test case
    #     else:
    #     # # error
    #     # print("error: more than one test case in tracking plan, please specify a '--test-case' parameter ")
    #     # pass

    r = gaunit.check_har(args.test_case, args.tracking_plan, har_path=args.har_file)

    r.print_result(display_ok=args.all)
    if False in r.checklist_expected:
        sys.exit(1)  # end with return code 1 if check failed
    # r.print_status_actual_events()
