import json
from typing import Tuple
import logging
import pprint

from colorama import init, Fore

from .utils import (
    filter_ga_urls,
    get_hits_from_tracking_plan,
    get_requests_from_har,
    load_dict_xor_json,
    parse_ga_url,
)


logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)


class TestCase(object):
    """User-defined class object representing a test case

    Used to get results between runned test case and expected tracking plan

    Args:
        id (str): test case id (same id used to match with tracking plan)
        tracking_plan (str): path to tracking plan file (see Documentation)
        har (dict): har for this test case in dict format
        har_path (str) : path to HAR file for this test case (standard HAR JSON)
        http_log (list): list of logged URL for this test case
        http_log_path (str) : HTTP log file for this test case (one line per URL)

    Raises:
        ValueError:

    Returns:
        [type]: [description]
    """

    def __init__(
        self, id: str, tracking_plan=None, har=None, har_path=None, http_log=None
    ):

        # # Default empty dicts/lists for dict/lists params.
        har = {} if har is None else har
        http_log = [] if http_log is None else http_log

        self.id = id  # test case name
        self.tracking_plan = tracking_plan  # path to tracking plan

        self.tracking_hits = {}
        if tracking_plan:
            self.tracking_hits = get_hits_from_tracking_plan(id, tracking_plan)

        self.har = {}  # for debug, will be killed soon

        self.ga_urls = {}
        self.ga_hits = {}
        # self.page_flow = [] # will store urls from pages TODO
        # self.page_flow_ids = [] # will store har ids for pages
        if har or har_path:
            self.load_har(har, har_path)

    def load_har(self, har=None, har_path=None):
        """updates self.har, self.hits, (soon : self.page_flow)

        Args:
            har (dict, optional): [description]. Defaults to None.
            har_path (str, optional): [description]. Defaults to None.

        Returns:


        Raises:
            ValueError: if zero or two arguments are given.
        """

        har = load_dict_xor_json(har, har_path)

        # extract GA hits (urls and params)
        urls = get_requests_from_har(har)
        ga_urls = filter_ga_urls(urls)
        ga_hits = [parse_ga_url(url) for url in ga_urls]

        self.har = har  # TDO remove attribute
        self.ga_urls, self.ga_hits = ga_urls, ga_hits

        # # extract pages (urls and har ids)
        # page_flow = get_pages_from_har(har)
        # page_flow_ids = get_pages_ids_from_har(har)

    def check(self, ordered=True) -> Tuple[list, list]:
        """returns results of checks

        Returns:
            [type]: [description]
        """

        # check if everything needed is defined
        message = "tried to check tracking but something is missing: %s"
        missing = []
        if not self.tracking_hits:
            missing.append("tracking plan")
        if not self.har:
            missing.append("har")
        if missing:
            raise Exception(message % ", ".join(missing))
        if not self.ga_hits:
            raise Exception("no ga hits found in har")

        # start checking
        tracking = self.tracking_hits
        hits = self.ga_hits
        chklst_plan = []
        chklst_hits = [False] * len(hits)
        pos = 0  # position of last checked hit
        for t in tracking:
            check = False
            for index, hit in enumerate(hits[pos:]):
                if t.items() <= hit.items():
                    # tracker is present : all params are there
                    check = True
                    chklst_hits[pos + index] = True
                    if ordered:
                        pos += index  # if we want hits to respect tracking plan order (default)
                    break
                # tracker is not here
            chklst_plan.append(check)

        return chklst_plan, chklst_hits

    def result(self):
        """performs tracking checks and return result"""

        checklist_trackers, checklist_hits = self.check()
        r = Result(self, checklist_trackers, checklist_hits)
        return r


class Result(object):
    def __init__(
        self, test_case: TestCase, checklist_trackers: list, checklist_hits: list
    ):
        self.test_case = test_case  # classe entière
        self.checklist_trackers = checklist_trackers
        self.checklist_hits = checklist_hits
        # self.comparison = None # to code after: comparison of both tracker and hits list

    # TODO method to return merged results : trackers, hits and pages

    def pprint_trackers(self):
        """pretty print list of trackers from tracking plan and status (present/missing)

        Args:
            url (bool): print url if True, print hit params if False. Default False
        """

        tc = self.test_case
        hits = tc.tracking_hits
        chcklst = self.checklist_trackers

        # print trackers urls
        init(autoreset=True)
        for (hit, check) in zip(hits, chcklst):
            pprint.pprint(hit)
            if check:
                print(70 * "-", Fore.GREEN + "OK")
            else:
                print(70 * "-", Fore.RED + "missing")

    def pprint_hits(self, url=True):
        """pretty print list of trackers from tracking plan and status (present/missing)

        Args:
            url (bool): print url if True, print hit params if False. Default False
        """
        tc = self.test_case
        urls = tc.ga_urls
        hits = tc.ga_hits
        chcklst = self.checklist_hits

        init(autoreset=True)
        for (u, hit, check) in zip(urls, hits, chcklst):
            if url:
                print(u)
            else:
                pprint.pprint(hit)  # TODO filter params
            if check:
                print(70 * "-", Fore.GREEN + "OK")
            else:
                print(70 * "-", "pass")
