.. _command:

Command Line
===================

If you have HAR files, GAUnit commands will greatly help you to quickly see which Google Analytics events
were fired, check if they correspond to what is expected, write a tracking plan from this base, etc.

GAUnit comes with 2 separate commands:

- |command__ga_check|_: from HAR file and a test case name, check events against an existing tracking plan
- |command__ga_extract|_: from a HAR file, extract and print GA events, possibly to add them to a tracking plan

.. |command__ga_check| replace:: ``ga check``
.. |command__ga_extract| replace:: ``ga extract``


``ga``
--------------------------

Arguments
^^^^^^^^^^^^^^^^

``--version``
    Show GAUnit version

``--help``, ``-h``
    Show help on this command

Examples
^^^^^^^^^^^^^^

Get GAUnit version:

.. code:: console

    $ ga --version
    GAUnit X.X.X

.. _command__ga_check:

``ga check``
--------------------------

This command takes a test case name, a HAR file and a tracking plan 
(in the form of a JSON file, ``tracking_plan.json`` by default)
and prints the result in the console. By default, it only prints missing events.

Arguments
^^^^^^^^^^^^^^^^

.. code:: console

    $ ga check file.har test_case


``file.har``
    Path to HAR file you want to check

``test_case``
    Name/id of the test case in the tracking plan

Optional arguments
^^^^^^^^^^^^^^^^^^^^^^^^

``--tracking_plan``, ``-t``
    Path to tracking plan JSON file (``tracking_plan.json`` by default)

``--all``, ``-a``
    Print all expected events from tracking plan (not only the missing ones)

``--help``, ``-h``
    Show help on this command

Examples
^^^^^^^^^^^^^^

*Examples can be run from the* `GAUnit Getting started sample <https://github.com/VinceCabs/GAUnit/tree/master/examples/getting_started>`_
*directory on Github.*

Check a HAR file against a tracking plan:

.. code:: console

    $ ga check demo_store_add_to_cart.har demo_store_add_to_cart
    events in tracking plan: 3
    --------------------------------------------------------------------------------
    GA events found: total:9 / ok:3 / missing:0
    ✔ OK: all expected events found

Specific path for the tracking plan:

.. code:: console

    $ ga check -t tracking_plan.json demo_store_add_to_cart.har demo_store_add_to_cart
    events in tracking plan: 3
    --------------------------------------------------------------------------------
    GA events found: total:9 / ok:3 / missing:0
    ✔ OK: all expected events found

Print all events (not only the missing ones):

.. code:: console

    $ ga check --all demo_store_add_to_cart.har demo_store_add_to_cart
    events in tracking plan: 3
    ================================================================================
    {'t': 'pageview', 'dt': 'Home'}
                                                                            ... OK
    ================================================================================
    {'t': 'pageview', 'dt': 'Product View'}
                                                                            ... OK
    ================================================================================
    {'t': 'event',
    'ec': 'ecommerce',
    'ea': 'add_to_cart',
    'ev': '44',
    'pr1nm': 'Compton T-Shirt',
    'pr1pr': '44.00'}
                                                                            ... OK
    --------------------------------------------------------------------------------
    GA events found: total:9 / ok:3 / missing:0
    ✔ OK: all expected events found

.. _command__ga_extract:

``ga extract``
--------------------------

This command takes a HAR file, extracts all Google Analytics events and
prints them in the console (Python dict format). You can also filter events parameters.

Purposes of this command are :

- extract events and use them as an input for future tracking plans
- look for specific events and parameters after a browsing session

Arguments
^^^^^^^^^^^^^^^^

.. code:: console

    $ ga extract file.har

``file.har``
    Path to HAR file containing GA events

Optional arguments
^^^^^^^^^^^^^^^^^^^^^^^^

``--filter``, ``-f``
    List of events parameters you want to extract, separated by a comma (``--filter a,b,c``).
    Other parameters are filtered out. 

``--help``, ``-h``
    Show help on this command

Examples
^^^^^^^^^^^^^^

*Examples can be run from the* `GAUnit Getting started sample <https://github.com/VinceCabs/GAUnit/tree/master/examples/getting_started>`_
*directory on Github.*

Show all events found in a HAR file:

.. code:: console

    $ ga extract demo_store_add_to_cart.har 
    [{'_v': 'j87', 'a': '1597243964', 'dt': 'Home', 't': 'pageview', 'v': '1'},
     {'_gid': '1844211766.1609794530',
      '_s': '2',
      '_u': 'aGBAAUALAAAAAC~',
      '_v': 'j87',
      'a': '2035613723',
      ...

Filter events. Only show event type and page title :

.. code:: console

    $ ga extract --filter t,dt,ea demo_store_add_to_cart.har
    [{'dt': 'Home', 't': 'pageview'},
     {'dt': 'Home', 'ea': 'view_item_list', 't': 'event'},
     {'dt': 'Home', 'ea': 'view_promotion', 't': 'event'},
     {'dt': 'Home', 'ea': 'select_content', 't': 'event'},
     {'dt': 'Product View', 't': 'pageview'},
     {'dt': 'Product View', 'ea': 'view_item', 't': 'event'},
     {'dt': 'Product View', 'ea': 'view_promotion', 't': 'event'},
     {'dt': 'Product View', 'ea': 'view_item_list', 't': 'event'},
     {'dt': 'Product View', 'ea': 'add_to_cart', 't': 'event'}]
