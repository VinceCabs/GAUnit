from os.path import abspath, dirname, join

import gaunit
from browsermobproxy import Server
from selenium import webdriver


def run():

    # set up proxy
    server = Server()
    server.start()
    proxy = server.create_proxy()

    # set up webdriver
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.private.browsing.autostart", False)
    profile.set_proxy(proxy.selenium_proxy())
    driver = webdriver.Firefox(firefox_profile=profile)
    driver.implicitly_wait(20)

    # start test case
    test_case = "home_engie"
    proxy.new_har(test_case)
    driver.get("https://particuliers.engie.fr")

    driver.find_element_by_id(
        "engie_fournisseur_d_electricite_et_de_gaz_naturel_headerhp_souscrire_a_une_offre_d_energie"
    ).click()  # clic on "souscrire" button

    # export har
    har = proxy.har

    # check hits against tracking plan and print results
    tracking_plan = join(abspath(dirname(__file__)), "tracking_plan.json")
    r = gaunit.check_har(test_case, tracking_plan, har=har)

    print("tracking checklist:", r.checklist_expected)  # [True, True, True] tracking is correct !
    r.pprint_actual_events(url=True)

    server.stop()
    driver.quit()


if __name__ == "__main__":
    run()
