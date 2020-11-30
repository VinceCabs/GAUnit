import unittest

import gaunit


class test_utils(unittest.TestCase):

    # tmpfilepath = os.path.join(tempfile.gettempdir(), "tmp-testfile")

    # def setUp(self):

    #     # # Create a temporary directory
    #     # tmpdirname = tempfile.TemporaryDirectory()
    #     # print(tmpdirname.name)

    # def tearDown(self):
    #     # Remove the directory after the test

    def test_get_event_params_from_tp_dict_wrong_format_1(self):

        tp = {"dummy": "dummy"}
        with self.assertRaises(KeyError):
            gaunit.utils.get_event_params_from_tp_dict("home_engie", tp)

    def test_get_event_params_from_tp_dict_wrong_format_2(self):

        tp = {"test_cases": {"home_engie": {"dummy": "dummy"}}}
        with self.assertRaises(KeyError):
            gaunit.utils.get_event_params_from_tp_dict("home_engie", tp)

    def test_get_event_params_from_tp_dict_missing_test_case(self):

        tp = {"test_cases": {"not_my_test_case": {"dummy": "dummy"}}}
        with self.assertRaises(Exception):
            gaunit.utils.get_event_params_from_tp_dict("home_engie", tp)

    def test_get_event_params_from_tp_dict_OK(self):

        tp = {"test_cases": {"home_engie": {"hits": [{"t": "pageview"}]}}}
        hits = gaunit.utils.get_event_params_from_tp_dict("home_engie", tp)
        self.assertEqual([{"t": "pageview"}], hits)

    def test_get_requests_from_har_OK(self):

        har = {"log": {"entries": [{"request": {"url": "https://domain.com"}}]}}
        urls = gaunit.utils.get_requests_from_har(har)
        self.assertEqual(["https://domain.com"], urls)

    def test_load_dict_xor_json_too_many_args(self):

        d = {"dummy": "dummy"}
        json_path = "dummy.json"
        with self.assertRaises(ValueError):
            gaunit.utils.load_dict_xor_json(d, json_path)

    def test_load_dict_xor_json_no_args(self):

        d = None
        json_path = None
        with self.assertRaises(ValueError):
            gaunit.utils.load_dict_xor_json(d, json_path)

    def test_filter_ga_urls(self):

        urls = [
            "https://www.google-analytics.com/collect?v=1..",
            "https://domain.com",
            "https://analytics.google.com/g/collect?v=2...",
        ]
        ga_urls = gaunit.utils.filter_ga_urls(urls)
        self.assertEqual(["https://www.google-analytics.com/collect?v=1.."], ga_urls)

    def test_parse_ga_url(self):

        url = "https://www.google-analytics.com/collect?v=1&t=pageviews&dp=home"
        params = gaunit.utils.parse_ga_url(url)
        self.assertEqual({"v": "1", "t": "pageviews", "dp": "home"}, params)


if __name__ == "__main__":
    unittest.main()
