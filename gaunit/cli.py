import argparse
import logging
from .GAUnit import GAUnit

# to run : gaunit home_engie tests/home_engie.har -t tests/tracking_plan.json


def main():
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
        "-d",
        "--debug",
        help="set log level to DEBUG",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.WARNING,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="set log level to INFO",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
    )
    args = parser.parse_args()

    g = GAUnit(tracking_plan=args.tracking_plan)
    g.set_log_level(args.loglevel)
    checklist = g.check_tracking_from_file(args.test_case, args.har_file)
    print(checklist)


if __name__ == "__main__":
    main()
