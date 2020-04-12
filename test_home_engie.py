import unittest
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
import time
import os
import json
import logging
import pickle
from gaunit.GAChecker import GAChecker
from gaunit.GALogger import GALogger

logging.basicConfig(level=logging.INFO)


class test_engie(unittest.TestCase):
    def setUp(self):

        proxy = "127.0.0.1:8080"

        options = webdriver.ChromeOptions()
        options.add_argument("--proxy-server=%s" % proxy)
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(920, 860)
        self.driver = driver
        self.gc = GAChecker()

        # cleaning files from previous tests
        if os.path.isfile(self.gc.hits_file):
            os.remove(self.gc.hits_file)
        if os.path.isfile(self.gc.pickle_file):
            os.remove(self.gc.pickle_file)

        # TODO : launch GALogger daemon

    def test_engie_home(self):

        # update test_case for GALogger
        test_case = "home_engie"
        self.gc.set_test_case(test_case)

        # browse scenario
        #TODO testing stage acc/preprod/prod/etc. in a test config file ?
        self.driver.get("https://particuliers.engie.fr?env_work=acc")
        time.sleep(2)
        self.driver.find_element_by_id(
            "engie_fournisseur_d_electricite_et_de_gaz_naturel_headerhp_souscrire_a_une_offre_d_energie"
        ).click()  # clic on "souscrire" button
        time.sleep(2)

        # check hits against tracking plan
        checklist = self.gc.check_tracking()
        self.assertNotIn(False, checklist)

    def test_demenagement(self):

        # update test_case for GALogger
        test_case = "demenagement"
        self.gc.set_test_case(test_case)

        # browse scenario
        self.driver.get("https://particuliers.engie.fr/demenagement.html?env_work=acc")
        time.sleep(2)

        # check hits against tracking plan
        checklist = self.gc.check_tracking()
        self.assertNotIn(False, checklist)

    def tearDown(self):
        self.driver.quit()
        self.gc.clear_test_case()
        if os.path.isfile(self.gc.pickle_file):
            os.remove(self.gc.pickle_file)


if __name__ == "__main__":
    unittest.main()
