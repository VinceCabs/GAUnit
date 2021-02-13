class GAUnitException(Exception):
    """There was an exception while running GAUnit"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TrackingPlanError(GAUnitException):
    """TrackingPlan is invalid"""


class DictXORJsonPathError(GAUnitException):
    """One and only one argument must be provided: dict or JSON path"""


class TestCaseCheckError(GAUnitException):
    """Something is missing in Test Case to make a proper check"""
