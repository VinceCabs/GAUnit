""""
Automatic test with proxy

Code sample: an "add to cart" scenario using Selenium and a proxy to automatically test 
tracking on Google online store demo.
"""
import json
from os.path import abspath, dirname, join
from time import sleep

import gaunit
from browsermobproxy import Server
from selenium import webdriver


def run():
    # set up proxy
    server = Server()  # or add path to binary: 'Server(path="browsermob-proxy")'
    server.start()
    # require 'useEcc' for decent response time with HTTPS
    proxy = server.create_proxy({"useEcc": True})

    # set up Geckodriver/Firefox
    # # uncomment if you want to use Firefox
    # profile = webdriver.FirefoxProfile()
    # profile.set_proxy(proxy.selenium_proxy())
    # driver = webdriver.Firefox(firefox_profile=profile)

    # set up Chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument("--proxy-server=%s" % proxy.proxy)
    # options.add_argument("--headless")  # uncomment if you want headless Chrome
    capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    capabilities["acceptInsecureCerts"] = True
    driver = webdriver.Chrome(options=options, desired_capabilities=capabilities)

    # start test case
    driver.implicitly_wait(10)
    test_case = "ga4_add_to_cart"
    # 'captureContent' for POST requests
    proxy.new_har(test_case, options={"captureContent": True})
    driver.get("https://vincecabs.github.io/ga4_with_gtag_js/")
    sleep(2)
    driver.find_element_by_id("add_to_cart").click()
    driver.find_element_by_id("login").click()
    sleep(3)

    # export har and close all
    har = proxy.har
    server.stop()
    driver.quit()

    # uncomment if you need to export the har
    # with open(
    #     join(abspath(dirname(__file__)), test_case) + ".har", "w", encoding="utf8"
    # ) as f:
    #     json.dump(har, f)

    # check hits against tracking plan and print results
    path = join(abspath(dirname(__file__)), "tracking_plan.json")
    tracking_plan = gaunit.TrackingPlan.from_json(path)
    r = gaunit.check_har(test_case, tracking_plan, har=har)

    r.print_result(display_ok=True)


if __name__ == "__main__":
    run()
