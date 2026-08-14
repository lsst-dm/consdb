#######
Schemas
#######

ConsDB is a relational database and uses schemas expressed in the YAML-based Felis format. 
`Felis <https://felis.lsst.io/>`__ is a tool for describing astronomical data catalogs developed
especially for Vera C. Rubin Observatory.

The organization of ConsDB is based on the sources of data used in the database. This can make it
tricky to find the data you're interested in, but this style of organization is chosen to maximize
the integrity of the data and to prevent different data sources from interfering with each other. At
the broadest level, the database is split into (1) the transformed EFD, which draws data from the
`Engineering Facilities Database <https://www.lsst.io/efd-guides/>`__, as the name suggests, and (2)
the mainline CDB, which contains data from the camera header services and from `Rapid Analysis
<https://phalanx.lsst.io/applications/rapid-analysis/index.html>`__.

.. note::

   The Transformed EFD is available only at USDF, not at summit.

The `Science Data Model Schemas site <https://sdm-schemas.lsst.io>`__ provides a web-based browser for ConsDB schemas, including Summit-generated schemas and Transformed EFD schemas.
All ConsDB schemas (one per instrument) are labeled as "ConsDB" or "Transformed EFD" on that site.

ConsDB has two schemas for each instrument.
A ``cdb_*`` schema contains the data that the Summit systems write.
An ``efd_*`` schema contains the data that the Transformed EFD service writes.

A full list of the ConsDB schemas is shown below.
Each name links to the YAML file that defines the schema in the ``sdm_schemas`` repository.

- `cdb_latiss <https://github.com/lsst/sdm_schemas/blob/main/python/lsst/sdm/schemas/cdb_latiss.yaml>`__
- `cdb_lsstcam <https://github.com/lsst/sdm_schemas/blob/main/python/lsst/sdm/schemas/cdb_lsstcam.yaml>`__
- `cdb_lsstcomcam <https://github.com/lsst/sdm_schemas/blob/main/python/lsst/sdm/schemas/cdb_lsstcomcam.yaml>`__
- `cdb_lsstcomcamsim <https://github.com/lsst/sdm_schemas/blob/main/python/lsst/sdm/schemas/cdb_lsstcomcamsim.yaml>`__
- `cdb_startrackerfast <https://github.com/lsst/sdm_schemas/blob/main/python/lsst/sdm/schemas/cdb_startrackerfast.yaml>`__
- `cdb_startrackernarrow <https://github.com/lsst/sdm_schemas/blob/main/python/lsst/sdm/schemas/cdb_startrackernarrow.yaml>`__
- `cdb_startrackerwide <https://github.com/lsst/sdm_schemas/blob/main/python/lsst/sdm/schemas/cdb_startrackerwide.yaml>`__
- `efd_latiss <https://github.com/lsst/sdm_schemas/blob/main/python/lsst/sdm/schemas/efd_latiss.yaml>`__
- `efd_lsstcam <https://github.com/lsst/sdm_schemas/blob/main/python/lsst/sdm/schemas/efd_lsstcam.yaml>`__
- `efd_lsstcomcam <https://github.com/lsst/sdm_schemas/blob/main/python/lsst/sdm/schemas/efd_lsstcomcam.yaml>`__

Each of these corresponds directly to one of the Rubin Observatory instruments, or a simulation
thereof.  They are largely, but not entirely, homologous, meaning the structure of the data matches
across all of the schemas.  No system writes data to the three ``cdb_startracker*`` schemas at this
time.  There is no plan to use them.

The ``efd_scheduler`` schema does not contain instrument data. It contains the task records of the
Transformed EFD service. This schema is meant for internal use by the database services, and does
not contain information that is useful to end users.

The ``efd_*`` schemas are not at the Summit, but they appear at the test stands and at the USDF.
The Transformed EFD service runs at the USDF, and it fills these schemas there.

