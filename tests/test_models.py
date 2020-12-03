import unittest
from os import path

import gaunit

from tests.utils import generate_mock_har, generate_mock_perf_log


class test_TestCase(unittest.TestCase):

    here = path.dirname(path.realpath(__file__))
    tracking_plan = path.join(here, "tracking_plan.json")
    tc = gaunit.TestCase("home_engie", tracking_plan)
    ga_base_url = "https://www.google-analytics.com/collect"

    def test_load_har_ok(self):

        har = {
            "log": {
                "entries": [
                    {"request": {"url": self.ga_base_url + "?v=1&t=pageview&dp=A"}}
                ]
            }
        }
        self.tc.load_har(har)

        self.assertEqual(
            self.tc.actual_urls,
            [self.ga_base_url + "?v=1&t=pageview&dp=A"],
        )
        self.assertEqual(
            self.tc.actual_events,
            [
                {
                    "v": "1",
                    "t": "pageview",
                    "dp": "A",
                }
            ],
        )

    def test_load_perf_log_ok(self):
        perf_log = generate_mock_perf_log("B")
        self.tc.load_perf_log(perf_log)

        self.assertEqual(
            self.tc.actual_urls,
            [self.ga_base_url + "?v=1&t=pageview&dp=B"],
        )
        self.assertEqual(
            self.tc.actual_events,
            [
                {
                    "v": "1",
                    "t": "pageview",
                    "dp": "B",
                }
            ],
        )

    def test_check_OK(self):
        har = generate_mock_har("A", "B", "C")
        self.tc.load_har(har)
        checklist_expected, checklist_actual = self.tc.check()
        self.assertEqual(checklist_expected, [True, True, True])
        self.assertEqual(checklist_actual, [True, True, True])

    def test_check_missing_1(self):
        """tracking plan is "A", "B", "C" """
        har = generate_mock_har("A", "x", "B", "x")
        self.tc.load_har(har)
        checklist_expected, checklist_actual = self.tc.check()
        self.assertEqual(checklist_expected, [True, True, False])
        self.assertEqual(checklist_actual, [True, False, True, False])

    def test_check_missing_2(self):
        har = generate_mock_har("A", "C", "x")
        self.tc.load_har(har)
        checklist_expected, checklist_actual = self.tc.check()
        self.assertEqual(checklist_expected, [True, False, True])
        self.assertEqual(checklist_actual, [True, True, False])

    def test_check_OK_not_ordered(self):
        har = generate_mock_har("A", "x", "C", "B")
        self.tc.load_har(har)
        checklist_expected, checklist_actual = self.tc.check(ordered=False)
        self.assertEqual(checklist_expected, [True, True, True])
        self.assertEqual(checklist_actual, [True, False, True, True])

    def test_check_missing_not_ordered(self):
        har = generate_mock_har("x", "C", "A")
        self.tc.load_har(har)
        checklist_expected, checklist_actual = self.tc.check(ordered=False)
        self.assertEqual(checklist_expected, [True, False, True])
        self.assertEqual(checklist_actual, [False, True, True])


class test_Result(unittest.TestCase):

    here = path.dirname(path.realpath(__file__))
    tracking_plan = path.join(here, "tracking_plan.json")
    tc = gaunit.TestCase("home_engie", tracking_plan)

    def test_get_status_expected_events(self):
        har = generate_mock_har("A", "B")
        self.tc.load_har(har)
        r = self.tc.result()
        self.assertEqual(
            r.get_status_expected_events(),
            [
                {"hit": {"dp": "A"}, "found": True},
                {"hit": {"dp": "B"}, "found": True},
                {"hit": {"dp": "C"}, "found": False},
            ],
        )

    def test_get_status_actual_events(self):
        har = generate_mock_har("A", "x")
        self.tc.load_har(har)
        r = self.tc.result()
        self.assertEqual(
            r.get_status_actual_events(url=True),
            [
                {
                    "url": "https://www.google-analytics.com/collect?v=1&dp=A",
                    "expected": True,
                },
                {
                    "url": "https://www.google-analytics.com/collect?v=1&dp=x",
                    "expected": False,
                },
            ],
        )


if __name__ == "__main__":
    unittest.main()
