"""
gaunit.models

This module implements main classes used by gaunit: :class:`TrackingPlan, 
:class:`TestCase` and :class:`Result`. 
"""
from __future__ import annotations

import logging
import pprint
from typing import List, Tuple
from urllib.parse import unquote

from colorama import Fore, init
from gspread import Spreadsheet

from gaunit.utils import open_json, remove_empty_values

from .utils import (
    get_ga_requests_from_browser_perf_log,
    get_ga_requests_from_har,
    get_py_version,
    load_dict_xor_json,
    parse_ga_request,
    parse_ga_url,
)

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)
# TODO remove that


class TrackingPlan(object):
    def __init__(self, test_cases=None):
        # Default empty dicts/lists for dict/lists params.
        test_cases = {} if test_cases is None else test_cases

        self.test_cases = test_cases

    def get_expected_events(self, test_case_id: str) -> list:
        """get expected events for a given test case

        Args:
            test_case_id (str):  test case id
        """
        try:
            d = self.test_cases.get(test_case_id, None)
            if d:
                # URL decode events params from tracking plan. Numbers must be converted to string
                events = []
                for event in d["events"]:
                    events.append({k: unquote(str(v)) for (k, v) in event.items()})
                return events
            else:
                raise Exception(
                    "no test case '%s' found in tracking plan" % test_case_id
                )
        except KeyError:
            raise KeyError(
                "tracking plan is not valid (see Documentation) '%s'" % test_case_id
            )

    @classmethod
    def from_json(cls, path: str) -> TrackingPlan:
        # TODO docstring
        d = open_json(path)
        tp = TrackingPlan(test_cases=d.get("test_cases", None))
        return tp

    @classmethod
    def from_spreadsheet(cls, sheet: Spreadsheet) -> TrackingPlan:
        # TODO docstring
        worksheets = sheet.worksheets()
        tp = {}
        for w in worksheets:
            events = w.get_all_records()
            events = [remove_empty_values(e) for e in events]
            tp.update({w.title: {"events": events}})
        return TrackingPlan(test_cases=tp)

    @classmethod
    def from_csv(cls, path: str) -> TrackingPlan:
        # TODO
        pass

    @classmethod
    def from_array(cls, array: List[list]) -> TrackingPlan:
        # First column has the name of the test_case
        # each row corresponds to an event
        # [[["test_case","dp","v"],["home_engie","home","1"],...]]
        # TODO
        pass

    def update_test_case(self, id: str, expected_events: List[dict]):
        # TODO docstring
        # events : list of dict
        # [{"v:1", "'dp":"home"},{],..}

        d = {id: {"events": expected_events}}
        self.test_cases.update(d)


