# GAUnit

[![Build Status](https://travis-ci.org/VinceCabs/GAUnit.svg?branch=master)](https://travis-ci.org/VinceCabs/GAUnit)
[![Documentation Status](https://readthedocs.org/projects/gaunit/badge/?version=latest)](https://gaunit.readthedocs.io/en/latest/?badge=latest)

GAUnit is a Python library for testing Google Analytics implementations with Selenium or RobotFramework test cases.

It is designed to be used within your pipelines in various environments such as traditional websites, Single Page Applications or Mobile Apps.

## Installation

You will need Python 3.7+ installed.

```sh
pip install gaunit
```

## Usage

Define your expected GA tracking plan for a given test case. Example : tracking the "play" button on a video from a product page:

```JSON
{
    "my_test_case": [
        {
            "t": "pageview",
            "dp": "my_product_page_name"
        },
        {
            "t": "event",
            "ec": "Video",
            "ea": "Play"
        }]
}
```

### Run your automated test wih Python

Run a test, export har and check it against your expected tracking plan:

```python
import gaunit
import browsermobproxy

# Run your Selenium test here and export har 
# (see samples below or how-tos for more details)
# ...

# import tracking plan from json file or event from Google Sheets
tracking_plan = gaunit.TrackingPlan.from_json("tracking_plan.json")
# check GA events
result = gaunit.check_har(
    "my_test_case", tracking_plan, har_path="my_test_case.har"
)
print(result.checklist_expected)
# [True, True] congrats! both events (pageview and click) were  fired.
```

### Or manually check HAR files with command line

Alternatively to automatic tests, you can manually browse your website, export a HAR file and check it through command line :

```sh
$ gaunit test_case.har my_test_case  # passed
events in tracking plan: 3
--------------------------------------------------------------------------------
GA events found: total:4 / ok:3 / missing:0
✔ OK: all expected events found

$ gaunit test_case.har my_test_case  # failed
events in tracking plan: 3
================================================================================
{'t': 'event', 'ec': 'Video', 'ea': 'Play'}
                                                                     ... missing
--------------------------------------------------------------------------------
GA events found: total:11 / ok:1 / missing:2
❌ FAILED: events missing
```

## Run your first tests (full working samples)

### Automated test using a proxy

We can use BrowserMob Proxy to intercept Google Analytics events.

- Install [Selenium](https://selenium-python.readthedocs.io/) and [Browsermob Proxy](https://browsermob-proxy-py.readthedocs.io/) packages:

  ```sh
  pip install selenium browsermob-proxy
  ```

- Download **BrowserMob Proxy** [latest release](https://github.com/lightbody/browsermob-proxy/releases) (note: install [Java](https://www.oracle.com/java/technologies/javase-jre8-downloads.html)).
  - add `bin/` directory to your %PATH

- Download [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)
  - add it to your %PATH or copy it in your working directory (more details [here](https://selenium-python.readthedocs.io/installation.html#drivers))

- Run the test:

  ```sh
  python samples/auto_test_with_proxy/demo_store_add_to_cart.py
  ```

### Automated test with Performance Log (Chrome only)

Performance Log is a fast and easy way to intercept GA events (GET events only). It works without BrowserMob Proxy.

Note: this method works for `analytics.js` but might not work for new GA implementations, such as transport beacon or GA4.

- Install Selenium and ChromeDriver (same as above)

- Run the test:

  ```sh
  python samples/auto_test_with_perf_log/demo_store_add_to_cart.py
  ```

### Robot Framework

If you want to use RobotFramework, check [GAUnit Library for Robot Framework](https://github.com/VinceCabs/robotframework-gaunitlibrary)

## Documentation

*Still work in progress, sorry!*

Full documentation will soon be available [here](https://gaunit.readthedocs.io/).

In the meantime, please refer to [samples](samples/) and [Developer interface](https://gaunit.readthedocs.io/en/latest/api.html#main-api).

## Why GAUnit?

Testing your Google Analytics implementation is often time consuming and, let's say it, sometimes very boring!

But most of all, if your tracking is not reliable as your application evolves, your reportings won't be either. People in your company will loose confidence in your reportings when they have to take important business decisions. You will provide great reportings if you integrate tracking in your DevOps pipelines (and thus, in you Quality Assurance plan).

[Some great tools](https://www.simoahava.com/analytics/automated-tests-for-google-tag-managers-datalayer/) let you automatically test your DataLayer, but sometimes it is not enough: you not only want to test `pageview`s, but also `event`s like clicks and Ecommerce. You might want to test tracking in various environments like Single Page Application, AMP or Mobile Applications. GAUnit lets you do just that.

## Contributing

GAUnit can be useful for several companies. Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Licence

This project is licensed under the MIT License - see the [LICENSE](LICENCE) file for details.

## Acknowledgments

GAUnit was inspired by [WAUnit](https://github.com/joaolcorreia/WAUnit). We decided to create a new library commpatible with Python 3 and easier to set up.

## Roadmap

- Complete test case samples with RobotFramework mobile app
- Tracking plan using analytics.js, GTM or GA4 syntax
- Dockerize (for simpler set up)
