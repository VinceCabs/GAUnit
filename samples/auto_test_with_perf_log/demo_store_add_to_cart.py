""""
Automatic test with Perf Logs

Code sample: an "add to cart" scenario using Selenium and Chrome Performance log to 
automatically test tracking on Google online store demo.
Warning : this method will not work with GA4
"""
from os.path import abspath, dirname, join
from time import sleep

import gaunit
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def run():

    # set up webdriver
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # chromedriver 75+
    driver = webdriver.Chrome(desired_capabilities=capabilities)

    # start test case
    driver.implicitly_wait(10)
    driver.get("https://enhancedecommerce.appspot.com/")
    sleep(2)
    driver.find_element_by_id("homepage-9bdd2-1").click()
    sleep(2)
    driver.find_element_by_id("addToCart").click()
    sleep(2)
    # Get Performance Log and close all
    log = driver.get_log("performance")
    driver.quit()

    # # Uncomment if you want to store log in json file
    # with open("perf_log.json", "w", encoding="utf8") as f:
    #     json.dump(log, f, indent=2)

    # # Uncomment if you want to parse existing log file before check
    # with open("perf_log.json", encoding="utf8") as f:
    #     log = json.load(f)

    # check hits against tracking plan and print results
    path = join(abspath(dirname(__file__)), "tracking_plan.json")
    tracking_plan = gaunit.TrackingPlan.from_json(path)
    r = gaunit.check_perf_log("ga_demo_store_add_to_cart", tracking_plan, log)

    r.print_result(display_ok=True)


if __name__ == "__main__":
    run()
