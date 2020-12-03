import unittest
from os import path

import gaunit

from tests.utils import generate_mock_har, generate_mock_perf_log


class test_api(unittest.TestCase):

    here = path.dirname(path.realpath(__file__))
    tracking_plan = path.join(here, "tracking_plan.json")

    def test_check_har(self):

        har = generate_mock_har("A", "B", "C")
        r = gaunit.check_har("home_engie", self.tracking_plan, har=har)
        self.assertEqual([True, True, True], r.checklist_expected)

    def test_check_perf_log(self):

        perf_log = generate_mock_perf_log("A", "B", "C")
        r = gaunit.check_perf_log("home_engie", self.tracking_plan, perf_log)
        self.assertEqual([True, True, True], r.checklist_expected)


if __name__ == "__main__":
    unittest.main()