Each ``cdb_*`` schema has ``exposure`` and ``visit1`` tables; the ``visit1`` tables are using the
one-to-one visit system (each exposure is a visit) and hence are cheaply implemented as views,
although formally visits should only include on-sky exposures.  Each schema also has a
``ccdexposure`` table and ``ccdvisit1`` view for per-CCD values.  There is a ``ccdexposure_camera``
table for certain values the Camera Control System is responsible for.  ``visit1_quicklook`` and
``ccdvisit1_quicklook`` tables are used to hold outputs from Rapid Analysis.  Additional tables can
be added for metadata coming from other sources.  Finally, flexible metadata tables named
``exposure_flexdata`` and ``ccdexposure_flexdata`` are available to hold key/value information on a
temporary or experimental basis.  (Visit flexdata can be added if there is a need.) See :doc:`this
page <flexible-metadata>` for more on flexible metadata.

The ``efd_*`` Transformed EFD tables, which have their own schemas, are described in :doc:`a separate page <transformed-efd>`.

Generally the tables within each schema are normalized so that there is minimal duplication of data other than exposure/visit identifiers between tables.
This may mean that a join is needed to get the desired information or to query on columns in more than one table.
Primary keys, unique keys, and foreign keys are defined to provide indexes for common queries and to speed up those joins.

Tables
======

Each of the instrument schemas presents the same table relationships within the schema. These tables
are in one of two categories: visit-level tables, in which one row is present in the table for each
visit/exposure by the telescope and CCD-level tables, in which each row in the table represents a
single CCD exposure. For CCD-level tables, there are \~200 rows per visit, or, equivalently, \~200
rows per corresponding row in a visit-level table.

Currently the Legacy Survey of Space and Time is designed such that *visits* and *exposures* are the
same thing, i.e., that visits and exposures correspond one-to-one. The assumption that this design
will always be used has crept into many parts of Consolidated Database. If the design of the survey
changes, significant modifications will be needed for the Consolidated Database schema.

Keys
----

The table keys are used to uniquely identify each row in the table. In Consolidated Database, tables
have two sets of keys, either of which can be used to identify a row.

The first set of table keys are the **multi-column keys**. These keys are ``day_obs`` and
``seq_num``, for visit-level tables, plus ``detector`` for CCD-level tables. The ``day_obs`` key is
an integer that corresponds to the observing night of the exposure in the YYYYMMDD format, such as
20250421 for 21 April 2025; this date rolls over at local Noon, so that all images taken on a given
night have the same ``day_obs``. The ``seq_num`` key is an incrementing integer starting at 1 for
the first image of that ``day_obs``. The ``detector`` key is an integer ranging from 0 to 8
inclusive for LSSTComCam, 0 to 204 for LSSTCam, or just zero for LATISS. For more information about
the LSSTCam and LSSTComCam focal planes, see `CTN-001 <https://ctn-001.lsst.io/>`__.

The mapping of LSSTComCam detector numbers to names is as follows:

.. list-table::
   :header-rows: 1

   * - Detector
     - CCD name
     - Detector
     - CCD name
     - Detector
     - CCD name
   * - 0
     - ``R22_S00``
     - 3
     - ``R22_S10``
     - 6
     - ``R22_S20``
   * - 1
     - ``R22_S01``
     - 4
     - ``R22_S11``
     - 7
     - ``R22_S21``
   * - 2
     - ``R22_S02``
     - 5
     - ``R22_S12``
     - 8
     - ``R22_S22``

The ``exposure`` table also carries a ``controller`` column.  It holds the one-letter code of the
controller that took the image.  The Header Service uses it to select the schema: ``O`` (the
observatory control system) goes to the ordinary schema of the instrument, and ``S`` (simulation)
goes to ``cdb_lsstcomcamsim``. *This split applies only to LSSTComCam. For LATISS and LSSTCam, the
architecture is such that simulated data are not loaded into the database at the summit or USDF.*

The second set of table keys are the **single-column keys**. Every table that holds observation data
also carries a single integer column that identifies the row on its own. Which column that is depends
on the level of the table: ``exposure_id`` and ``visit_id`` identify visit-level rows, while
``ccdexposure_id`` and ``ccdvisit_id`` identify CCD-level rows. All four are ``long`` (64-bit
integer) columns.
For the instruments in use, ``exposure_id`` is ``day_obs * 100000 + seq_num``, so the two sets of keys carry the same information.
The daily consistency check (see :doc:`../operator-guide/monitoring`) verifies this relation.

