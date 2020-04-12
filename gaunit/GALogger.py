from mitmproxy import http
from mitmproxy import ctx
from urllib.parse import urlparse, parse_qs
import json
import re
import os
import pickle
import logging

class GALogger:
    """this class is an addon to MITM Proxy, used with 'mitmdump' command.

    GALogger acts as a daemon wich intercepts, process and stores GA requests in a specific JSON file.
    This file is then parsed by GALogger to check that the tracking plan is implemented properly for a given scenario
    """

    def __init__(self, config_file="config.json"):

        cfg = self.__getConfig(config_file)
        self.hits_file = cfg["hits_file"]
        self.log_file = cfg["log_file"]
        self.pickle_file = cfg["pickle_file"]

    def request(self, flow: http.HTTPFlow) -> None:
        """implements 'request' method from MITMProxy. Used to intercept GA requests"""
        extract = re.search(
            r"https://www\.google-analytics\.com/collect.*", flow.request.url
        )
        if extract:
            ga_url = extract.group(0)

            self.__ga_request_url_to_file(ga_url)
            self.ga_params_to_JSON(ga_url)

    def __read_test_case(self) -> str:
        """used by this daemon to read current running test case (set by the main running script)"""
        try:
            with open(self.pickle_file, "rb") as f:
                test_case = pickle.load(f)
                f.close()
        except FileNotFoundError:
            ctx.log.warn("No test case defined. File not found: {}".format(self.pickle_file))
        return test_case

    def __ga_request_url_to_file(self, url: str) -> None:
        """stores raw url in a log file. For log and debug only
            
        """
        # TODO :mkdirs if not exist
        with open(self.log_file, "a") as f:
            f.write(url + "\n")

    def ga_params_to_JSON(self, url: str) -> None:
        """get GA hit fields from complete URL and insert them in a JSON hits file
        """

        # load hits file if exists
        if os.path.isfile(self.hits_file):
            try:
                with open(self.hits_file, "r") as f:
                    hits = json.load(f)
                    f.close()
            except json.decoder.JSONDecodeError:
                logging.warning(
                    "File exists but is empty or not proper JSON: " + self.hits_file
                )
        else:
            hits = {}

        # update dict
        test_case = self.__read_test_case()  # get current test_case set by GAChecker
        hit_fields = self.__parse_ga_url(url)
        hits = self.update_hits(hits, hit_fields, test_case)

        # store in JSON
        with open(self.hits_file, "w") as f:
            json.dump(hits, f, indent=3)

    def __parse_ga_url(self, url : str):
        query = urlparse(url).query
        hit_fields = parse_qs(query)
        hit_fields = {
            f: hit_fields[f][0] for f in hit_fields
        }  # transform {f:[v]} to {f:v}
        return hit_fields

    def update_hits(self, hits: dict, hit_fields: dict, test_case: str) -> dict:
        if hits.get(test_case):
            hits[test_case].append(hit_fields)
        else:
            hits[test_case] = [hit_fields]
        return hits

    def __getConfig(self, file: str) -> dict:
        with open(file) as f:
            config = json.load(f)
        return config


addons = [GALogger()]
