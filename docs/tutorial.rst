.. _tutorial:

Getting Started
=================

This is a simple step by step guide on how to test Google Analytics 
implementations with GAUnit.

Make sure you have Python and GAUnit installed (see :ref:`install`).

The Scenario
---------------

You will test if the "Add To Cart" *event* is well implemented on Google's 
`Enhanced Ecommerce Demo Store <https://enhancedecommerce.appspot.com/>`_.
There are 2 parts in this tutorial:

- Manual test: you will export network traffic recorded in the Chrome console and check if *events* are OK (`source on Github <https://github.com/VinceCabs/GAUnit/tree/master/samples/getting_started>`_)
- Auto test: then, you will use GAUnit APIs to perform a full automated test with Selenium and BrowserMob Proxy (`source on Github <https://github.com/VinceCabs/GAUnit/tree/master/samples/auto_test_with_proxy>`_).

Your *test case* will consist of a few simple steps:

1. Go to https://enhancedecommerce.appspot.com/
2. Click on the "Compton T-Shirt" product
3. Click on the "Add To Cart" button
4. Test if all events are well implemented

.. image:: img/demo_store.gif

**Let's start!**

Write your tracking plan
------------------------------

You need a name for your *test case*. Let's call it ``ga_demo_store_add_to_cart``.

GAUnit offers various ways to define a *tracking plan*. Below, you will
use a JSON file. You could also use Google Sheet or Python dictionary to define which
events you expect for your test case.

First, create a ``tracking_plan.json`` file where you specify the expected 
events:

.. code-block:: JSON

   {
      "test_cases": {
         "demo_store_add_to_cart": {
            "events": [
               {
                  "t": "pageview",
                  "dt": "Home"
               },
               {
                  "t": "pageview",
                  "dt": "Product View"
               },
               {
                  "t": "event",
                  "ec": "ecommerce",
                  "ea": "add_to_cart",
                  "ev": "44",
                  "pr1nm": "Compton T-Shirt",
                  "pr1pr": "44.00"
               }
            ]
         }
      }
   }

Few remarks here:

- In a *tracking plan*, you can define more than one *test case*. Which is normal, given that you may have several test case for your website!
- For this test case, you expect 3 events: 
   - the ``Home`` page view, 
   - the ``Product View`` page view,
   - the ``Add To Cart`` click (with event value and product price)
- Events are defined by their URL parameters as per the *Measurement Protocol* (`GA <https://developers.google.com/analytics/devguides/collection/protocol/v1/parameters>`_ and `GA4 <https://developers.google.com/analytics/devguides/collection/protocol/ga4>`_). In future versions of GAUnit, you will able to use original API parameters.

.. note::

   GAUnit is compatible with all versions of GA:
   `analytics.js <https://developers.google.com/analytics/devguides/collection/protocol/v1/parameters>`_, 
   `gtag.js <https://developers.google.com/analytics/devguides/collection/gtagjs>`_ 
   and `GA4 properties <https://developers.google.com/analytics/devguides/collection/ga4>`_


Manual Check
--------------------------

In this part, you will export network traffic into a HAR file. 
Then, **you will use GAUnit to check if tracking plan is OK**.

.. note::

   In this tutorial, we use Chrome, but you could use any tool 
   to get an HAR file: Firefox Developer Tool, proxies, etc.

Open Chrome Network panel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open Chrome and open DevTools: *Command+Option+J* (Mac) or *Control+Shift+J* (Windows, Linux, Chrome OS).

Go to the Network panel and check "Preserve Log":

.. image:: img/network_panel.png

Browse site and export HAR file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Let's start our test case!**

On the same Chrome tab, enter this address: https://enhancedecommerce.appspot.com/. 
It is important to use the same tab to record the browsing session.

Click on the "Compton T-Shirt".

On the Compton T-Shirt product page, click on the "Add To Cart" button.

.. image:: img/demo_store.gif

Export the browsing session into a HAR File: in the Network panel, 
click on the small "Export HAR..." icon:

.. image:: img/export_har.png

Save the HAR file in the same directory you use 
for this tutorial. Name it ``demo_store_add_to_cart.har``.

Check if Google Analytics events are OK 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Almost done!**

You will write a simple Python script to check if the expected events (defined in
tracking plan) were fired.

Create a new ``demo_store_add_to_cart.py`` Python file.

.. note::

   Use this command at each step to run the file: 
   ``python demo_store_add_to_cart.py``

First, add these lines to create a :class:`~gaunit.TrackingPlan` and import  
the ``tracking_plan.json`` file you wrote ealier.

.. code:: Python

   import gaunit
   tracking_plan = gaunit.TrackingPlan.from_json("tracking_plan.json")

*Optional*: print the events for your test case with 
:meth:`~gaunit.TrackingPlan.get_expected_events()`

.. code:: Python

   events = tracking_plan.get_expected_events("demo_store_add_to_cart")
   print(events)
   # [{"t": "pageview", "dt": "Home"}, ...]

Now, let's :meth:`~gaunit.check_har()` and print the result.

.. code:: Python

   # get result
   r = gaunit.check_har(
      "demo_store_add_to_cart", tracking_plan, har_path="demo_store_add_to_cart.har"
   )
   print( r.was_successful() )
   # True

The :meth:`~gaunit.Result.was_successful()` method is the simplest way to get the result, but you can 
also get more details. For example:

.. code:: Python

   # Checklist of the expected events actually found in HAR ('True' if present)
   print( r.checklist_expected_events )
   # [True, True, True]

   # All GA events actually found in HAR
   print ( r.actual_events )
   # [{'v': '1', '_v': 'j87', 'a': '1597243964', 't': 'pageview', 'dt': 'Home'}, ..]

   # Pretty print the result of the test (and display all events)
   r.print_result(display_ok=True)

This last line shall print this in console:

.. image:: img/print_result.jpg

**Bravo! You've just made your first GAUnit test!**

Bonus: do the same with command line
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes, it's better to use command line directly, instead of Python.
GAUnit lets you do that:

.. code:: console

   $ gaunit demo_store_add_to_cart.har demo_store_add_to_cart

.. image:: img/print_result.jpg

See :ref:`command` documentation on how to use GAUnit commands. They can be useful for your
CI/CD pipelines.

.. What if test fails?

Automatic test case with Selenium (WIP)
------------------------------------------------------------