class TestCase(object):
    """User-defined class object representing a test case.

    Used to get results between runned test case and expected tracking plan.

    Note:
        one and one only argument must be given: ``har`` or ``har_path``

    Example :
        >>> events = [{"t":"pageview","dt":"home"},...]
        tc = TestCase("my_test_case", expected_events=events)
        >>> r = tc.check_har(har=har)  # or tc.check_har(har_path=path) for a HAR file
        >>> r.checklist_expected_events
        [True, True]
        >>> r.was_sucessful()
        True

    Attributes:
        id (str): test case id (same id used to match with tracking plan)
        expected_events (list) : list of Google Analytics event in tracking plan.
            Each event is represented by a dict of params.
            Example: ``[{"t":"pageview","dt":"home"},...]``.
            This parameter prevails over ``tracking_plan`` parameter.
            Defaults to None.
        tracking_plan (TrackingPlan): tracking plan containing expected events for this
            test case. Defaults to None
        har (dict): actual har for this test case in dict format. Defaults to None
        har_path (str) : path to HAR file for this test case (standard HAR JSON).
            Defaults to None.
        perf_log (list) : browser performance log

        actual_events (list) : list of GA events params parsed from HAR or http log
            Each event is represented by a dict of params (same as `expected_events`).
            Example: ``[{"t":"pageview","dt":"home"},...]``
            note that TestCase.check() will compare ``expected_events`` and
            ``actual_events``, which makes sense!
    """

    def __init__(
        self,
        id: str,
        expected_events: list = None,
        tracking_plan: TrackingPlan = None,
        har: dict = None,
        har_path: str = None,
        perf_log: list = None,
    ):
        # Default empty dicts/lists for dict/lists params.
        expected_events = [] if expected_events is None else expected_events
        har = {} if har is None else har
        perf_log = [] if perf_log is None else perf_log

        self.id = id  # test case name

        if expected_events:
            self.expected_events = expected_events
        elif tracking_plan:
            self.expected_events = tracking_plan.get_expected_events(self.id)
        self.actual_events = []

        self.har = {}  # for debug, will be killed soon
        # self.page_flow = [] # will store urls from pages TODO
        # self.page_flow_ids = [] # will store har ids for pages
        if har or har_path:
            self.load_har(har, har_path)

        if perf_log:
            self.load_perf_log(perf_log)

    def load_har(self, har=None, har_path=None):
        """extracts and stores analytics hits from a har

        updates attributes `actual_events` (wip: page_flow).
        Takes one and one only argument : dict or path to a json file

        Args:
            har (dict, optional): [description]. Defaults to None.
            har_path (str, optional): [description]. Defaults to None.

        Raises:
            ValueError: if zero or two arguments are given.
        """

        har = load_dict_xor_json(har, har_path)
        # extract GA events
        requests = get_ga_requests_from_har(har)
        events = []
        for r in requests:
            events.extend(parse_ga_request(r))

        self.har = har  # TDO remove attribute
        self.actual_events = events

        # # extract pages (urls and har ids)
        # page_flow = get_pages_from_har(har)
        # page_flow_ids = get_pages_ids_from_har(har)

    def load_perf_log(self, perf_log: list):
        """extracts and stores analytics events from Performance Log

        For more info on Performance Log, see https://chromedriver.chromium.org/logging/performance-log

        Args:
            perf_log (list): log entries from ``driver.get_log("performance")``

        See also :
            :func:`TestCase.load_har`
        """
        # TODO GA4 check that there are no POST methods, otherwise throw an error or warning
        urls = get_ga_requests_from_browser_perf_log(perf_log)
        events = [parse_ga_url(url) for url in urls]

        self.actual_events = events

    def check(self, ordered=True) -> Tuple[list, list]:
        # TODO make private?
        """compares hits from tracking plan and from log and returns 2 checklists

        Args:
            ordered (bool, optional): True if we want hits to respect tracking plan
                order (default behavior)

        Raises:
            Exception: if something's missing (tracking plan, test case log entries or
                analytics events)

        Returns:
            Tuple[list, list]: 2 checklists:
                First checklist tells which event in tracking plan is missing
                Second checklist tells which analytics event from test case corresponds
                to an expected event
        """

        # check if everything needed is defined
        message = "tried to check tracking but something is missing: %s"
        missing = []
        if not self.expected_events:
            missing.append("tracking plan")
        if missing:
            raise Exception(message % ", ".join(missing))
        if not self.actual_events:
            raise Exception("no actual analytics event found in log")

        # start checking
        expected = self.expected_events
        actual = self.actual_events
        chklst_expected = []
        chklst_actual = [False] * len(actual)
        pos = 0  # position of last checked hit
        for t in expected:
            check = False
            for index, hit in enumerate(actual[pos:]):
                if t.items() <= hit.items():
                    # expected event is present : all params are there
                    check = True
                    chklst_actual[pos + index] = True
                    if ordered:
                        pos += index  # if we want hits to respect tracking plan order (default)
                    break
                # expected event is not here
            chklst_expected.append(check)

        return chklst_expected, chklst_actual

    def result(self):
        """performs tracking checks and return a Result class object"""

        expected, actual = self.check()
        r = Result(self, expected, actual)
        return r


