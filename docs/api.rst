.. _api:

Developer Interface
===================

.. module:: gaunit

Main API
-----------

All the methods you will need for general usage.

.. autofunction:: check_har
.. autofunction:: check_perf_log

Classes
----------

.. autoclass:: TrackingPlan
    :members:
.. autoclass:: TestCase
    :members:
.. autoclass:: Result
    :members:

Exceptions 
------------

.. autoexception:: GAUnitException
    :members:

.. autoexception:: TrackingPlanError
    :members:

.. autoexception:: DictXORJsonPathError
    :members:

.. autoexception:: TestCaseCheckError
    :members:
