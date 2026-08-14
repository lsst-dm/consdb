##########
Wide Views
##########

A *wide view* is intended to be a single database view, defined for one instrument and one
observation type, that joins together the tables holding data for that observation type. Its purpose
is to let a client retrieve everything ConsDB knows about a single exposure or visit in one request,
without needing to know which tables that information is spread across or how to join them. The REST
API already exposes this idea through the ``/query/{instrument}/{obs_type}/obs/{obs_id}`` endpoint.

.. note::

   The wide views are not implemented. No ConsDB schema currently contains a view matching the
   expected naming pattern, and as a result the endpoint described here returns an error for every
   request. This page records what the service already expects of a wide view, so that the views can
   be created at a future date.


Current status
==============

The code in pqserver is implemented for wide views. The views themselves are not present in the
database. The request handler is ``get_all_metadata()`` in
``python/lsst/consdb/handlers/external.py``, and the helper that locates a view is
``InstrumentTable.compute_wide_view_name()`` in ``python/lsst/consdb/cdb_schema.py``.

Implementation of wide views requires:

#. Creating the SQL code to generate the view based on the schema as it exists now.
#. Generalizing that code to handle schema migrations, using either felis or the
   YAML files in the sdm_schemas repository.
#. Adding to Alembic such that relevant code is automatically generated as needed when the schema
   changes, to delete the views and re-create them.

It should be noted that PostgreSQL limits tables to 1,600 columns and 8 kilobytes per row (not
counting offloading of data using TOAST). This may present an obstacle in the implementation of the
wide view feature, and it might turn out to be necessary to pick a subset of columns that will be
contained in the wide views. At present, the tables seem small enough that wide views can accomodate
everything, but it is not clear whether this will remain true as ConsDB grows.

What the service expects of a wide view
=======================================

Anyone implementing the views should treat the following as requirements, because the existing
handler will not work correctly if they are not met.

Naming and location
-------------------

A wide view must be named ``{obs_type}_wide_view`` and must live in the ``cdb_{instrument}`` schema
of the instrument it describes, where the instrument name is lowercase. The observation type is one
of ``exposure``, ``visit1``, ``ccdexposure``, or ``ccdvisit1``; these are the members of
``ObsTypeEnum``, and the value supplied by a caller is matched case-insensitively. A complete set of
views for LSSTCam would therefore be ``cdb_lsstcam.exposure_wide_view``,
``cdb_lsstcam.visit1_wide_view``, ``cdb_lsstcam.ccdexposure_wide_view``, and
``cdb_lsstcam.ccdvisit1_wide_view``.

There is no requirement that every observation type have a view. The service reports the observation
types that are actually available, so a partial implementation is acceptable and will simply offer
fewer options.

The identifier column
---------------------

The endpoint selects a single row by matching the ``obs_id`` path parameter against one column of
the view. That column is chosen during reflection by taking the first name present in this ordered
list:

#. ``ccdvisit_id``
#. ``visit_id``
#. ``ccdexposure_id``
#. ``exposure_id``
#. ``obs_id``

A wide view must therefore expose at least one of these columns, or the endpoint will fail. If it
exposes several, the earliest in the list wins, regardless of which one a caller might consider more
natural. Because this choice determines what callers must pass as ``obs_id``, it should be made
deliberately rather than inherited by accident from whichever tables are joined.

Uniqueness
----------

The handler retrieves the row with SQLAlchemy's ``one_or_none()``. A view that returns more than one
row for a single identifier will therefore raise ``MultipleResultsFound``, which is a subclass of
``SQLAlchemyError`` and is reported to the caller as an HTTP 500 rather than as a meaningful
message. Each wide view must yield at most one row per identifier value.

Response shape
--------------

The row is converted with ``dict(row)`` and returned as a flat JSON object whose keys are column
names. Two consequences follow. Column names must be unique across all of the joined tables, since a
duplicate name would collapse into a single key. Every column must also be JSON-serializable, which
deserves attention for types such as timestamps and PostgreSQL-specific geometric types.


The ``flex`` query parameter
============================

The endpoint accepts an optional ``flex`` query parameter. When it is set, the flexible metadata for
the observation is merged into the same flat dictionary as the wide view columns, rather than being
nested under a separate key.

This means that flexible metadata keys and wide view column names share a single namespace. A
flexible metadata key that happens to match a column name will overwrite that column in the
response, silently and without error, because the merge is a plain dictionary update. Whether to
guard against this, and how, is an open question for the implementation.
