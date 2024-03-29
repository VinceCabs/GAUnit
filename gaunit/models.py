"""
gaunit.models

This module implements main classes used by gaunit: :class:`TrackingPlan, 
:class:`~gaunit.TestCase` and :class:`~gaunit.Result`. 
"""
from __future__ import annotations

import json
import pprint
from typing import List, Tuple

from colorama import Fore, init
from gspread import Spreadsheet

from .exceptions import TestCaseCheckError, TrackingPlanError
from .utils import (
    format_events,
    get_ga_requests_from_browser_perf_log,
    get_ga_requests_from_har,
    get_py_version,
    load_dict_xor_json,
    open_json,
    parse_ga_request,
    parse_ga_url,
)


class TrackingPlan(object):
    """User-defined class object representing a :class:`~gaunit.TrackingPlan`.

    Used as an input to perform a check or create a :class:`~gaunit.TestCase`.

    Example:
        See Documentation :ref:`getting_started` or :ref:`howtos` for more details.
    """

    def __init__(self):
        self.content = {}

    def get_expected_events(self, test_case_id: str) -> list:
        """Get expected events for a given test case.

        Args:
            test_case_id (str):  test case id

        Raises:
            :exception:`gaunit.TrackingPlanError`: if test case is not found in tracking plan
        """
        try:
            tc = self.content[test_case_id]
        except KeyError:
            raise TrackingPlanError(
                "test case not found in tracking plan: '%s'" % test_case_id
            )
        events = tc["events"]
        return events

    @classmethod
    def from_events(
        cls, test_case_id: str, expected_events: List[dict]
    ) -> TrackingPlan:
        """Creates an instance of :class:`~gaunit.TrackingPlan` from a list of expected events
        (only for one test case)

        Example :
            >>> from gaunit import TrackingPlan
            >>> expected_events = [{"t":"pageview","dt":"home"},...]
            >>> tracking_plan = TrackingPlan.from_events("my_test_case", expected_events)

        Args:
            test_case_id (str): test case id
            expected_events (list[Dict]): expected events for this tests case

        Returns:
            :class:`~gaunit.TrackingPlan` instance
        """
        tp = TrackingPlan()
        tp.add_test_case(test_case_id, expected_events)
        return tp

    @classmethod
    def from_json(cls, path: str) -> TrackingPlan:
        """Creates an instance of :class:`TrackingPlan` from a JSON file

        See Documentation for the JSON file format.

        Example:
            >>> from gaunit import TrackingPlan
            >>> tracking_plan = TrackingPlan.from_json("tracking_plan.json")

        Args:
            path (str): path to JSON file representing the tracking plan

        Raises:
            :exception:`gaunit.TrackingPlanError`: if tracking plan format is not valid

        Returns:
            :class:`~gaunit.TrackingPlan` instance.
        """
        tp = TrackingPlan()
        d = open_json(path)
        try:
            test_cases = d["test_cases"]
            for tc in test_cases:
                events = test_cases[tc]["events"]
                events = format_events(events)
                test_cases[tc]["events"] = events
            tp.content = test_cases
            return tp
        except KeyError:
            # TODO custom Exceptions
            raise TrackingPlanError(
                "Tracking plan is not valid (see Documentation) '%s'" % path
            )

    @classmethod
    def from_spreadsheet(cls, sheet: Spreadsheet) -> TrackingPlan:
        """Creates an instance of :class:`~gaunit.TrackingPlan` from a Google Spreadsheet.

        This method uses gspread to connect to Google Sheets and import test cases and
        expected events. See Documentation for the spreadsheet format.

        Examples:
            >>> import gspread
            >>> from gaunit import TrackingPlan
            >>> gc = gspread.service_account()  # authentication
            >>> sh = gc.open("Example spreadsheet")  # open spreadsheet
            >>> tp = TrackingPlan.from_spreadsheet(sh)  # import tracking plan

        Args:
            sheet (gspread.Spreadsheet): gspread instance of the spreadsheet to import

        Returns:
            :class:`TrackingPlan` instance.
        """
        tp = TrackingPlan()
        worksheets = sheet.worksheets()
        for w in worksheets:
            events = w.get_all_records()
            events = format_events(events)
            tp.add_test_case(w.title, events)
        return tp

    # @classmethod
    # def from_csv(cls, path: str) -> TrackingPlan:
    #     # TODO P1
    #     pass

    # @classmethod
    # def from_array(cls, array: List[list]) -> TrackingPlan:
    #     # First column has the name of the test_case
    #     # each row corresponds to an event
    #     # [[["test_case","dp","v"],["home_engie","home","1"],...]]
    #     # TODO
    #     pass

    def to_json(self, file: str):
        """Exports :class:`~gaunit.TrackingPlan` instance into a JSON file.

        Example:
            >>> from gaunit import TrackingPlan
            >>> expected_events = [{"t":"pageview","dt":"home"},...]
            >>> tracking_plan = gaunit.TrackingPlan.from_events("my_test_case", expected_events)
            >>> tracking_plan.to_json("tracking_plan.json")

        Args:
            file (str): target file
        """

        tracking_plan = {"test_cases": self.content}
        with open(file, "w", encoding="utf8") as f:
            json.dump(tracking_plan, f)

    def add_test_case(self, test_case_id: str, expected_events: List[dict]):
        """Add or update expected events for a given test case.

        Example:

            >>> from gaunit import TrackingPlan
            >>> expected_events = [{"t":"pageview","dt":"home"},...]
            >>> tracking_plan = TrackingPlan()
            >>> tracking_plan.add_test_case("my_test_case", expected_events)


        See also:
            :func:`TrackingPlan.from_events()`

        Args:
            test_case_id (str): id of the test case
            expected_events (List[dict]): list of expected events for the given test case

        Raises:
            TypeError: if format of ``expected_events`` is not valid.
        """
        try:
            expected_events = format_events(expected_events)
            d = {test_case_id: {"events": expected_events}}
            self.content.update(d)
        except AttributeError:
            raise TypeError(
                "Invalid events type: '%s'. Please provide a list of events"
                % expected_events
            )

    def update_test_case(self, test_case_id: str, expected_events: List[dict]):
        """Simple alias for :func:`TrackingPlan.add_test_case()`."""
        self.add_test_case(test_case_id, expected_events)


