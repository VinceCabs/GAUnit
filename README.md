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
from gaunit.GAUnit import GAUnit
import browsermobproxy

# Instantiate GAUnit and set your test case name
g = GAUnit()

# Run your Selenium test here with browsermob-proxy and export har
# ...

checklist = g.check_tracking_from_har("my_test_case.har")
print(checklist)  # [True, False] oups! pageview is fine but video "play" button is not properly tracked.
```

See a full working example [here](./test_home_engie.py). You can also use GAUnit within unittest or RobotFramework test cases (WIP : we will soon add samples).

## Installation

You will need Python 3.6+ installed.

- install gaunit :

```sh
pip3 install gaunit  # Linux
pip install gaunit  # Windows
```

- If you want to use RobotFramework module :

```sh
pip3 install -r requirements/robot.txt  # Linux
pip install -r requirements/robot.txt  # Windows
```

- Download **browsermob-proxy** [latest release](https://github.com/lightbody/browsermob-proxy/releases) (note: you'll need [Java](https://www.oracle.com/java/technologies/javase-jre8-downloads.html)).
  - Add `bin/` directory to your %PATH

- Download a **webdriver**. To run the [example](./test_home_engie.py), get Geckodriver [latest release](https://chromedriver.chromium.org/getting-started) 
  - add it to your %PATH or copy it in your working directory

## Run your first tests

Test with Selenium Python

```sh
python3 test_home_engie.py  # Linux
python test_home_engie.py  # Windows
```

Test with RobotFramework

```sh
robot samples/test_home_engie.robot
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

- Complete test case samples with RobotFramework for web and mobile app
- Tracking plan using analytics.js or GTM syntax
- Dockerize (for simpler set up)
