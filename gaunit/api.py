from . import models


def check(test_case: str, **kwargs):
    tc = models.TestCase(test_case, **kwargs)
    return tc.result()


def check_har(test_case: str, tracking_plan: str, har=None, har_path=None, **kwargs):
    return check(
        test_case, tracking_plan=tracking_plan, har=har, har_path=har_path, **kwargs
    )