class TestCase(object):
    """User-defined class object representing a test case.

    Used to get results between runned test case and expected tracking plan.

    Note:
        One and one only argument must be given: ``har`` or ``har_path``

    Example:
        >>> from gaunit import TestCase
        >>> events = [{"t":"pageview","dt":"home"},...]
        >>> tc = TestCase("my_test_case", expected_events=events)
        >>> r = tc.check_har(har=har)  # or tc.check_har(har_path=path) for a HAR file
        >>> r.was_sucessful()
        True

    See also:
        :func:`gaunit.check_har()` is more straight forward to use.

    Attributes:
        id (str): Test case id (same id used to match with tracking plan)
        tracking_plan (:class:`~gaunit.TrackingPlan`): Tracking plan containing expected events for this
            test case. Defaults to None
        har (dict): Actual har for this test case in dict format. Defaults to None
        har_path (str): Path to HAR file for this test case (standard HAR JSON).
            Defaults to None.
        perf_log (list): Browser performance log
        transport_url (str): custom transport URL for server side GTM.
            Defaults to 'https://www.google-analytics.com'
        actual_events (list): List of GA events params parsed from HAR or http log
            Each event is represented by a dict of params (same as `expected_events`).
            Example: ``[{"t":"pageview","dt":"home"},...]``
    """

    def __init__(
        self,
        id: str,
        tracking_plan: TrackingPlan,
        har: dict = None,
        har_path: str = None,
        perf_log: list = None,
        transport_url: str = "https://www.google-analytics.com",
    ):
        # Default empty dicts/lists for dict/lists params.
        har = {} if har is None else har
        perf_log = [] if perf_log is None else perf_log

        self.id = id  # test case name
        self.transport_url = transport_url
        if isinstance(tracking_plan, TrackingPlan):
            self.expected_events = tracking_plan.get_expected_events(self.id)
        else:
            raise TypeError(
                "Invalid tracking plan type: '%s'. Please provide a 'TrackingPlan' instance."
                % tracking_plan
            )
        self.actual_events = []

        self.har = har  # for debug, will be killed soon
        self.perf_log = perf_log
        # self.page_flow = [] # will store urls from pages TODO
        # self.page_flow_ids = [] # will store har ids for pages
        if har or har_path:
            self.load_har(har, har_path)

        if perf_log:
            self.load_perf_log(perf_log)

    def load_har(
        self,
        har: dict = None,
        har_path: str = None,
    ):
        """Extracts and stores analytics events from a har.

        Updates :attr:`actual_events`.
        Takes one and one only argument : dict or path to a json file

        Args:
            har (dict, optional): [description]. Defaults to None.
            har_path (str, optional): [description]. Defaults to None.

        """

        har = load_dict_xor_json(har, har_path)
        # extract GA events
        requests = get_ga_requests_from_har(har, self.transport_url)
        events = []
        for r in requests:
            events.extend(parse_ga_request(r))

        self.har = har  # TDO remove attribute
        self.actual_events = events

        # # extract pages (urls and har ids)
        # page_flow = get_pages_from_har(har)
        # page_flow_ids = get_pages_ids_from_har(har)

    def load_perf_log(self, perf_log: list):
        """Extracts and stores analytics events from Performance Log.

        For more info on Performance Log, see https://chromedriver.chromium.org/logging/performance-log

        Warning:
            Performance logs do not record POST requests (massively used with GA4 and soon, according to
            Google, with gtag.js). This method will be
            deprecated in future versions. We advise you to use :func:`gaunit.check_har` or
            :func:`TestCase.load_har` instead.

        Args:
            perf_log (list): log entries from ``driver.get_log("performance")``

        """
        # TODO GA4 check that there are no POST methods, otherwise throw an error or warning
        urls = get_ga_requests_from_browser_perf_log(perf_log, self.transport_url)
        events = [parse_ga_url(url) for url in urls]

        self.perf_log = perf_log
        self.actual_events = events

    def check(self, ordered=True) -> Tuple[list, list]:
        # TODO make private?
        """Compares events from tracking plan and from log and returns 2 checklists.

        Compares :attr:`expected_events` and :attr:`actual_events`, which makes sense!

        Args:
            ordered (bool, optional): True if we want hits to respect tracking plan
                order (default behavior)

        Raises:
            :exception:`gaunit.TestCaseCheckError`: if no valid HAR or Perf log were provided before check

        Returns:
            Tuple[list, list]: 2 checklists; First checklist tells which event in tracking plan is
            missing. Second checklist tells which analytics event from test case corresponds
            to an expected event.
        """

        # check if everything needed is defined
        if not self.har and not self.perf_log:
            raise TestCaseCheckError(
                "HAR and Perf log are both missing or empty. Please load one before performing a check"
            )

        # start checking
        expected = self.expected_events
        actual = self.actual_events
        chklst_expected = []
        chklst_actual = [False] * len(actual)
        pos = 0  # last checked hit position
        for t in expected:
            check = False
            for index, hit in enumerate(actual[pos:]):
                if t.items() <= hit.items():
                    # expected event found: all params are there
                    check = True
                    chklst_actual[pos + index] = True
                    if ordered:
                        # update last checked hit position to respect tracking plan order (default)
                        pos += index
                    break
                # expected event is not here
            chklst_expected.append(check)

        return chklst_expected, chklst_actual

    def result(self):
        """Performs tracking checks and return a :class:`Result` instance"""

        expected, actual = self.check()
        r = Result(self, expected, actual)
        return r


