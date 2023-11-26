""""
Open a manual test session

Code sample: opens a new browser session and records a har. At the end of the session, 
it checks the har against tracking plan. Tracking plan is the "add to cart" scenario on 
Google online store demo described in GAUnit Documentation: 
https://gaunit.readthedocs.io/en/latest/getting_started.html
"""
import json
from os.path import abspath, dirname, join
from time import sleep
from tkinter import messagebox


import gaunit
from browsermobproxy import Server
from selenium import webdriver


def run():
    # set up proxy
    server = Server()  # or add path to binary: 'Server(path="browsermob-proxy")'
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
    # options.add_argument("--headless")  # uncomment if you want headless Chrome
    capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    capabilities["acceptInsecureCerts"] = True
    driver = webdriver.Chrome(options=options, desired_capabilities=capabilities)

    # start test case
    driver.implicitly_wait(10)
    test_case = "demo_store_add_to_cart"
    # 'captureContent' for POST requests
    proxy.new_har(test_case, options={"captureContent": True})
    driver.get("https://enhancedecommerce.appspot.com/")

    messagebox.showinfo(
        "Manual browsing mode",
        "Recording network trafic. Browse site, then press 'OK' when you're finished",
    )

    # export har and close all
    har = proxy.har
    server.stop()
    driver.quit()

    # uncomment if you need to export the har
    # with open(
    #     join(abspath(dirname(__file__)), test_case) + ".har", "w", encoding="utf8"
    # ) as f:
    #     json.dump(har, f)

    # check events against tracking plan and print results
    path = join(abspath(dirname(__file__)), "tracking_plan.json")
    tracking_plan = gaunit.TrackingPlan.from_json(path)
    r = gaunit.check_har(test_case, tracking_plan, har=har)

    r.print_result(display_ok=True)


if __name__ == "__main__":
    run()
