from browsermobproxy import Server
from selenium import webdriver

from gaunit.GAUnit import GAUnit


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
    g = GAUnit(config_file="config.json")

    # start test case
    test_case = "home_engie"
    proxy.new_har(test_case)
    driver.get("https://particuliers.engie.fr?env_work=acc")
    driver.find_element_by_id(
        "engie_fournisseur_d_electricite_et_de_gaz_naturel_headerhp_souscrire_a_une_offre_d_energie"
    ).click()  # clic on "souscrire" button

    # export har
    har = proxy.har
    checklist = g.check_tracking_from_har(test_case, har)
    print(checklist)  # [True, True, True] tracking is correct !

    server.stop()
    driver.quit()


if __name__ == "__main__":
    run()
