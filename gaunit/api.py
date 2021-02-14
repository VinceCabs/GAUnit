"""
gaunit.api

This modules makes gaunit nicer to use
"""
from .models import Result, TestCase, TrackingPlan


def check_har(
    test_case_id: str, tracking_plan: TrackingPlan, har=None, har_path=None
) -> Result:
    """Performs checks of a har dict or HAR JSON file against a :class:`~gaunit.TrackingPlan`.

    Example:
        >>> expected_events = [{"t":"pageview","dt":"home"},...]
        >>> tracking_plan = gaunit.TrackingPlan.from_events("my_test_case", expected_events)
        >>> r = gaunit.check_har("my_test_case", tracking_plan, har=har) # from har dict
        >>> r.was_sucessful()
        True
        >>> r = gaunit.check_har("my_test_case", tracking_plan, har_path="har.json") # from HAR file
        >>> r.was_sucessful()
        True

    Args:
        test_case_id (str): test case id (same id used to match with tracking plan)
        tracking_plan (:class:`~gaunit.TrackingPlan`): tracking plan containing expected events for this
            test case. Defaults to None
        har (dict): actual har for this test case in dict format. Defaults to None
        har_path (str) : path to HAR file for this test case (standard HAR JSON). Defaults to None

    Note:
        One and one only argument must be given: ``har`` or ``har_path``

    Returns:
        :class:`gaunit.Result`: complete results of your test case.
    """
    tc = TestCase(test_case_id, tracking_plan=tracking_plan, har=har, har_path=har_path)
    return tc.result()


def check_perf_log(
    test_case_id: str, tracking_plan: TrackingPlan, perf_log: list
) -> Result:
    """Performs checks of a Performance log against a :class:`~gaunit.TrackingPlan`.


    Warning:
        Performance logs do not record POST requests (massively used with GA4 and soon, according to
        Google, with gtag.js). This method will be
        deprecated in future versions. We advise you to use :func:`gaunit.check_har` instead

    Example:
        See full example on Github
        `here <https://github.com/VinceCabs/GAUnit/tree/master/examples/auto_test_with_perf_log>`_.

    Args:
        test_case_id (str): test case id (same id used to match with tracking plan)
        tracking_plan (:class:`~gaunit.TrackingPlan`): tracking plan containing expected events for this
            test case. Defaults to None
        perf_log (list): log entries from driver

    Returns:
        :class:`gaunit.Result`: complete results of your test case.
    """
    tc = TestCase(test_case_id, tracking_plan=tracking_plan, perf_log=perf_log)
    return tc.result()