class Result(object):
    """Let you store, get or print results from a test case in various forms

    Usually, :class:`Result` will be returned by main API methods or :func:`TestCase.result()` .

    See also :
        :func:`gaunit.check_har()`, :func:`TestCase.result()`

    Attributes:
        expected_events (list): Events from tracking plan
        actual_events (list): Events found during test run
        checklist_expected_events (list): Checklist of events from tracking plan which
            are missing (``False`` if missing)
        checklist_actual_events (list): Checklist of events found in log which corresponds
                to an expected event
    """

    def __init__(
        self, test_case: TestCase, checklist_expected: list, checklist_actual: list
    ):
        self.expected_events = test_case.expected_events
        self.actual_events = test_case.actual_events
        self.checklist_expected_events = checklist_expected
        self.checklist_actual_events = checklist_actual
        # self.comparison = None

    # TODO method to return merged results : comparison of both tracker and hits list

    def was_successful(self) -> bool:
        """returns the result of test case

        Returns:
            bool: True if test case was successful
        """
        return all(self.checklist_expected_events)

    def get_status_expected_events(self) -> list:
        """Returns expected event and their status

        Returns:
            list: list of expected events and their status (``True`` if found in actual events))

        Example:
            >>> from gaunit import TestCase
            >>> r = gaunit.check_har("my_test_case", tracking_plan, har=har)
            >>> r.get_status_expected_events()
            [{'event':{'t':'pageview', 'dp': 'home'}, 'found': True},..]
        """

        events = self.expected_events
        chcklst = self.checklist_expected_events

        return [{"event": h, "found": c} for (h, c) in zip(events, chcklst)]

    def get_status_actual_events(self) -> list:
        """Returns actual events and which ones were expected in tracking plan

        Returns:
            list: list of actual hits

        Example:
            >>> from gaunit import TestCase
            >>> r = gaunit.check_har("my_test_case", "tracking_plan.json", har=har)
            >>> r.get_status_actual_events()
            [{'event:{'t':'pageview', 'dp': 'home'}, 'expected': True}
        """

        events = self.actual_events
        chcklst = self.checklist_actual_events

        return [{"event": h, "expected": c} for (h, c) in zip(events, chcklst)]

    def print_result(self, display_ok=False):
        """Pretty print result of a test.

        Two parts: prints the expected events that are missing by defaults or all expected events
        if ``display_ok=True`` then prints a summary.

        Example:
            >>> from gaunit import TestCase
            >>> r = gaunit.check_har("my_test_case", "tracking_plan.json", har=har)
            >>> r.print_result(display_ok=True)
            events in tracking plan: 3
            ================================================================================
            {'t': 'pageview', 'dt': 'Home'}
                                                                                    ... OK
            ================================================================================
            {'t': 'pageview', 'dt': 'Product View'}
                                                                                    ... OK
            ================================================================================
            {'t': 'event',
            'ec': 'ecommerce',
            'ea': 'add_to_cart',
            'ev': '44',
            'pr1nm': 'Compton T-Shirt',
            'pr1pr': '44.00'}
                                                                                    ... OK
            --------------------------------------------------------------------------------
            GA events found: total:9 / ok:3 / missing:0
            ✔ OK: all expected events found

        Args:
            display_ok (bool, optional): if set to ``True``, print all expected events, not only
                missing events. Defaults to ``False``.
        """
        self._print_expected_events(all=display_ok)
        self._print_summary()

    def _print_expected_events(self, all=False):
        """pretty print list of events from tracking plan

        says which tracker was found in test case  ("OK" or "missing"), used in CLI

        Args:
            all (bool, optional): if False, print only missing events if True, print all.
                Defaults to False.
        """
        expected = self.expected_events
        chcklst = self.checklist_expected_events
        init(autoreset=True)  # colorama

        print("events in tracking plan: %s" % len(expected))
        args = (
            {"sort_dicts": False} if get_py_version() >= (3, 8) else {}
        )  # preserve dict params order when printing (only for Python>=3.8)
        for event, check in zip(expected, chcklst):
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
        expected = self.expected_events
        actual = self.actual_events
        chcklst = self.checklist_expected_events
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
            try:
                print("\N{Cross Mark} FAILED: events missing")
            except UnicodeEncodeError:
                print("FAILED: events missing")
        else:
            try:
                print("\N{Heavy Check Mark} OK: all expected events found")
            except UnicodeEncodeError:
                print("OK: all expected events found")

    def print_actual_events(self):
        """pretty print list of analytics hits from test case

        says which analytics hit was in tracking plan ("OK" or "skip"), used in CLI
        """
        events = self.actual_events
        chcklst = self.checklist_actual_events

        init(autoreset=True)  # colorama
        args = (
            {"sort_dicts": False} if get_py_version() >= (3, 8) else {}
        )  # preserve dict params order when printing (only for Python>=3.8)
        for event, check in zip(events, chcklst):
            print(80 * "=")
            pprint.pprint(event, **args)  # pylint: disable=E1123
            if check:
                print(72 * " ", " ... " + Fore.GREEN + "OK")
            else:
                print(70 * " ", " ... skip")
