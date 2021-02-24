# GAUnit

[![Build Status](https://travis-ci.org/VinceCabs/GAUnit.svg?branch=master)](https://travis-ci.org/VinceCabs/GAUnit)
[![Documentation Status](https://readthedocs.org/projects/gaunit/badge/?version=latest)](https://gaunit.readthedocs.io/en/latest/?badge=latest)

GAUnit is a Python library used for Google Analytics implementations testing.

It is designed to be used within your pipelines in various environments such as traditional websites or Single Page Applications.

GAUnit is compatible with [GA4](https://developers.google.com/analytics/devguides/collection/ga4).

## Features

- Automate tests for Google Analytics implementations
- Write tracking plans with Python dictionaries, JSON files or Google Sheets
- Check HAR files against a tracking plan
- Extract GA events from HAR files
- Use Python or command line

## Installation

You will need [Python 3.7+](https://www.python.org/downloads/) installed.

Use pip:

```sh
pip install gaunit
```

## Usage

Let's say you have a new video player on your product page and you want
to check that the right Google Analytics event is sent when the user clicks on "Play":

```python
expected_events = [
    {
        "t": "pageview",
        "dp": "my_product_page_name"
    },
    {
        "t": "event",
        "ec": "Video",
        "ea": "Play"
    }
]
```

### Run an automated test with Python

Run a selenium test case, export har and check it against your expected _tracking plan_:

```python
import gaunit

# Run your Selenium test here and export har
# (see Documentation or examples for more details)
# ...

# create your tracking plan from dict, JSON files or Google Sheets
tracking_plan = gaunit.TrackingPlan.from_events("my_test_case", expected_events)
# check GA events
r = gaunit.check_har("my_test_case", tracking_plan, har_path="my_test_case.har")
print(r.was_successful())
# True
# Congrats! both events (pageview and click) were fired.
```

### Or manually check HAR files with command line

Alternatively to automatic tests, you can manually browse your website, export a
HAR file and check it through command line:

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

### Robot Framework

If you want to use RobotFramework, check [GAUnit Library for Robot Framework](https://github.com/VinceCabs/robotframework-gaunitlibrary)

## Documentation

[Getting Started](https://gaunit.readthedocs.io/en/latest/getting_started.html).

Full documentation is available [here](https://gaunit.readthedocs.io/).

## Why GAUnit?

Testing your Google Analytics implementation is often time consuming and, let's say it, sometimes very boring!

But most of all, if your tracking is not reliable as your application evolves, your reportings won't be either. People in your company will loose confidence in your reportings when they have to take important business decisions. You will provide great reportings if you integrate tracking in your DevOps pipelines (and thus, in you Quality Assurance plan).

[Some great tools](https://www.simoahava.com/analytics/automated-tests-for-google-tag-managers-datalayer/) let you automatically test your DataLayer, but sometimes it is not enough: you not only want to test `pageview`s, but also `event`s like clicks and Ecommerce. You might want to test tracking in various environments like Single Page Application, AMP or Mobile Applications. GAUnit lets you do just that.

## Contributing

GAUnit can be useful for several companies. Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Licence

This project is licensed under the MIT License - see the [LICENSE](LICENCE) file for details.

## Acknowledgments

GAUnit was inspired by [WAUnit](https://github.com/joaolcorreia/WAUnit). We decided to create a new library compatible with Python 3 and easier to set up.

## Roadmap

- Mobile Apps
- Tracking plan using analytics.js, GTM or GA4 API syntax
- Dockerize (for simpler set up and CI/CD)
