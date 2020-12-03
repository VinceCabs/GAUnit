"""
gaunit.api

This modules makes gaunit nicer to use
"""
from gaunit.models import TestCase, Result


def check_har(test_case: str, tracking_plan: str, har=None, har_path=None) -> Result:
    """Performs checks of a har dict or HAR JSON file against a tracking plan

    Example:
        >>> r = gaunit.check_har("my_test_case", "tracking_plan.json", har=har) # from har dict
        >>> r.checklist_expected
        [True, True]
        >>> r = gaunit.check_har("my_test_case", "tracking_plan.json", har_path="har.json") # from HAR file
        >>> r.checklist_expected
        [True, True]

    See also :
        :func:`gaunit.check_perf_log`

    Args:
        test_case (str): test case id (same id used to match with tracking plan)
        tracking_plan (str): path to tracking plan file (see Documentation)
        har (dict): actual har for this test case in dict format. Defaults to None
        har_path (str) : path to HAR file for this test case (standard HAR JSON). Defaults to None

    Note:
        one and one only argument must be given: ``har`` or ``har_path``

    Returns:
        :class:`gaunit.Result`: complete results of your test case.
    """
    tc = TestCase(test_case, tracking_plan, har, har_path)
    return tc.result()


def check_perf_log(test_case: str, tracking_plan: str, perf_log: list) -> Result:
    """Performs checks of a Performance log against a tracking plan

    For more info on Performance Log and how to get it, see
    https://chromedriver.chromium.org/logging/performance-log

    See also :
        :func:`gaunit.check_har`

    Example:
        >>> driver.get_log("performance")  # selenium driver
        >>> r = gaunit.check_perf_log("my_test_case", "tracking_plan.json", perf_log)
        >>> r.checklist_expected
        [True, True]

    Args:
        test_case (str): test case id (same id used to match with tracking plan)
        tracking_plan (str): path to tracking plan file (see Documentation)
        perf_log (list): log entries from driver

    Returns:
        :class:`gaunit.Result`: complete results of your test case.
    """
    tc = TestCase(test_case, tracking_plan, perf_log=perf_log)
    return tc.result()
