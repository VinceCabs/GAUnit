# GAUnit

[![Build Status](https://travis-ci.org/VinceCabs/GAUnit.svg?branch=master)](https://travis-ci.org/VinceCabs/GAUnit)
[![Documentation Status](https://readthedocs.org/projects/gaunit/badge/?version=latest)](https://gaunit.readthedocs.io/en/latest/?badge=latest)

GAUnit is a Python library for testing Google Analytics implementations with Selenium or RobotFramework test cases.

It is designed to be used within your pipelines in various environments such as traditional websites, Single Page Applications or Mobile Apps.

## Installation

You will need Python 3.6+ installed.

```sh
pip3 install gaunit  # Linux
pip install gaunit  # Windows
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
# (see howtos or samples for more details)
# ...

result = gaunit.check_har(
    "my_test_case", "tracking_plan.json", har_path="my_test_case.har"
)
print(result.checklist_expected)
# [True, True] congrats! both events (pageview and click) were  fired.
```

### Or manually check HAR files

Alternatively to automatic tests, you can manually browse your website, export a HAR file and check it through command line :

```sh
$ gaunit my_test_case my_test_case.har
[True, True]
```


## Run your first tests (full working samples)

### Automated test using a proxy

We can use BrowserMob Proxy to intercept Google Analytics events.

- Install [Selenium](https://selenium-python.readthedocs.io/) and [Browsermob Proxy](https://browsermob-proxy-py.readthedocs.io/) packages:

  ```sh
  pip3 install selenium browsermobproxy # Linux
  pip install selenium browsermobproxy # Windows
  ```

- Download **BrowserMob Proxy** [latest release](https://github.com/lightbody/browsermob-proxy/releases) (note: install [Java](https://www.oracle.com/java/technologies/javase-jre8-downloads.html)).
  - add `bin/` directory to your %PATH

- Download [Geckodriver/Firefox](https://github.com/mozilla/geckodriver/releases)
  - add it to your %PATH or copy it in your working directory (more details [here](https://selenium-python.readthedocs.io/installation.html#drivers))

- Run the test:

  ```sh
  python3 samples/home_engie_with_proxy.py  # Linux
  python samples/home_engie_with_proxy.py  # Windows
  ```

### Automated test with Performance Log (Chrome only)

Performance Log is a fast and easy way to intercept GA events (GET events only).

Note: this method works for `analytics.js` but might not work for new GA implementations, such as GA4 or `gtag.js`.*

- Install Selenium (see above) and  [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)

- Run the test:

  ```sh
  python3 samples/home_engie_with_perf_log.py  # Linux
  python samples/home_engie_with_perf_log.py  # Windows
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
