import unittest
import json
import os
from gaunit.GALogger import GALogger
from gaunit.GAChecker import GAChecker
import logging


class test_GALogger(unittest.TestCase):
    def setUp(self):

        self.gl = GALogger(config_file="tests/ut_config.json")
        self.gc = GAChecker(config_file="tests/ut_config.json")


    def test_ga_params_to_JSON_from_scratch(self):

        # cleaning
        if os.path.isfile(self.gl.hits_file):
            os.remove(self.gl.hits_file)
        if os.path.isfile(self.gl.pickle_file):
            os.remove(self.gl.pickle_file)

        # ga requests for each scenarios
        ga_urls = [
            "htts://www.google-analytics.com/collect?t=pageview&dp=page_name",
            "htts://www.google-analytics.com/collect?t=event&ec=category",
        ]
        # expected hits (stored from a would be GALogger)
        expected_hits = {
            "basic_scenario": [
                {"t": "pageview", "dp": "page_name"},
                {"t": "event", "ec": "category"},
            ],
            "other_scenario": [
                {"t": "pageview", "dp": "page_name"},
                {"t": "event", "ec": "category"},
            ],
        }
        self.gc.set_test_case("basic_scenario")
        for url in ga_urls:
            self.gl.ga_params_to_JSON(url)

        self.gc.set_test_case("other_scenario")
        for url in ga_urls:
            self.gl.ga_params_to_JSON(url)

        with open(self.gl.hits_file) as f:
            json_hits = json.load(f)
            f.close()

        self.assertDictEqual(json_hits, expected_hits)

    def test_update_hits_add_test(self):

        hits = {"test_1": [{"t": "pageview"}]}
        test_case = "test_2"
        hit_fields = {"t": "pageview"}
        hits = self.gl.update_hits(hits, hit_fields, test_case)
        expected_hits = {"test_1": [{"t": "pageview"}], "test_2": [{"t": "pageview"}]}
        self.assertDictEqual(hits, expected_hits)

    def test_update_hits_add_hit(self):

        hits = {"test_1": [{"t": "pageview"}]}
        test_case = "test_1"
        hit_fields = {"t": "pageview", "dp": "new"}
        hits = self.gl.update_hits(hits, hit_fields, test_case)
        expected_hits = {"test_1": [{"t": "pageview"}, {"t": "pageview", "dp": "new"}]}
        self.assertDictEqual(hits, expected_hits)

    def tearDown(self):
        if os.path.isfile(self.gl.hits_file):
            os.remove(self.gl.hits_file)
        if os.path.isfile(self.gl.pickle_file):
            os.remove(self.gl.pickle_file)


if __name__ == "__main__":
    unittest.main()
