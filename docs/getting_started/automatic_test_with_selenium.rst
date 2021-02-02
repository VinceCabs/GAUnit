.. _automatic_test:

Automatic test with Selenium 🚀
------------------------------------------------------------

**Instead of tedious manual tests, let's automate!**

What if we could automate the whole process?

- browse on the site
- record all GA events
- check the events against the tracking plan

.. _install_selenium_browsermob:

Install Selenium and BrowserMob Proxy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First, you need to install Selenium to automate browsing and 
BrowserMob Proxy to intercept Google Analytics events.

- Install `Selenium <https://selenium-python.readthedocs.io/>`_ and `Browsermob Proxy <https://browsermob-proxy-py.readthedocs.io>`_ Python packages:

.. code:: console

   pip install selenium browsermob-proxy

- Download `BrowserMob Proxy latest release <https://github.com/lightbody/browsermob-proxy/releases/latest>`_ (note: requires `Java <https://www.oracle.com/java/technologies/javase-jre8-downloads.html>`_).
   - unzip it where convenient for you
   - add the ``bin/`` directory to your ``%PATH``

- Download `ChromeDriver <https://sites.google.com/a/chromium.org/chromedriver/downloads>`_
   - unzip it where convenient for you
   - add it to your ``%PATH`` or copy it in your working directory (more details `here <https://selenium-python.readthedocs.io/installation.html#drivers>`_)

- Here is a simple way to test if install is OK:

.. code:: console

   $ browsermob-proxy --version
   BrowserMob Proxy X.X.X
   $ chromedriver --version
   ChromeDriver XX.XX.XX (XX)

Full automation with Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Make sure you have done this part:* :ref:`write_tracking_plan`

**You will now fully automate the process of testing GA implementation**.

Create a new Python file, for example: ``demo_store_add_to_cart.py`` as in previous section.

Import the required packages for our test:

.. code:: Python

   import gaunit
   from browsermobproxy import Server
   from selenium import webdriver

Create a BrowserMob Proxy server and activate it:

.. code:: python

   # set up proxy
   server = Server()  # or add path to binary: 'Server(path="browsermob-proxy")'
   server.start()
   # 'useEcc' is needed to have decent response time with HTTPS
   proxy = server.create_proxy({"useEcc": True})

Set BrowserMob Proxy to record a new har:

.. code:: python

   proxy.new_har("demo_store_add_to_cart")

Create a webdriver and configure it to use the newly created proxy:

.. code:: python

   options = webdriver.ChromeOptions()
   options.add_argument("--proxy-server=%s" % proxy.proxy)
   # options.add_argument("--headless")  # uncomment if you want headless Chrome
   capabilities = webdriver.DesiredCapabilities.CHROME.copy()
   capabilities["acceptInsecureCerts"] = True
   driver = webdriver.Chrome(chrome_options=options, desired_capabilities=capabilities)

Write the test case we described earlier (see :ref:`the_scenario`) with Selenium API: 

.. code:: python

   driver.get("https://enhancedecommerce.appspot.com/")  # go to Demo Store
   driver.find_element_by_id("homepage-9bdd2-1").click()  # click on Compton T-Shirt
   driver.find_element_by_id("addToCart").click()  # click on "Add To Cart"

Export har in a Python dict and close all.

.. code:: Python

   har = proxy.har
   server.stop()
   driver.quit()

Check the har (code is almost the same as in :ref:`manual_test`)

.. code:: python

   tracking_plan = gaunit.TrackingPlan.from_json("tracking_plan.json")
   r = gaunit.check_har("demo_store_add_to_cart", tracking_plan, har=har)
   print( r.was_successful() )
   # True

   # Pretty print the result of the test (and display all events)
   r.print_result(display_ok=True)

.. image:: ../img/print_result.jpg

.. note::

   Full source code can be found on Github: `GAUnit automatic test sample <https://github.com/VinceCabs/GAUnit/tree/master/samples/auto_test_with_proxy>`_