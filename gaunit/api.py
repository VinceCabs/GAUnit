"""
gaunit.api

This modules makes gaunit nicer to use
"""
from gaunit.models import TestCase, Result


def check_har(test_case: str, tracking_plan: str, har=None, har_path=None) -> Result:
    """Performs checks of a har dict or HAR JSON file against a tracking plan

    Typical usage:
    # from har dict
    r = gaunit.check_har("my_test_case", "tracking_plan.json", har=har)
    print(r.checklist_trackers)  # [True, True]
    # or from HAR JSON file
    r = gaunit.check_har("my_test_case", "tracking_plan.json", har_path="har.json")
    print(r.checklist_trackers)  # [True, True]

    Args:
        test_case (str): test case id (same id used to match with tracking plan)
        tracking_plan (str): path to tracking plan file (see Documentation)
        har_path (str) : path to HAR file for this test case (standard HAR JSON)

    Note: one and one only argument must be given: `har`or `har_path`

    Returns:
        [type]: [description]
    """
    tc = TestCase(test_case, tracking_plan, har, har_path)
    return tc.result()
