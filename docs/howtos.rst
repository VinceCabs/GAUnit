.. _howtos:

How Tos
=================

In this part, we assume you already have the basics of GAUnit. If not,
we advise to read the :ref:`tutorial` section.

Write a tracking plan
-------------------------

This part describes several methods to create a :class:`~gaunit.models.TrackingPlan`.

Bear in mind that what we call a *tracking plan* here defines the *expected events* for one or more *test cases*.

.. todo: terminology

with a JSON file 
^^^^^^^^^^^^^^^^^

See :ref:`write_tracking_plan` from *Getting Started* section to get an example 
of a ``tracking_plan.json`` file.

You can then import the file with these 2 lines of code:

.. code:: python
    
    import gaunit

    tracking_plan = gaunit.TrackingPlan.from_json("tracking_plan.json")


with Google Sheet
^^^^^^^^^^^^^^^^^^^^

Google Sheets is very convenient to write tracking plans:

- they are shareable and easily accessible
- they allow collaborative editing
- anyone from business teams to business partners can read or contribute

With GAunit, you can import tracking plans from Google Sheets (thanks to `gspread <https://gspread.readthedocs.io/en/latest/>`_). 
Here is how it works :

- Each tab corresponds to a test case
- Lines correspond to events
- Columns correspond to event parameters

In this Spreadsheet, we import one test case named ``ga_demo_store_add_to_cart`` for which we expect 3 events:

.. image:: img/tracking_plan_gsheet.png

This Spreadsheet publicly is available `here <https://docs.google.com/spreadsheets/d/1Kd68s3vLrBqtMDW-PaALZF-5bTm-4J450YbJ3NTbZjQ>`_

**Let's see how to do that!**

Create a Python file where you will import the Google Spreadsheet.
For example, name it ``demo_store_add_to_cart.py``.

First, we need to authenticate with gspread. Have a look at documentation 
(`gspread authentication <https://gspread.readthedocs.io/en/latest/oauth2.html>`_) to choose the method that suits you.
In this example, we use *Service Account* authentication :

.. code:: python

    import gaunit
    import gspread

    gc = gspread.service_account(filename="service_account.json")

.. note::

    Authentication with gspread is mandatory, even for public Spreadsheets.

Now, we can open the Spreadsheet and import it with :meth:`~gaunit.TrackingPlan.from_spreadsheet()` method:

.. code::

    gsheet = gc.open_by_key("1Kd68s3vLrBqtMDW-PaALZF-5bTm-4J450YbJ3NTbZjQ")

    tracking_plan = gaunit.TrackingPlan.from_spreadsheet(gsheet)
    expected_events = tracking_plan.get_expected_events("ga_demo_store_add_to_cart")
    print(expected_events)
    # [{'t': 'pageview', 'dt': 'Home'}, {'t': 'pageview', 'dt': 'Product View'}, {'t': 'event', 'ec': 'ecommerce', ..}]

**It worked!**

.. note::

    Full source code can be found on Github:
    `Tracking Plan from Gsheet sample <https://github.com/VinceCabs/GAUnit/tree/master/samples/tracking_plan_from_gsheet>`_


In Python
^^^^^^^^^^^^

This is very simple. Two methods can help you here: 

- :meth:`~gaunit.TrackingPlan.from_events()` which returns a :class:`~gaunit.models.TrackingPlan`
- :meth:`~gaunit.TrackingPlan.add_test_case()` which adds a test case to an existing instance of :class:`~gaunit.TrackingPlan`

We will see them both. First, write the expected events for your test case 
called ``demo_store_add_to_cart`` in a list:

.. code:: python

    expected_events = [
        {
            "t": "pageview",
            "dt": "Home"
        },
        {   "t": "pageview", 
            "dt": "Product View"
        },
        {
            "t": "event",
            "ec": "ecommerce",
            "ea": "add_to_cart",
            "ev": "44",
            "pr1nm": "Compton T-Shirt",
            "pr1pr": "44.00",
        }
    ]

Now, you can create your tracking plan (2 methods):

.. code:: 

    import gaunit

    tracking_plan = gaunit.TrackingPlan.from_events("demo_store_add_to_cart", expected_events)
    # or you can do this way:
    tracking_plan = gaunit.TrackingPlan()
    tracking_plan.add_test_case("demo_store_add_to_cart", expected_events)

You can add as many test cases as you want with the :meth:`~gaunit.TrackingPlan.add_test_case()` method.

Test Google Analytics implementations 
----------------------------------------

Once you have a :class:`~gaunit.models.TrackingPlan`, you want to run test cases and check GA events. 
This part describes various ways to do that.

Check a HAR file from command line
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See :ref:`gaunit_command` shell command.

Launch a manual browsing session to check events
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes, automating test cases is too much work if you only want to perform
a few tests.

What if we could use Python and GAunit to:

- **open a browser session** already set up with a proxy,
- **manually run** the test case (do the browsing yourself instead of Selenium),
- when done, **let GAUnit check GA events** against a tracking plan?

This is possible and here is how to do that!

First, you need to :ref:`install_selenium_browsermob`.

.. todo: separated part for install

Create a Python file (for examples, named ``demo_store_add_to_cart.py``).
Set up a proxy to record network trafic in HAR and create a webdriver using this proxy
(see :ref:`automatic_test` tutorial in *Getting Started*):

.. code:: Python

    import gaunit
    from browsermobproxy import Server
    from selenium import webdriver

    # set up proxy
    server = Server()  # or add path to binary: 'Server(path="browsermob-proxy")'
    server.start()
    # 'useEcc' is needed to have decent response time with HTTPS
    proxy = server.create_proxy({"useEcc": True})

    proxy.new_har("demo_store_add_to_cart")

    options = webdriver.ChromeOptions()
    options.add_argument("--proxy-server=%s" % proxy.proxy)
    # options.add_argument("--headless")  # uncomment if you want headless Chrome
    capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    capabilities["acceptInsecureCerts"] = True
    driver = webdriver.Chrome(chrome_options=options, desired_capabilities=capabilities)

But now it gets different from a full automated test case; let's use a dialog box to pause 
execution and give hand to the user until he or she says:

.. code:: Python

    from tkinter import messagebox

    messagebox.showinfo(
        "Manual browsing mode",
        "Recording network trafic. Browse site, then press 'OK' when you're finished",
    )

This code will open a dialog box:

.. image:: img/dialog_box.png

The code to run after the user presses 'OK' is: export har, close all, check events againts tracking plan
(see :ref:`automatic_test` tutorial in *Getting Started* section):

.. code:: Python

    # export har and close all
    har = proxy.har
    server.stop()
    driver.quit()

    # check events against tracking plan and print results
    tracking_plan = gaunit.TrackingPlan.from_json("tracking_plan.json")
    r = gaunit.check_har(test_case, tracking_plan, har=har)

    r.print_result(display_ok=True)

.. image:: img/print_result.jpg

**That's it!**

.. note::

   Full source code can be found on Github: `GAUnit manual test session <https://github.com/VinceCabs/GAUnit/tree/master/samples/manual_test_session>`_

Use GAUnit in your CI/CD (WIP)
-----------------------------------

WIP

Other
----------

Extract HAR events for future tests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See :ref:`gaextract_command` shell command.



