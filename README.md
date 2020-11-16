# GAUnit

GAUnit is a Python library for testing Google Analytics implementations with Selenium or RobotFramework test cases.

It is designed to be used within your pipelines in various environments such as traditional websites, Single Page Applications or Mobile Apps.

## Usage

Define your expected GA [tracking plan](tracking_plan.json) for a given test case. Example : tracking the "play" button on a video:

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

Run your test wih Python and check it against your expected tracking plan:

```python
import gaunit
import browsermobproxy

# Run your Selenium test here with browsermob-proxy and export har
# ...

result = gaunit.check_har("my_test_case", tracking_plan = "tracking_plan.json", har_path="my_test_case.har")
print(checklist)  # [True, False] oups! pageview is fine but video "play" button is not properly tracked.
```

See a full working example [here](./samples/test_home_engie.py). You can also use GAUnit within unittest or RobotFramework test cases (WIP : we will soon add samples).

## Installation

You will need Python 3.6+ installed.

- install gaunit :

```sh
pip3 install gaunit  # Linux
pip install gaunit  # Windows
```

## Run your first automated tests

- Download **browsermob-proxy** [latest release](https://github.com/lightbody/browsermob-proxy/releases) (note: install [Java](https://www.oracle.com/java/technologies/javase-jre8-downloads.html)).
  - Add `bin/` directory to your %PATH

- Download a **webdriver**. To run the [example](./samples/test_home_engie.py), get Geckodriver [latest release](https://chromedriver.chromium.org/getting-started)
  - add it to your %PATH or copy it in your working directory

Test with Selenium Python

```sh
python3 samples/test_home_engie.py  # Linux
python samples/test_home_engie.py  # Windows
```

If you want to use RobotFramework, check [GAUnit Library for Robot Framework](https://github.com/VinceCabs/robotframework-gaunitlibrary)

## Manually control a HAR file

You can manually browse your website, export a HAR file and check it through command line :

```sh
$ gaunit home_engie home_engie.har
[True, True, True]
$ gaunit -h
usage: gaunit [-h] [-t TRACKING_PLAN] [-v] test_case har_file

positional arguments:
  test_case             name of test case
  har_file              path to HAR file

optional arguments:
  -h, --help            show this help message and exit
  -t TRACKING_PLAN, --tracking_plan TRACKING_PLAN
                        path to tracking plan
  -v, --verbose         print all trackers with their status and all hits
                        recorded
```

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
