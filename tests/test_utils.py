import unittest

import gaunit


class test_utils(unittest.TestCase):
    def test_get_ga_requests_from_har_OK(self):
        har = {
            "log": {
                "entries": [
                    {"request": {"url": "https://domain.com"}},
                    {"request": {"url": "https://www.google-analytics.com/collect"}},
                    {"request": {"url": "https://domain.com"}},
                ]
            }
        }
        requests = gaunit.utils.get_ga_requests_from_har(har)
        self.assertEqual(
            [{"url": "https://www.google-analytics.com/collect"}], requests
        )

    # other test_get_ga_requests_from_har ?

    def test_parse_ga_request_GET(self):
        request = {
            "method": "GET",
            "url": "https://www.google-analytics.com/g/collect?v=1",
        }
        events = gaunit.utils.parse_ga_request(request)
        self.assertEqual([{"v": "1"}], events)

    def test_parse_ga_request_POST(self):
        request = {
            "method": "POST",
            "url": "https://www.google-analytics.com/g/collect?v=2",
            "postData": {"text": "en=page_view\r\nen=scroll"},
        }
        events = gaunit.utils.parse_ga_request(request)
        self.assertEqual(
            [{"v": "2", "en": "page_view"}, {"v": "2", "en": "scroll"}], events
        )

    def test_parse_ga_request_GET_url_encode(self):
        request = {
            "method": "GET",
            "url": "https://www.google-analytics.com/g/collect?dp=%2F",
        }
        events = gaunit.utils.parse_ga_request(request)
        self.assertEqual([{"dp": "/"}], events)

    def test_parse_ga_request_POST_url_encode(self):
        request = {
            "method": "POST",
            "url": "https://www.google-analytics.com/g/collect?v=2",
            "postData": {"text": "en=page_view&dt=%2F"},
        }
        events = gaunit.utils.parse_ga_request(request)
        self.assertEqual([{"v": "2", "en": "page_view", "dt": "/"}], events)

    def test_parse_ga_request_GET_numbers(self):
        request = {
            "method": "GET",
            "url": "https://www.google-analytics.com/g/collect?ev=1&pr1pr=2.0",
        }
        events = gaunit.utils.parse_ga_request(request)
        self.assertEqual([{"ev": "1", "pr1pr": "2.0"}], events)

    def test_parse_ga_request_POST_numbers(self):
        request = {
            "method": "POST",
            "url": "https://www.google-analytics.com/g/collect?v=2",
            "postData": {"text": "ev=1&pr1pr=2.0"},
        }
        events = gaunit.utils.parse_ga_request(request)
        self.assertEqual([{"v": "2", "ev": "1", "pr1pr": "2.0"}], events)

    def test_parse_ga_request_POST_no_postData(self):
        request = {
            "method": "POST",
            "url": "https://www.google-analytics.com/g/collect?v=2",
        }
        events = gaunit.utils.parse_ga_request(request)
        self.assertEqual([{"v": "2"}], events)

    def test_parse_postdata_events_1(self):
        data = "p=v"
        events = gaunit.utils.parse_postdata_events(data)
        self.assertEqual([{"p": "v"}], events)

    def test_parse_postdata_events_2(self):
        data = "p=v\r\np=v"
        events = gaunit.utils.parse_postdata_events(data)
        self.assertEqual([{"p": "v"}, {"p": "v"}], events)

    def test_parse_postdata_events_3(self):
        data = "p=v\r\np=v&pp=vv"
        events = gaunit.utils.parse_postdata_events(data)
        self.assertEqual([{"p": "v"}, {"p": "v", "pp": "vv"}], events)

    def test_parse_postdata_events_empty(self):
        data = ""
        events = gaunit.utils.parse_postdata_events(data)
        self.assertEqual([{}], events)

    def test_get_ga_requests_from_browser_perf_log_OK(self):
        # fmt: off
        perf_log = [
            # log entry we want to get
            {
                "level": "INFO",
                "message": "{\"message\":{\"method\":\"Network.requestWillBeSent\",\"params\":{\"request\":{\"url\":\"https://www.google-analytics.com/collect\"}}}}", 
            },
            # skipped
                        {
                "level": "INFO",
                "message": "{\"message\":{\"method\":\"Network.responseReceived\",\"params\":{}}}", 
            }
        ]
        # fmt: on
        urls = gaunit.utils.get_ga_requests_from_browser_perf_log(perf_log)
        self.assertEqual(["https://www.google-analytics.com/collect"], urls)

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

    # def get_ga_request_type(self):
    #     urls = [
    #         "https://www.google-analytics.com/collect?v=1..",
    #         "https://www.google-analytics.com/j/collect?v=1..",
    #         "https://domain.com",
    #         "https://analytics.google.com/g/collect?v=2...",
    #     ]
    #     ga_urls = gaunit.utils.filter_ga_urls(urls)
    #     self.assertEqual(
    #         [
    #             "https://www.google-analytics.com/collect?v=1..",
    #             "https://www.google-analytics.com/j/collect?v=1..",
    #         ],
    #         ga_urls,
    #     )

    def test_parse_url_params(self):
        url = "https://www.google-analytics.com/collect?v=1&t=pageviews&dp=home"
        params = gaunit.utils.parse_ga_url(url)
        self.assertEqual({"v": "1", "t": "pageviews", "dp": "home"}, params)
        # TODO parse url without params : {}

    def test_is_ga_url(self):
        self.assertTrue(
            gaunit.utils.is_ga_url("https://www.google-analytics.com/collect")
        )


if __name__ == "__main__":
    unittest.main()
