import unittest
from os.path import dirname, join, realpath

import gaunit

from tests.utils import generate_mock_har, generate_mock_perf_log


class test_TrackingPlan(unittest.TestCase):
    def test_from_json_OK(self):
        here = dirname(realpath(__file__))
        path = join(here, "tracking_plan.json")
        tp = gaunit.TrackingPlan.from_json(path)
        self.assertEqual(
            tp.content.get("home_engie", None).get("events", None),
            [{"dp": "A"}, {"dp": "B"}, {"dp": "C"}],
        )

    # TODO with unittest.mock
    # def test_from_json_wrong_format_1(self):
    #     test_cases = {"dummy": "dummy"}
    #     with self.assertRaises(Exception):
    #         gaunit.TrackingPlan(test_cases=test_cases)

    # def test_from_json_wrong_format_2(self):
    #     test_cases = {"home_engie": {"dummy": "dummy"}}
    #     with self.assertRaises(Exception):
    #         gaunit.TrackingPlan(test_cases=test_cases)

    # def test_from_spreadsheet(self):

    def test_add_test_case_create_OK(self):
        events = [{"dp": "A"}]
        tp = gaunit.TrackingPlan()
        tp.add_test_case("home_engie", events)
        self.assertEqual(tp.content, {"home_engie": {"events": events}})

    def test_update_test_case_OK(self):
        # all events are replaced by new events
        events = [{"dp": "A"}]
        tp = gaunit.TrackingPlan()
        tp.add_test_case("home_engie", events)
        tp.add_test_case("home_engie", [{"dp": "X"}])
        self.assertEqual(tp.content, {"home_engie": {"events": [{"dp": "X"}]}})

    def test_get_expected_events_missing_test_case(self):
        events = []
        tp = gaunit.TrackingPlan()
        tp.add_test_case("not_my_test_case", events)
        with self.assertRaises(Exception):
            tp.get_expected_events("home_engie")

    def test_get_expected_events_OK(self):
        events = [{"t": "pageview"}]
        tp = gaunit.TrackingPlan()
        tp.add_test_case("home_engie", events)
        events = tp.get_expected_events("home_engie")
        self.assertEqual([{"t": "pageview"}], events)

    def test_get_expected_events_with_int_OK(self):
        events = [{"ev": 1}]
        tp = gaunit.TrackingPlan()
        tp.add_test_case("home_engie", events)
        events = tp.get_expected_events("home_engie")
        self.assertEqual([{"ev": "1"}], events)

    def test_get_expected_events_with_float_OK(self):
        events = [{"ev": 1.0}]
        tp = gaunit.TrackingPlan()
        tp.add_test_case("home_engie", events)
        events = tp.get_expected_events("home_engie")
        self.assertEqual([{"ev": "1.0"}], events)

    def test_get_expected_events_with_url_decode_OK(self):
        events = [{"dl": "%2F"}]
        tp = gaunit.TrackingPlan()
        tp.add_test_case("home_engie", events)
        events = tp.get_expected_events("home_engie")
        self.assertEqual([{"dl": "/"}], events)


class test_TestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.expected_events = [{"dp": "A"}, {"dp": "B"}, {"dp": "C"}]
        self.tc = gaunit.TestCase("home_engie", expected_events=self.expected_events)

    def test_constructor_with_tracking_plan(self):
        # TestCase should be equal to tc_ref
        tp = gaunit.TrackingPlan()
        tp.update_test_case("home_engie", self.expected_events)
        tc_ref = gaunit.TestCase("home_engie", tracking_plan=tp)
        self.assertEqual(self.expected_events, tc_ref.expected_events)

    def test_load_har_ok(self):
        har = {
            "log": {
                "entries": [
                    {
                        "request": {
                            "method": "GET",
                            "url": "https://www.google-analytics.com/collect?v=1&t=pageview&dp=A",
                        }
                    }
                ]
            }
        }
        self.tc.load_har(har)
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

    def test_check_None(self):
        har = generate_mock_har("x")
        self.tc.load_har(har)
        checklist_expected, checklist_actual = self.tc.check()
        self.assertEqual(checklist_expected, [False, False, False])
        self.assertEqual(checklist_actual, [False])

    def test_check_no_http_log_loaded(self):
        with self.assertRaises(Exception):
            self.tc.check()


class test_Result(unittest.TestCase):
    def setUp(self) -> None:
        expected_events = [{"dp": "A"}, {"dp": "B"}, {"dp": "C"}]
        self.tc = gaunit.TestCase("home_engie", expected_events=expected_events)

    def test_was_successful(self):
        har = generate_mock_har("A", "B", "C")
        self.tc.load_har(har)
        r = self.tc.result()
        self.assertTrue(r.was_successful())

    def test_get_status_expected_events(self):
        har = generate_mock_har("A", "B")
        self.tc.load_har(har)
        r = self.tc.result()
        self.assertEqual(
            r.get_status_expected_events(),
            [
                {"event": {"dp": "A"}, "found": True},
                {"event": {"dp": "B"}, "found": True},
                {"event": {"dp": "C"}, "found": False},
            ],
        )

    def test_get_status_actual_events(self):
        har = generate_mock_har("A", "x")
        self.tc.load_har(har)
        r = self.tc.result()
        self.assertEqual(
            r.get_status_actual_events(),
            [
                {
                    "event": {"v": "1", "dp": "A"},
                    "expected": True,
                },
                {
                    "event": {"v": "1", "dp": "x"},
                    "expected": False,
                },
            ],
        )


if __name__ == "__main__":
    unittest.main()
