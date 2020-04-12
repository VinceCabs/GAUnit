import unittest
import json
import os
from gaunit.GAChecker import GAChecker


class test_GAChecker(unittest.TestCase):

    def setUp(self):
        

        self.gc = GAChecker("tests/ut_config.json")

        if os.path.isfile(self.gc.hits_file):
            os.remove(self.gc.hits_file)
        if os.path.isfile(self.gc.pickle_file):
            os.remove(self.gc.pickle_file)
        if os.path.isfile(self.gc.tracking_file):
            os.remove(self.gc.tracking_file)

        # create tracking plan file for a basic scenario
        tracking_plan = {
            "basic scenario": [
                {"t": "pageview", "dp": "page_name"},
                {"t": "event", "ec": "category", "ea": "action", "el": "label"},
            ],
            "other scenario": [
                {"t": "pageview", "dp": "other_page_name"}
            ]
        }
        with open(self.gc.tracking_file, "w") as f:
            json.dump(tracking_plan, f)
            f.close()
        
        # simulate hits from basic scenario (as would be stored from a GALogger)
        self.gc.set_test_case("basic scenario")
        hits = {"basic scenario": [{"t": "pageview", "dp": "page_name"}, {"t": "event"}]}
        with open(self.gc.hits_file, "w") as f:
            json.dump(hits, f)
            f.close()

    def test_check_tracking(self):

        checklist = self.gc.check_tracking()
        self.assertEqual([True, False], checklist)

    def test_set_test_case(self):
        #TODO
        pass

    def test_clear_test_case(self):
        #TODO
        pass

    def tearDown(self):
        if os.path.isfile(self.gc.hits_file):
            os.remove(self.gc.hits_file)
        if os.path.isfile(self.gc.pickle_file):
            os.remove(self.gc.pickle_file)
        if os.path.isfile(self.gc.tracking_file):
            os.remove(self.gc.tracking_file)


if __name__ == "__main__":
    unittest.main()