The following table lists the single-column key for each table in the ``cdb_*`` instrument schemas
(``cdb_latiss``, ``cdb_lsstcam``, ``cdb_lsstcomcam``, and ``cdb_lsstcomcamsim``), alongside the
multi-column primary key that is now declared for that table.

.. list-table:: Keys in the ``cdb_*`` schemas
   :header-rows: 1
   :widths: 32 24 44

   * - Table
     - Single-column key
     - Declared primary key
   * - ``exposure``
     - ``exposure_id``
     - ``day_obs``, ``seq_num``
   * - ``exposure_quicklook``
     - ``exposure_id``
     - ``day_obs``, ``seq_num``
   * - ``visit1``
     - ``visit_id``
     - ``day_obs``, ``seq_num``
   * - ``visit1_quicklook``
     - ``visit_id``
     - ``day_obs``, ``seq_num``
   * - ``ccdexposure``
     - ``ccdexposure_id``
     - ``day_obs``, ``seq_num``, ``detector``
   * - ``ccdexposure_camera``
     - ``ccdexposure_id``
     - ``day_obs``, ``seq_num``, ``detector``
   * - ``ccdexposure_quicklook``
     - ``ccdexposure_id``
     - ``day_obs``, ``seq_num``, ``detector``
   * - ``ccdvisit1``
     - ``ccdvisit_id``
     - ``day_obs``, ``seq_num``, ``detector``
   * - ``ccdvisit1_quicklook``
     - ``ccdvisit_id``
     - ``day_obs``, ``seq_num``, ``detector``
   * - ``exposure_flexdata``
     - ``obs_id`` (with ``key``)
     - ``day_obs``, ``seq_num``, ``key``
   * - ``ccdexposure_flexdata``
     - ``obs_id`` (with ``key``)
     - ``day_obs``, ``seq_num``, ``detector``, ``key``
   * - ``exposure_flexdata_schema``
     - ``key``
     - ``key``
   * - ``ccdexposure_flexdata_schema``
     - ``key``
     - ``key``

The ``efd_*`` schemas follow the same pattern for their two summary tables. Their unpivoted tables
have no single-column key, because a row there is identified by a property and field within an
exposure or visit rather than by the exposure or visit alone.

.. list-table:: Keys in the ``efd_*`` schemas
   :header-rows: 1
   :widths: 32 24 44

   * - Table
     - Single-column key
     - Declared primary key
   * - ``exposure_efd``
     - ``exposure_id``
     - ``day_obs``, ``seq_num``
   * - ``visit1_efd``
     - ``visit_id``
     - ``day_obs``, ``seq_num``
   * - ``exposure_efd_unpivoted``
     - none
     - ``day_obs``, ``seq_num``, ``exposure_id``, ``property``, ``field``
   * - ``visit1_efd_unpivoted``
     - none
     - ``day_obs``, ``seq_num``, ``visit_id``, ``property``, ``field``

The single-column primary keys should be considered deprecated. Prefer the multi-column primary keys
when you design your database queries. The single-column keys may be phased out at a future date.
As of schema version 1.9.0 these columns are no longer declared as primary keys; they are kept as
unique constraints, so they still identify a row and still carry an index.

.. note::

   The three unused ``cdb_startracker*`` schemas are the exception to all of the above. They have no
   ``day_obs``/``seq_num`` primary key, and ``exposure_id`` remains the declared primary key of their
   ``exposure`` and ``exposure_quicklook`` tables. These schemas are currently unused.

When you use Consolidated Database, you will often need to combine data from different tables using
a **JOIN** operation. The **JOIN** is a very common tool used with databases that combines multiple
tables into one. Here is an example of a join of two tables:

.. code-block::

    SELECT e.day_obs, e.seq_num, e.exp_time, q.mount_jitter_rms
    FROM cdb_lsstcam.exposure AS e
    JOIN cdb_lsstcam.exposure_quicklook AS q
        ON e.day_obs = q.day_obs AND e.seq_num = q.seq_num
    WHERE e.day_obs = 20250421
    LIMIT 10;

