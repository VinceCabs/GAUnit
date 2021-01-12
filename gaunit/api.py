"""
gaunit.api

This modules makes gaunit nicer to use
"""
from .models import Result, TestCase, TrackingPlan


def check_har(
    test_case_id: str, tracking_plan: TrackingPlan, har=None, har_path=None
) -> Result:
    """Performs checks of a har dict or HAR JSON file against a tracking plan

    Example:
        >>> expected_events = [{"t":"pageview","dt":"home"},...]
        >>> tracking_plan = gaunit.TrackingPlan.from_events("my_test_case", expected_events)
        >>> r = gaunit.check_har("my_test_case", tracking_plan, har=har) # from har dict
        >>> r.was_sucessful()
        True
        >>> r = gaunit.check_har("my_test_case", tracking_plan, har_path="har.json") # from HAR file
        >>> r.was_sucessful()
        True

    See also :
        :func:`gaunit.check_perf_log`

    Args:
        test_case_id (str): test case id (same id used to match with tracking plan)
        tracking_plan (TrackingPlan): tracking plan containing expected events for this
            test case. Defaults to None
        har (dict): actual har for this test case in dict format. Defaults to None
        har_path (str) : path to HAR file for this test case (standard HAR JSON). Defaults to None

    Note:
        one and one only argument must be given: ``har`` or ``har_path``

    Returns:
        :class:`gaunit.Result`: complete results of your test case.
    """
    tc = TestCase(test_case_id, tracking_plan=tracking_plan, har=har, har_path=har_path)
    return tc.result()


def check_perf_log(
    test_case_id: str, tracking_plan: TrackingPlan, perf_log: list
) -> Result:
    """Performs checks of a Performance log against a tracking plan

    For more info on Performance Log and how to get it, see
    https://chromedriver.chromium.org/logging/performance-log

    See also :
        :func:`gaunit.check_har`

    Example:
        >>> perf_log = driver.get_log("performance")  # selenium driver
        >>> r = gaunit.check_perf_log("my_test_case", tracking_plan, perf_log)
        >>> r.checklist_expected_events
        [True, True]
        >>> r.was_sucessful()
        True

    Args:
        test_case_id (str): test case id (same id used to match with tracking plan)
        tracking_plan (TrackingPlan): tracking plan containing expected events for this
            test case. Defaults to None
        perf_log (list): log entries from driver

    Returns:
        :class:`gaunit.Result`: complete results of your test case.
    """
    tc = TestCase(test_case_id, tracking_plan=tracking_plan, perf_log=perf_log)
    return tc.result()
