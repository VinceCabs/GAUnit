# GAUnit

GAUnit is a Python library for testing Google Analytics implementations with Selenium or RobotFramework test cases.

It is designed to be used within your pipelines in various environments such as traditional websites, Single Page Applications or Mobile Apps.

## Usage

Define your expected GA [tracking plan](tracking_plan.json) for a given test case. Example : tracking a click on a video:

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

Launch GAUnit proxy:

```sh
sh ./launch_proxy.sh
```

Run your test wih Python and check it against your expected tracking plan:

```python
from gaunit.GAChecker import GAChecker

# Instantiate GAUnit and set your test case name
gc = GAChecker()
gc.set_test_case("my_test_case")

# Run your Selenium test here
# (configure proxy at 127.0.0.1:8080)
# ...

checklist = gc.check_tracking()
print(checklist)  # [True, False] oups! pageview is fine but video "play" button is not properly tracked.

```

You can also use GAUnit within unittest or RobotFramework test cases. We provide a unit test case [sample](test_home_engie.py) to help you getting started (WIP : we will soon add more samples).

## Installation

You will need Python 3.6+ installed.

GAUnit uses [mitmproxy](https://mitmproxy.org/) to log Google Analytics hits. mitmproxy is easy to use and works like charm with HTTPS.

- Follow mitmproxy [installation instructions](https://docs.mitmproxy.org/stable/overview-installation/).
  - If your website uses HTTPS, you must [install mitmproxy certificates](https://docs.mitmproxy.org/stable/concepts-certificates/). If you do this for the first time, trust me, it is easier to do than you might think!

If you've never used Selenium with ChromeDriver, you might need to install both :

- Install Selenium

```sh
pip3 install selenium  # Linux
pip install selenium  # Windows
```

- Follow ChromeDriver [installation instruction](https://chromedriver.chromium.org/getting-started) (make sure ChromeDriver is in your path or in your working directory).


## Why GAUnit?

Testing your Google Analytics implementation is often time consuming and, let's say it, sometimes very boring! 

But most of all, if your tracking is not reliable as your application evolves, your reportings won't be either. People in your company will loose confidence in your reportings when they have to take important business decisions. You will provide great reportings if you integrate tracking in your DevOps pipelines (and thus, in you Quality Assurance plan).

[Some great tools](https://www.simoahava.com/analytics/automated-tests-for-google-tag-managers-datalayer/) let you automatically test your DataLayer, but sometimes it is not enough: you not only want to test `pageview`s, but also `event`s like clicks and Ecommerce. You might want to test tracking in various environments like Single Page Application, AMP or Mobile Applications. GA Unit lets you do just that.

## Contributing

GAUnit can be useful for several companies. Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Licence

This project is licensed under the MIT License - see the [LICENSE](LICENCE) file for details.

## Acknowledgments

GAUnit was inspired by [WAUnit](https://github.com/joaolcorreia/WAUnit). We decided to create a new library for compatibility with Python 3 and latest versions of mitmproxy.

## Roadmap

- Complete test case samples with RobotFramework for web and mobile app
- Tracking plan using analytics.js or GTM syntax
- Dockerize (for simpler set up)