class Result(object):
    """Created by a TestCase object. Stores results from a check

    Attributes:
        test_case (TestCase): test case these results are coming from
    """

    def __init__(
        self, test_case: TestCase, checklist_expected: list, checklist_actual: list
    ):
        self.test_case = test_case  # entire TestCase object  # TODO replace by content
        self.checklist_expected = (
            checklist_expected  # TODO rename to checklist_expected _events
        )
        self.checklist_actual = checklist_actual  # TODO same
        # self.comparison = None

    # TODO method to return merged results : comparison of both tracker and hits list

    # TODO was_sucessful()

    def get_status_expected_events(self) -> list:
        """Returns expected event and their status

        Returns:
            list: list of expected events and their status (``True`` if found in actual events))

        Example:
            >>> r = gaunit.check_har("my_test_case", "tracking_plan.json", har=har)
            >>> r.get_status_expected_events()
            [{'event':{'t':'pageview', 'dp': 'home'}, 'found': True},..]
        """

        tc = self.test_case
        events = tc.expected_events
        chcklst = self.checklist_expected

        return [{"event": h, "found": c} for (h, c) in zip(events, chcklst)]

    def get_status_actual_events(self) -> list:
        """Returns actual events and which ones were expected in tracking plan

        Returns:
            list: list of actual hits

        Example:
            >>> r = gaunit.check_har("my_test_case", "tracking_plan.json", har=har)
            >>> r.get_status_actual_events()
            [{'event:{'t':'pageview', 'dp': 'home'}, 'expected': True}
        """

        tc = self.test_case
        events = tc.actual_events
        chcklst = self.checklist_actual

        return [{"event": h, "expected": c} for (h, c) in zip(events, chcklst)]

    def print_result(self, display_ok=False):
        self._print_expected_events(all=display_ok)
        self._print_summary()

    def _print_expected_events(self, all=False):
        """pretty print list of events from tracking plan

        says which tracker was found in test case  ("OK" or "missing"), used in CLI

        Args:
            all (bool, optional): if False, print only missing events if True, print all.
                Defaults to False.
        """
        expected = self.test_case.expected_events
        chcklst = self.checklist_expected
        init(autoreset=True)  # colorama

        print("events in tracking plan: %s" % len(expected))
        args = (
            {"sort_dicts": False} if get_py_version() >= (3, 8) else {}
        )  # preserve dict params order when printing (only for Python>=3.8)
        for (event, check) in zip(expected, chcklst):
            if not check:
                print(80 * "=")
                pprint.pprint(event, **args)  # pylint: disable=E1123
                print(67 * " ", " ... " + Fore.RED + "missing")
            elif check and all:
                print(80 * "=")
                pprint.pprint(event, **args)  # pylint: disable=E1123
                print(72 * " ", " ... " + Fore.GREEN + "OK")
            else:
                pass

    def _print_summary(self):
        """print a result summary

        Example:
            output:

            | GA events found: total:4 / ok:3 / missing:0
            | ✔ OK: all expected events found

            or

            | GA events found: total:11 / ok:1 / missing:2
            | ❌ FAILED: events missing
            ""

        """
        expected = self.test_case.expected_events
        actual = self.test_case.actual_events
        chcklst = self.checklist_expected
        total_found, expected_found = len(actual), len([c for c in chcklst if c])
        missing = len(expected) - expected_found

        print(80 * "-")
        if total_found == 0:
            print("no GA events found")
        else:
            print(
                "GA events found: total:%s / ok:%s / missing:%s"
                % (total_found, expected_found, missing)
            )
        if False in chcklst:
            print("\N{Cross Mark} FAILED: events missing")
        else:
            print("\N{Heavy Check Mark} OK: all expected events found")

    def print_actual_events(self):
        """pretty print list of analytics hits from test case

        says which analytics hit was in tracking plan ("OK" or "skip"), used in CLI
        """
        tc = self.test_case
        events = tc.actual_events
        chcklst = self.checklist_actual

        init(autoreset=True)  # colorama
        args = (
            {"sort_dicts": False} if get_py_version() >= (3, 8) else {}
        )  # preserve dict params order when printing (only for Python>=3.8)
        for (event, check) in zip(events, chcklst):
            print(80 * "=")
            pprint.pprint(event, **args)  # pylint: disable=E1123
            if check:
                print(72 * " ", " ... " + Fore.GREEN + "OK")
            else:
                print(70 * " ", " ... skip")
