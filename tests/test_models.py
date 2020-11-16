import unittest
from os import path

import gaunit

from tests.utils import generate_mock_har_ga


class test_TestCase(unittest.TestCase):

    here = path.dirname(path.realpath(__file__))
    tracking_plan = path.join(here, "tracking_plan.json")
    tc = gaunit.TestCase("home_engie", tracking_plan)

    def test_load_har_ok(self):

        ga_base_url = "https://www.google-analytics.com/collect"
        har = {
            "log": {
                "entries": [{"request": {"url": ga_base_url + "?v=1&t=pageview&dp=A"}}]
            }
        }
        self.tc.load_har(har)

        self.assertEqual(
            self.tc.ga_urls,
            [ga_base_url + "?v=1&t=pageview&dp=A"],
        )
        self.assertEqual(
            self.tc.ga_hits,
            [
                {
                    "v": "1",
                    "t": "pageview",
                    "dp": "A",
                }
            ],
        )

    def test_check_OK(self):
        har = generate_mock_har_ga("A", "B", "C")
        self.tc.load_har(har)
        checklist_trackers, checklist_hits = self.tc.check()
        self.assertEqual(checklist_trackers, [True, True, True])
        self.assertEqual(checklist_hits, [True, True, True])

    def test_check_missing_1(self):
        """tracking plan is "A", "B", "C" """
        har = generate_mock_har_ga("A", "x", "B", "x")
        self.tc.load_har(har)
        checklist_trackers, checklist_hits = self.tc.check()
        self.assertEqual(checklist_trackers, [True, True, False])
        self.assertEqual(checklist_hits, [True, False, True, False])

    def test_check_missing_2(self):
        har = generate_mock_har_ga("A", "C", "x")
        self.tc.load_har(har)
        checklist_trackers, checklist_hits = self.tc.check()
        self.assertEqual(checklist_trackers, [True, False, True])
        self.assertEqual(checklist_hits, [True, True, False])

    def test_check_OK_not_ordered(self):
        har = generate_mock_har_ga("A", "x", "C", "B")
        self.tc.load_har(har)
        checklist_trackers, checklist_hits = self.tc.check(ordered=False)
        self.assertEqual(checklist_trackers, [True, True, True])
        self.assertEqual(checklist_hits, [True, False, True, True])

    def test_check_missing_not_ordered(self):
        har = generate_mock_har_ga("x", "C", "A")
        self.tc.load_har(har)
        checklist_trackers, checklist_hits = self.tc.check(ordered=False)
        self.assertEqual(checklist_trackers, [True, False, True])
        self.assertEqual(checklist_hits, [False, True, True])


if __name__ == "__main__":
    unittest.main()
