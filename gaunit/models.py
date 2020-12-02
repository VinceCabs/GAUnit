"""
gaunit.models

This module implements main classes used by gaunit: :class:`TestCase` and :class:`Result`. 
"""
from typing import Tuple
import logging
import pprint

from colorama import init, Fore

from .utils import (
    filter_ga_urls,
    get_events_from_tracking_plan,
    get_requests_from_browser_perf_log,
    get_requests_from_har,
    load_dict_xor_json,
    parse_ga_url,
)


logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)


class TestCase(object):
    """User-defined class object representing a test case.

    Used to get results between runned test case and expected tracking plan.

    Note:
        one and one only argument must be given: ``har`` or ``har_path``

    Example :
        >>> tc = TestCase("my_test_case", "tracking_plan.json")
        >>> tc.load_har(har=har)
        >>> r = tc.check()
        >>> r.expected_events
        [True, True]

    Attributes:
        id (str): test case id (same id used to match with tracking plan)
        tracking_plan (str): path to tracking plan file (see Documentation)
        har (dict): actual har for this test case in dict format. Defaults to None
        har_path (str) : path to HAR file for this test case (standard HAR JSON). Defaults to None
        perf_log (list) : browser performance log
        expected_events (list) : list of Google Analytics event in tracking plan.
            Each event is represented by a dict of params.
            Example: ``[{"t":"pageview","dt":"home"},...]``
        actual_urls (list) : actual GA events urls found in Test Case (from given HAR or
            http_log)
        actual_events (list) : list of GA events params parsed from `actual_urls`.
            Each event is represented by a dict of params (same as `expected_events`).
            Example: ``[{"t":"pageview","dt":"home"},...]``
            note that TestCase.check() will compare ``expected_events`` and
            ``actual_events``, whick makes sense!
    """

    def __init__(
        self, id: str, tracking_plan=None, har=None, har_path=None, perf_log=None
    ):
        # Default empty dicts/lists for dict/lists params.
        har = {} if har is None else har
        perf_log = [] if perf_log is None else perf_log

        self.id = id  # test case name
        self.tracking_plan = tracking_plan  # path to tracking plan

        self.expected_events = {}
        if tracking_plan:
            self.expected_events = get_events_from_tracking_plan(id, tracking_plan)

        self.har = {}  # for debug, will be killed soon

        self.actual_urls = {}
        self.actual_events = {}
        # self.page_flow = [] # will store urls from pages TODO
        # self.page_flow_ids = [] # will store har ids for pages
        if har or har_path:
            self.load_har(har, har_path)

        if perf_log:
            self.load_perf_log(perf_log)

    def load_har(self, har=None, har_path=None):
        """extracts and stores analytics hits from a har

        updates attributes `ga_urls` and `ga_hits` (soon: page_flow).
        Takes one and one only argument : dict or path to a json file

        Args:
            har (dict, optional): [description]. Defaults to None.
            har_path (str, optional): [description]. Defaults to None.

        Raises:
            ValueError: if zero or two arguments are given.
        """

        har = load_dict_xor_json(har, har_path)

        # extract GA hits (urls and params)
        urls = get_requests_from_har(har)
        urls = filter_ga_urls(urls)
        params = [parse_ga_url(url) for url in urls]

        self.har = har  # TDO remove attribute
        self.actual_urls, self.actual_events = urls, params

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

        urls = get_requests_from_browser_perf_log(perf_log)
        urls = filter_ga_urls(urls)
        params = [parse_ga_url(url) for url in urls]

        self.actual_urls, self.actual_events = urls, params

    def check(self, ordered=True) -> Tuple[list, list]:
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
        if not self.actual_urls:
            missing.append("log")
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
        self.test_case = test_case  # entire TestCase object
        self.checklist_expected = checklist_expected
        self.checklist_actual = checklist_actual
        # self.comparison = None

    # TODO method to return merged results : comparison of both tracker and hits list

    def get_status_expected_events(self) -> list:
        """Returns expected event and their status

        Returns:
            list: list of expected events and their status (``True`` if found in actual events))

        Example:
            >>> r = gaunit.check_har("my_test_case", "tracking_plan.json", har=har)
            >>> r.get_status_expected_events()
            [{'hit':{'t':'pageview', 'dp': 'home'}, 'found': True},..]
        """

        tc = self.test_case
        hits = tc.expected_events
        chcklst = self.checklist_expected

        return [{"hit": h, "found": c} for (h, c) in zip(hits, chcklst)]

    def get_status_actual_events(self, url=True) -> list:
        """Returns actual events and which ones were expected in tracking plan

        Args:
            url (bool): print url if True, print hit params if False. Default: True.

        Returns:
            list: list of actual hits

        Example:
            >>> r = gaunit.check_har("my_test_case", "tracking_plan.json", har=har)
            >>> r.get_status_actual_events()
            [{'url:{'t':'pageview', 'dp': 'home'}, 'expected': True}
            >>> r.get_status_actual_events(url=False)
            [{'url:'https://www.google-analytics.com/collect?v=1&...', 'expected': True}
        """

        tc = self.test_case
        urls = tc.actual_urls
        hits = tc.actual_events
        chcklst = self.checklist_actual

        if url:
            return [{"url": u, "expected": c} for (u, c) in zip(urls, chcklst)]
        else:
            return [{"hit": h, "expected": c} for (h, c) in zip(hits, chcklst)]

    def pprint_expected_events(self):
        """pretty print list of events from tracking plan

        says which tracker was found in test case  ("OK" or "missing")
        """

        tc = self.test_case
        hits = tc.expected_events
        chcklst = self.checklist_expected

        # print expected urls
        init(autoreset=True)
        for (hit, check) in zip(hits, chcklst):
            pprint.pprint(hit)
            if check:
                print(70 * "-", Fore.GREEN + "OK")
            else:
                print(70 * "-", Fore.RED + "missing")

    def pprint_actual_events(self, url=True):
        """pretty print list of analytics hits from test case

        says which analytics hit was in tracking plan ("OK" or "skip")

        Args:
            url (bool): print url if True, print hit params if False. Default: True.
        """
        tc = self.test_case
        urls = tc.actual_urls
        hits = tc.actual_events
        chcklst = self.checklist_actual

        init(autoreset=True)
        for (u, hit, check) in zip(urls, hits, chcklst):
            if url:
                print(u)
            else:
                pprint.pprint(hit)  # TODO filter params
            if check:
                print(70 * "-", Fore.GREEN + "OK")
            else:
                print(70 * "-", "skip")
