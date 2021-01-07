"""
gaunit.utils

This module implements general methods used by gaunits.
"""
import json
import re
import sys
from typing import Tuple
from urllib.parse import parse_qs, unquote, urlparse


def open_json(json_path) -> dict:
    """convert JSON file into a dict"""

    with open(json_path, "r", encoding="utf8") as f:
        content = json.load(f)
    return content


def get_ga_requests_from_har(har: dict) -> list:
    """extract HAR requests from GA

    Args:
        har (dict): HAR from a test case

    Returns:
        list: list of requests from har (located in ``har["log"]["entries"]``)
    """
    # TODO change events to dict and add event type : [{"type":"GA4", "params":{} }]
    # get requests
    entries = har["log"]["entries"]
    requests = [e["request"] for e in entries]
    # extracting events from requests to Google Analytics domain only
    ga_requests = []
    for r in requests:
        if is_ga_url(r["url"]):
            ga_requests.append(r)
        pass
    return ga_requests


def parse_ga_request(request: dict) -> list:
    """extract event params from GA requests (POST and GET)

    Args:
        request (dict): a request extracted from har (located in ``har["log"]["entries"]``)

    Returns:
        list: list of GA events parameters
    """
    events = []
    r = request
    params_url = parse_ga_url(r["url"])
    if r["method"] == "GET":
        events = [params_url]
    if r["method"] == "POST":
        try:
            events = parse_postdata_events(r["postData"]["text"])
            # must add url params (shared by all events in postData)
            for e in events:
                e.update(params_url)
        except KeyError:
            # if no postData key, get url params anyway
            events = [params_url]
    return events


def parse_postdata_events(data: str) -> list:
    """extract events params from POST data

    Args:
        data (str): data string contained in GA POST request

    Returns:
        dict: all events found in POST data
    """
    # sample postdata: "en=page_view\r\nen=scroll&epn.percent_scrolled=90"
    # en=scroll
    # en=scroll&epn.percent_scrolled=90
    # ""

    events = []
    # events delimited by :
    for e in data.split("\r\n"):
        params = {}
        # params delimited by :
        for t in e.split("&"):
            if t:
                p, v = t.split("=")
                params.update({p: v})
            pass
        events.append(params)
    return format_events(events)


def get_ga_requests_from_browser_perf_log(log: list) -> list:
    """returns a list of HTTP requests urls found in log

    Args:
        log (list): log entries from ``driver.get_log("performance")``.

    Returns:
        list: list of urls
    """
    urls = []
    for entry in log:
        message = json.loads(entry["message"])["message"]
        if (
            "Network.response" in message["method"]  # not sure it is useful
            or "Network.request" in message["method"]
            or "Network.webSocket" in message["method"]  # same here
        ):
            try:
                url = message["params"]["request"]["url"]
                if is_ga_url(url):
                    urls.append(url)
            except:
                pass
    return urls


def load_dict_xor_json(d: dict, json_path: str) -> dict:
    """load  dict XOR json file

    one and one only argument must be given

    Args:
        d (dict): dict
        json_path (str) : path to HAR file (standard HAR Json)

    Returns:
        dict : d XOR dict with json file content

    Raises:
        ValueError: if zero or two arguments are given
    """
    # both arguments
    if d and json_path:
        raise ValueError(
            "too many arguments (dict and json_path). only one argument must be given"
        )
    # dict load
    elif d:
        return d
    # json load
    elif json_path:
        j = open_json(json_path)
        return j
    # no arguments
    else:
        raise ValueError("arguments given are both empty (dict or JSON file path)")


def parse_ga_url(url: str) -> dict:
    query = urlparse(url).query
    event_params = parse_qs(query)
    event_params = {
        f: event_params[f][0] for f in event_params
    }  # transform {f:[v]} to {f:v}
    return event_params


def is_ga_url(url: str) -> bool:
    # TODO check if rule is enough (no need of v=1 or v=2 params?)
    # TODO return GA event type (GA or GA4)
    r = False
    # GA
    if re.search(r"www\.google-analytics\.com\/(j\/|)collect.*", url):
        r = True
    # GA4
    if re.search(r"www\.google-analytics\.com\/g\/collect.*", url):
        r = True
    return r


def get_py_version() -> Tuple[int, int]:
    _ver = sys.version_info
    return (_ver[0], _ver[1])


def filter_keys(d: dict, key_filter: list) -> dict:
    d = {k: v for (k, v) in d.items() if k in key_filter}
    return d


def remove_empty_values(d: dict) -> dict:
    d = {k: v for (k, v) in d.items() if not v == ""}
    return d


def unquote_values(d: dict) -> dict:
    d = {k: unquote(str(v)) for (k, v) in d.items()}
    return d


def format_events(events: list) -> list:
    events = [unquote_values(e) for e in events]
    events = [remove_empty_values(e) for e in events]
    return events
