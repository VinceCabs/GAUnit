import unittest

import gaunit

from tests.utils import generate_mock_har, generate_mock_perf_log


class test_api(unittest.TestCase):
    def setUp(self) -> None:
        self.tp = gaunit.TrackingPlan()
        self.tp.update_test_case("home_engie", [{"dp": "A"}, {"dp": "B"}, {"dp": "C"}])

    def test_check_har(self):
        har = generate_mock_har("A", "B", "C")
        r = gaunit.check_har("home_engie", self.tp, har=har)
        self.assertEqual([True, True, True], r.checklist_expected_events)

    def test_check_perf_log(self):
        perf_log = generate_mock_perf_log("A", "B", "C")
        r = gaunit.check_perf_log("home_engie", self.tp, perf_log)
        self.assertEqual([True, True, True], r.checklist_expected_events)


if __name__ == "__main__":
    unittest.main()
