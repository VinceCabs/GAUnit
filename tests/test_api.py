import unittest
from os import path

import gaunit

from tests.utils import generate_mock_har_ga


class test_api(unittest.TestCase):

    here = path.dirname(path.realpath(__file__))
    tracking_plan = path.join(here, "tracking_plan.json")

    def test_check_har(self):

        har = generate_mock_har_ga("A", "B", "C")
        r = gaunit.check_har("home_engie", tracking_plan=self.tracking_plan, har=har)
        self.assertEqual([True, True, True], r.checklist_trackers)
