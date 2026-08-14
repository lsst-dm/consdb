##########
Python API
##########

These pages come from the docstrings in ``python/lsst/consdb``.

The page covers the modules whose docstrings build without a warning today.
The other modules need work before they can go here: some need a dependency that the ``docs`` environment in ``tox.ini`` does not install, and some have docstrings that Sphinx cannot parse.
The :doc:`../user-guide/rest-api-and-clients` page gives the interactive REST API documentation that ``pqserver`` serves.

Each directive lists the names its module imports under ``:skip:``, because ``automodapi`` documents every public name in a module that does not define ``__all__``.

.. automodapi:: lsst.consdb.exceptions
   :no-inheritance-diagram:
   :skip: Any

.. automodapi:: lsst.consdb.utils
   :no-inheritance-diagram:

.. automodapi:: lsst.consdb.dependencies
   :no-inheritance-diagram:

.. automodapi:: lsst.consdb.consistency_queries
   :no-inheritance-diagram:

.. automodapi:: lsst.consdb.daily_consistency_check
   :no-inheritance-diagram:
   :skip: Mapping, URL, defaultdict

.. automodapi:: lsst.consdb.handlers.consistency_page
   :no-inheritance-diagram:
