.. _tutorial:

Tutorial
=================

**WIP**
a simple introduction to tracking plan testing with GAUnit.

The Scenario
---------------

We will check if Google Analytics tags are well implemented on website XXX.

- first, we will do it manually: we will export network traffic recorded in the Chrome console and use command line to check if tracking plan is OK
- second, we will use GAUnit APIs in an automated Selenium test case.

Write our tracking plan
------------------------------

Manual Check
--------------------------

Browse your site and export HAR file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Check if Google Analytics hits are OK 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Fix you GA tags and rerun tests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Automatic test case with Selenium
----------------------------------------------------
