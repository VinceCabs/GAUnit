import unittest
from gaunit.GAUnit import GAUnit

# TODO make it work inside test/ dir
class test_GAUnit(unittest.TestCase):
    def setUp(self):

        self.g = GAUnit(config_file="config.json")

    def test_check_tracking_from_file_ok(self):
        test_case = "home_engie"
        log_file = "tests/home_engie.log"
        checklist = self.g.check_tracking_from_file(
            test_case, log_file, format="log")
        # all hits are here
        self.assertEqual([True, True, True], checklist)

    def test_check_tracking_from_file_hit_missing(self):
        test_case = "home_engie"
        log_file = "tests/home_engie_first_missing.log"
        checklist = self.g.check_tracking_from_file(
            test_case, log_file, format="log")
        # first hit is missing
        self.assertEqual([False, True, True], checklist)


if __name__ == "__main__":
    unittest.main()
