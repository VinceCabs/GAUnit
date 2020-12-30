from os.path import abspath, dirname, join
from time import sleep

import gaunit
from browsermobproxy import Server
from selenium import webdriver


def run():

    # set up proxy
    server = Server()
    server.start()
    # 'useEcc' is needed to have decent response time with HTTPS
    proxy = server.create_proxy({"useEcc": True})

    # set up Geckodriver/Firefox
    # # uncomment if you want to use Firefox
    # profile = webdriver.FirefoxProfile()
    # profile.set_proxy(proxy.selenium_proxy())
    # driver = webdriver.Firefox(firefox_profile=profile)

    # set up Chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument("--proxy-server=%s" % proxy.proxy)
    # options.add_argument("--headless")
    capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    capabilities["acceptInsecureCerts"] = True
    driver = webdriver.Chrome(chrome_options=options, desired_capabilities=capabilities)

    # start test case
    driver.implicitly_wait(10)
    test_case = "home_engie"
    proxy.new_har(test_case)
    driver.get("https://particuliers.engie.fr")
    sleep(2)
    driver.find_element_by_id(
        "engie_fournisseur_d_electricite_et_de_gaz_naturel_headerhp_souscrire_a_une_offre_d_energie"
    ).click()  # clic on "souscrire" button
    sleep(2)

    # export har and close all
    har = proxy.har
    server.stop()
    driver.quit()

    # check hits against tracking plan and print results
    tracking_plan = join(abspath(dirname(__file__)), "tracking_plan.json")
    r = gaunit.check_har(test_case, tracking_plan, har=har)

    r.print_result(display_ok=True)


if __name__ == "__main__":
    run()