Let's break this down:

 * The line with ``SELECT`` identifies which columns we want to get from our query.
 * The line with ``FROM`` specifies the first table that will be included in our query. In this
   case, the first table is ``cdb_lsstcam.exposure``, which we are giving the alias ``e`` for
   convenience.
 * The ``JOIN`` line adds the ``cdb_lsstcam.exposure_quicklook`` table to the query, gives this
   table the alias ``q``, and specifies how to match up the lines in this table with the rest of the
   results, with the ``ON`` clause. **This is an essential part of the query** because it is what
   limits the result to matching rows. A join with no condition returns every combination of rows
   in the two tables — far more than expected, and a excessive load on the database server.
 * The ``WHERE`` line limits the results to the specified criteria. In this case, only rows from the
   night of 21 April 2025 will be returned. 
 * The ``LIMIT`` line tells the server to return no more than 10 rows. If more than 10 matches are
   available, the database will only send the first 10 it finds.

``exposure`` and ``ccdexposure``
--------------------------------

These tables are supplied from the camera header service CSC for each camera. All of the other
tables in the database make reference to the keys in these tables. If a row is present in any table
in the database, it is guaranteed that there will be a corresponding row in the ``exposure`` or
``ccdexposure`` table. Because the data in these tables come from the header service, none of the
information in these tables is in any way based on the content of the images.

These two tables also exist as copies in the form of the ``visit1`` and ``ccdvisit1`` tables (which
are actually *views* rather than *tables* within the database). If the visit and exposure
equivalence were broken in the Rubin survey, these two tables would differ. As long as the
equivalence holds, you can reliably expect that the data in each of these tables are equivalent to
its counterpart.


Rapid Analysis tables
---------------------

These tables are supplied by Rapid Analysis, which processes images shortly after they are taken.
The visit-level measurements are held in ``exposure_quicklook`` and ``visit1_quicklook``, and the
CCD-level measurements in ``ccdexposure_quicklook`` and ``ccdvisit1_quicklook``. Each of these
tables refers back to the keys in the ``exposure`` or ``ccdexposure`` table. In contrast to the
header service tables, every value in these tables is derived from the content of the images.

Unlike ``visit1`` and ``ccdvisit1``, all four of these are ordinary tables rather than views, and
the exposure-level and visit-level tables are not copies of one another; apart from the key columns,
``exposure_quicklook`` and ``visit1_quicklook`` hold entirely different quantities, as do
``ccdexposure_quicklook`` and ``ccdvisit1_quicklook``. A row is present only once Rapid Analysis has
processed the corresponding image, so an exposure may have no quicklook row at all, and a query
joining these tables to ``exposure`` will drop such exposures unless it uses an outer join.


Flexible metadata tables
------------------------

These tables hold key/value data that needs to be added quickly and is not expected to be needed
permanently. The values are held in ``exposure_flexdata`` at the visit level and
``ccdexposure_flexdata`` at the CCD level, one row per observation and key, with the value stored as
text. Each key must first be registered in the corresponding ``exposure_flexdata_schema`` or
``ccdexposure_flexdata_schema`` table, which records the key's name, its data type, and optionally a
documentation string, a unit, and an IVOA UCD. Reading a value therefore means consulting the schema
table to learn how the text should be interpreted.

Because these tables are replicated from the Summit to the USDF, rows should only ever be written at
the Summit. They are intended for experimental, investigatory, or debugging values, and should not
be used for anything taking part in an automated control loop. See :doc:`this page
<flexible-metadata>` for the REST API used to define keys and insert values.

.. note::

   As of September 2026, no system writes to the flexible metadata tables.


Sky regions
-----------

For an on-sky image, ``exposure`` and ``ccdexposure`` hold the footprint of the image in two forms.
``s_region`` is an IVOA polygon string in degrees, suitable for display and for TAP clients.
``pgs_region`` is a `pgSphere <https://pgsphere.github.io/>`__ polygon in radians, which the database can index and search.
Both columns are null for images that are not of type ``OBJECT``.

