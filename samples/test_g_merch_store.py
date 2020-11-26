from os.path import abspath, dirname, join

from selenium.webdriver.remote.webelement import WebElement

import gaunit
from browsermobproxy import Server
from selenium import webdriver

import json


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
    driver.implicitly_wait(60)

    # start test case
    test_case = "g_merch_store_home"
    proxy.new_har(test_case)
    driver.get("https://shop.googlemerchandisestore.com/")

    # # export har
    har = proxy.har

    # # check hits against tracking plan and print results
    tracking_plan = join(abspath(dirname(__file__)), "tracking_plan.json")
    r = gaunit.check_har(test_case, tracking_plan, har=har)

    with open("har.json", "w", encoding="utf8") as f:
        json.dump(har, f)

    print("tracking checklist:", r.checklist_expected)  # [True]
    r.pprint_actual_events(url=True)

    server.stop()
    driver.quit()


if __name__ == "__main__":
    run()
