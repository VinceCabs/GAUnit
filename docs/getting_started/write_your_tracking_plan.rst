.. _getting_started__write_your_tracking_plan:

Write your tracking plan 📑
------------------------------

GAUnit offers various ways to define a *tracking plan*. Below, you will
use a JSON file. You could also use Google Sheets or Python dictionaries to define which
events you expect for your test case, but that's for later (see :ref:`howtos`).

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

- In a *tracking plan*, you can define more than one *test case*. Which is normal, given that you may have several test cases for your website!
- Here, we named our *test case* ``demo_store_add_to_cart``
- For this test case, you expect at least 3 events: 
   - the ``Home`` page view, 
   - the ``Product View`` page view,
   - the ``Add To Cart`` click (with event value ``"ev"`` and product price ``"pr1pr"``)

.. note::

   GAUnit is compatible with all versions of GA:
   `analytics.js <https://developers.google.com/analytics/devguides/collection/protocol/v1/parameters>`_, 
   `gtag.js <https://developers.google.com/analytics/devguides/collection/gtagjs>`_ 
   and `GA4 properties <https://developers.google.com/analytics/devguides/collection/ga4>`_



