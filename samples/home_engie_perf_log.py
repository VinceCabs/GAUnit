import json
import time
from os.path import abspath, dirname, join

import gaunit
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def run():

    capabilities = DesiredCapabilities.CHROME
    # capabilities["loggingPrefs"] = {"performance": "ALL"}  # chromedriver < ~75
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # chromedriver 75+
    driver = webdriver.Chrome(desired_capabilities=capabilities)

    driver.get("https://particuliers.engie.fr")
    driver.find_element_by_id(
        "engie_fournisseur_d_electricite_et_de_gaz_naturel_headerhp_souscrire_a_une_offre_d_energie"
    ).click()  # clic on "souscrire" button
    time.sleep(4)

    # Get Performance Log
    log = driver.get_log("performance")

    # with open("perf_log.json", "w", encoding="utf8") as f:
    #     json.dump(log,f,indent=2)

    # with open("perf_log.json",encoding="utf8") as f:
    #     log=json.load(f)

    # check hits against tracking plan and print results
    tracking_plan = join(abspath(dirname(__file__)), "tracking_plan.json")
    r = gaunit.check_perf_log("home_engie", tracking_plan, log=log)

    print(
        "tracking checklist:", r.checklist_expected
    )  # [True, True, True] tracking is correct !
    # # r.pprint_actual_events(url=True)

    driver.quit()


if __name__ == "__main__":
    run()
