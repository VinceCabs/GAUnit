import json
import re
from urllib.parse import parse_qs, urlparse


def get_hits_from_tracking_plan(test_case: str, tracking_plan: str) -> dict:
    """load tracking plan file and extract hits for a given test case

    Args:
        tracking_plan (str): path to tracking plan JSON file (see Documentation for tracking plan expected format)
    """
    # 4 test unit
    tp = open_json(tracking_plan)
    return get_hits_from_tp_dict(test_case, tp)


def open_json(json_path) -> dict:
    """convert JSON file into a dict"""

    with open(json_path, "r", encoding="utf8") as f:
        content = json.load(f)
    return content


def get_hits_from_tp_dict(tc: str, tp: dict) -> dict:
    """extract hits from tracking plan dict"""
    try:
        d = tp["test_cases"].get(tc, None)
        if d:
            return d["hits"]
        else:
            raise Exception("no test case '%s' found in tracking plan" % tc)
    except KeyError as e:
        raise KeyError(
            "tracking plan format is not valid (see Documentation). '%s'" % tc
        )


def get_requests_from_har(har: dict) -> list:
    """returns

    Args:
        har (dict): har

    Returns:
        list: [description]
    """
    entries = har["log"]["entries"]
    urls = [e["request"]["url"] for e in entries]
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
        extract = re.search(r"https://www\.google-analytics\.com/(g/|)collect.*", url)
        if extract:
            ga_urls.append(extract.group(0))
    return ga_urls


def parse_ga_url(url: str) -> dict:
    query = urlparse(url).query
    hit_fields = parse_qs(query)
    hit_fields = {f: hit_fields[f][0] for f in hit_fields}  # transform {f:[v]} to {f:v}
    return hit_fields