``pgs_region`` is the only spatial index in ConsDB.
Use it with the pgSphere operators for a spatial search, for example to find the LSSTCam exposures whose footprint contains a point:

.. code-block:: sql

    SELECT day_obs, seq_num, band
    FROM cdb_lsstcam.exposure
    WHERE pgs_region @> spoint(radians(150.1), radians(2.2))
      AND day_obs BETWEEN 20250401 AND 20250430;

The ``pgs_region`` column is not in the schema browser.
It is a *shadow column*, added outside the schema files, and meant primarily for the ``consdbtap`` service, although PostgreSQL users can also take advantage of it.
The :doc:`../developer-guide/alembic` page explains how it is added.

Writing efficient queries
-------------------------

The database is indexed on the primary keys, the unique keys, and the foreign keys given above, and
on nothing else.  A query that filters on ``day_obs``, or on ``day_obs`` and ``seq_num``, uses an
index and is fast even on the largest tables.  A query that filters only on another column, such as
``band`` or ``exp_time``, reads the whole table.  When testing a new query, it may be helpful to put
a ``day_obs`` range in the query for testing. **Always** put both ``day_obs`` and ``seq_num`` (and
``detector`` at the CCD level) in every ``JOIN`` condition.

A CCD-level table has about 200 rows for each LSSTCam exposure. A join between an exposure-level
table and a CCD-level table without a filter returns about 200 rows for each exposure in the range,
so results from such queries can easily become very large. If you can get the information you need
without relying on CCD-level tables, this will make your queries more efficient.

Versioning
==========

ConsDB schemas follow the versioning guidelines of the ``sdm_schemas`` repository, together with the
rules recorded there for the ``cdb_*`` schemas specifically.

Each schema carries its own internal version, declared at the top of its YAML file. This version
tracks changes to that schema alone; it is distinct from the tags and versions of ``sdm_schemas``
itself, and each ConsDB schema is versioned independently of the others. The version is written with
three numbers in the format ``MAJOR.MINOR.PATCH``, such as ``1.2.3``, and may need to be updated
when the schema changes.

The following guidelines are used when incrementing the version:

- Different ``MAJOR`` versions are incompatible.
- Different ``MINOR`` versions are backward compatible.
- Different ``PATCH`` versions are completely compatible.

The current version of each schema is at the top of its YAML file (linked from the list of schemas above) and on the schema browser page for that schema.
The database itself does not record this version.
It records only the Alembic revision of each schema, in the ``cdb.<schema>_version`` table.

These suggestions need not be followed strictly, and there may be exceptions. Where the
ConsDB-specific rules below differ from them, the rules below govern.

For the ConsDB schemas, versioning is defined with respect to two kinds of client: consuming
clients, which only read, and producing clients, which write only their own tables. A client that
works with one version of a schema should continue to work with any later version that has not
changed its ``MAJOR`` number.

These guidelines cover the changes most often made to a ConsDB schema:

.. list-table::
   :header-rows: 1
   :widths: 30 18 52

   * - Operation
     - Increment
     - Notes
   * - Add table
     - ``MINOR``
     - All existing clients continue to operate normally; an updated producer may write to the new
       table.
   * - Add column with default
     - ``MINOR``
     - Existing clients continue to operate normally.
   * - Add column without default
     - ``MINOR``
     - The producing client must be updated, but all others continue to operate normally. This
       stretches semantic versioning slightly in order to avoid a major version change.
   * - Remove column or table
     - ``MAJOR``
     - Consuming clients, and the client that produced the object, can no longer use it and must be
       upgraded.
   * - Change column or table name
     - ``MAJOR``
     - Equivalent to a removal followed by an addition.
   * - Change column type
     - ``MAJOR`` or ``PATCH``
     - May or may not be transparent, so it can be either incompatible or fully compatible.
   * - Add index
     - ``PATCH``
     - Fully backward compatible.
   * - Change object metadata
     - ``PATCH``
     - Does not affect the database schema, but does affect how it is presented to the user.
