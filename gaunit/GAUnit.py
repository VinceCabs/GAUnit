import json
import logging
import re
from logging import log
from urllib.parse import parse_qs, urlparse


class GAUnit:

    # TODO add add unit tests
    # TODO add logging level in config

    def __init__(self, config_file="config.json"):
        cfg = self.__getConfig(config_file)
        self.tracking_file = cfg["tracking_plan_file"]

    def check_tracking_from_har(self, test_case: str, har: dict) -> list:
        """takes har recorded for a given test case and check it against tracking plan

        Args:
            test_case (str): Test case id. e.g. "home_engie"
            har (dict): har generated by test case

        Returns:
            list: checklist of boolean with tracker statuses. eg. [True, False, True]
        """

        urls = self.__get_urls_from_har(har)
        checklist = self.check_tracking_from_urls(test_case, urls)
        return checklist

    def check_tracking_from_urls(self, test_case: str, urls: list) -> list:
        """takes HTTP request URLs for a given test case and check it against tracking plan

        Args:
            test_case (str): Test case id. e.g. "home_engie"
            urls (list): HTTP resquest URLs generated by test case

        Returns:
            list: checklist of boolean with tracker statuses. eg. [True, False, True]
        """

        # only ga_hits (https://google-analytics.com/collect?...)
        urls = self.__filter_ga_hits(urls)

        # extract GA hits parameters from all urls.
        # Output is a list like this one :
        # [{'v':'1','dp'='home',..},{..},..]
        hits = self.__load_hits_from_urls(urls)

        # load tracking plan
        tracking = self.__get_hits_from_tracking_plan(
            self.tracking_file, test_case)

        # check recorded hits against hits in tracking plan
        checklist = self.__check_hits_vs_tracking_hits(
            tracking, hits
        )
        return checklist

    def check_tracking_from_file(
        self, test_case: str, file: str, format="har"
    ) -> list:
        """takes har or HTTP requests log file for a given test case and check it against tracking plan


        Args:
            test_case (str): Test case id. e.g. "home_engie"
            file (str): path to raw hits log file generated by test case (with URLs).
            format (str, optional): file format. `har` or `log` (one full URL per line). Defaults to `har`.
                note: `log` format is one http request per line
        Raises:
            Exception: if file format is not recognized

        Returns:
            list: checklist of boolean with tracker statuses. eg. [True, False, True]
        """

        # load urls list from file
        if format == "log":
            with open(file, encoding='utf8') as f:
                urls = f.readlines()
        elif format == "har":
            with open(file, encoding='utf8') as f:
                har = json.load(f)
                urls = self.__get_urls_from_har(har)
        else:
            raise Exception("File format '%s' is not recognized" % format)

        checklist = self.check_tracking_from_urls(test_case, urls)
        return checklist

    def __check_hits_vs_tracking_hits(
        self, tracking: list, hits: list, ordered=True
    ) -> list:
        chklst = []
        # TODO prevent False everywhere if tracker missing
        # TODO add return : formatted string with results
        # search strategy: if ordered = True, hits have to be in the same order as in tracking plan.
        if ordered:
            pos = 0  # position of last checked hit
            for t in tracking:
                check = False
                for hit in hits[pos:]:
                    if ordered:
                        # if we want hits to respect tracking plan order (default)
                        pos += 1
                    if t.items() <= hit.items():
                        # tracker is present : all params are there
                        check = True
                        break
                    # tracker is not here
                chklst.append(check)
        return chklst

    def __get_urls_from_har(self, har: dict) -> list:
        entries = har["log"]["entries"]
        urls = [e["request"]["url"] for e in entries]
        return urls

    def __load_hits_from_urls(self, urls: list) -> list:
        raw_ga_hits = self.__filter_ga_hits(urls)
        hits = []
        for url in raw_ga_hits:
            hit_fields = self.__parse_ga_url(url)
            hits.append(hit_fields)
        return hits

    def __filter_ga_hits(self, urls: list) -> list:
        raw_ga_hits = []
        for url in urls:
            extract = re.search(
                r"https://www\.google-analytics\.com/(g/|)collect.*", url)
            if extract:
                raw_ga_hits.append(extract.group(0))
        return raw_ga_hits

    def __parse_ga_url(self, url: str) -> dict:
        query = urlparse(url).query
        hit_fields = parse_qs(query)
        hit_fields = {
            f: hit_fields[f][0] for f in hit_fields
        }  # transform {f:[v]} to {f:v}
        return hit_fields

    def __get_hits_from_tracking_plan(self, file_name: str, test_case: str) -> dict:
        hits = {}
        try:
            with open(file_name, "r") as f:
                content = json.load(f)
                hits = content["test_cases"][test_case]["hits"]
                f.close()
        except FileNotFoundError:
            logging.warning("No tracking plan file found:" +
                            self.tracking_file)
        return hits

    def __getConfig(self, file: str) -> dict:
        with open(file) as f:
            config = json.load(f)
        return config

    def convert_file_har2log(self, har_file: str, target: str) -> None:
        """helper function to export GA HTTP requests into a log file 

        Args:
            har_file (str): path to the har file
            target (str): path to the target log file
        """
        with open(har_file, encoding='utf8') as f:
            har = json.load(f)

        urls = self.convert_har2log(har)

        with open(target, "w", encoding='utf8') as f:
            f.write("\n".join(urls))

    def convert_har2log(self, har: dict) -> list:
        """helper function to export GA HTTP requests into a log file 

        Args:
            har_file (dict): har

        Returns:
            list: GA HTTP requests
        """
        urls = self.__get_urls_from_har(har)
        urls = self.__filter_ga_hits(urls)
        return urls
