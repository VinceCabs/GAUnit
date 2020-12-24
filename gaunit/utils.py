"""
gaunit.utils

This module implements general methods used by gaunits.
"""
import json
import re
from urllib.parse import parse_qs, unquote, urlparse


def get_events_from_tracking_plan(test_case: str, tracking_plan: str) -> list:
    """load tracking plan file and extract hits for a given test case

    Args:
        tracking_plan (str): path to tracking plan JSON file (see Documentation for tracking plan expected format)
    """
    tp = open_json(tracking_plan)
    return get_event_params_from_tp_dict(test_case, tp)


def open_json(json_path) -> dict:
    """convert JSON file into a dict"""

    with open(json_path, "r", encoding="utf8") as f:
        content = json.load(f)
    return content


def get_event_params_from_tp_dict(tc: str, tp: dict) -> list:
    """extract GA event params from tracking plan dict"""
    try:
        d = tp["test_cases"].get(tc, None)
        if d:
            # URL decode events params from tracking plan
            events = []
            for event in d["events"]:
                events.append({k: unquote(v) for (k, v) in event.items()})
            return events
        else:
            raise Exception("no test case '%s' found in tracking plan" % tc)
    except KeyError:
        raise KeyError(
            "tracking plan format is not valid (see Documentation). '%s'" % tc
        )


def get_ga_requests_from_har(har: dict) -> list:
    # TODO docstring
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
        data (str): [description]

    Returns:
        dict: [description]
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
    return events


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


def filter_ga_urls(urls: list) -> list:
    """gets a list of urls and returns only GA urls

    Args:
        urls (list): [description]

    Returns:
        list: [description]
    """

    ga_urls = []
    for url in urls:
        extract = re.search(
            r"https://www\.google-analytics\.com\/(j\/|)collect\?v=1.*", url
        )
        if extract:
            ga_urls.append(extract.group(0))
    return ga_urls


def parse_ga_url(url: str) -> dict:
    query = urlparse(url).query
    event_params = parse_qs(query)
    event_params = {
        f: event_params[f][0] for f in event_params
    }  # transform {f:[v]} to {f:v}
    return event_params


def is_ga_url(url: str) -> bool:
    return "www.google-analytics.com" in url


# def get_ga_request_type(request: dict) -> str:
#     """tells what kind of GA event it is

#     Args:
#         urls (list): [description]

#     Returns:
#         str : None, "GA" or "GA4"
#     """
#     # TODO check if rule is enough (no need of v=1 or v=2 params?)
#     ga_type = None
#     url = request["url"]
#     if re.search(
#             r"https://www\.google-analytics\.com\/(j\/|)collect.*", url
#         ):
#         ga_type = "GA"
#     if re.search(
#             r"https://www\.google-analytics\.com\/g\/collect.*", url
#         ):
#         ga_type =  "GA4"
#     return ga_type
