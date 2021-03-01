.. gaunit documentation master file, created by
   sphinx-quickstart on Wed Nov 18 00:34:15 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to GAUnit's documentation!
===================================

.. image:: https://travis-ci.org/VinceCabs/GAUnit.svg?branch=master
   :target: https://travis-ci.org/VinceCabs/GAUnit
.. image:: https://readthedocs.org/projects/gaunit/badge/?version=latest
   :target: https://gaunit.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

GAUnit is a Python library used for Google Analytics implementations testing.

It is designed to be used within your pipelines in various environments such as traditional websites or Single Page Applications.

GAUnit is compatible with `GA4 <https://developers.google.com/analytics/devguides/collection/ga4>`_.

Features
---------------

- Automate tests for Google Analytics implementations
- Write tracking plans with Python dictionaries, JSON files or Google Sheets
- Check HAR files against a tracking plan
- Extract GA events from HAR files
- Use Python or command line

.. _install:

Installation
----------------

You will need `Python 3.7+ <https://www.python.org/downloads/>`_.

Use pip:

.. code:: console

   pip install gaunit

Usage
--------------

Let's say you have a new video player on your product page and you want 
to check if the right Google Analytics event is sent when the user clicks on "Play":

.. code-block:: python

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

Run an automated test with Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run a selenium test case, export har and check it against your expected tracking plan:

.. code:: python

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

Or manually check HAR files with command line
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Alternatively to automatic tests, you can manually browse your website, export a 
HAR file and check it through command line:

.. code:: console

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


Robot Framework
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to use RobotFramework, check `GAUnit Library for Robot Framework <https://github.com/VinceCabs/robotframework-gaunitlibrary>`_.


Usage
------------

.. toctree::
   :maxdepth: 1

   getting_started
   howtos

Reference & documentation
---------------------------------------------------------------

.. toctree::
   :maxdepth: 2

   command
   api
   tracking_plan

Background / Explanation
-----------------------------

**WIP**

