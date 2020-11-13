import os.path
import logging

from browsermobproxy import Server
from gaunit.GAUnit import GAUnit
from selenium import webdriver


def run():

    # set up proxy
    server = Server()
    server.start()
    proxy = server.create_proxy()

    # set up webdriver
    profile = webdriver.FirefoxProfile()
    profile.set_proxy(proxy.selenium_proxy())
    driver = webdriver.Firefox(firefox_profile=profile)
    driver.implicitly_wait(10)

    # instantiate GAUnit
    tracking_plan_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "tracking_plan.json"
        )
    g = GAUnit(tracking_plan=tracking_plan_path)
    g.set_log_level(logging.INFO)

    # start test case
    test_case = "home_engie"
    proxy.new_har(test_case)
    driver.get("https://particuliers.engie.fr")
    driver.find_element_by_id(
        "engie_fournisseur_d_electricite_et_de_gaz_naturel_headerhp_souscrire_a_une_offre_d_energie"
    ).click()  # clic on "souscrire" button

    # export har
    har = proxy.har
    checklist = g.check_tracking_from_har(test_case, har)
    print("tracking checklist:", checklist)  # [True, True, True] tracking is correct !

    server.stop()
    driver.quit()


if __name__ == "__main__":
    run()
