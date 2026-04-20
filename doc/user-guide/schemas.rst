#######
Schemas
#######

ConsDB is a relational database and uses schemas expressed in SQL.

The `Science Data Model Schemas site <https://sdm-schemas.lsst.io>`__ provides a web-based browser for ConsDB schemas, including Summit-generated schemas and Transformed EFD schemas.
All ConsDB schemas (one per instrument) are labeled as "ConsDB" or "Transformed EFD" on that site.

There are currently four main schemas: ``cdb_latiss``, ``cdb_lsstcam``, ``efd_latiss``, and ``efd_lsstcam``.

Each ``cdb_*`` schema has ``exposure`` and ``visit1`` tables; the ``visit1`` tables are using the one-to-one visit system (each exposure is a visit) and hence are cheaply implemented as views, although formally visits should only include on-sky exposures.
Each schema also has a ``ccdexposure`` table and ``ccdvisit1`` view for per-CCD values.

There is a ``ccdexposure_camera`` table for certain values the Camera Control System is responsible for.
``visit1_quicklook`` and ``ccdvisit1_quicklook`` tables are used to hold outputs from Rapid Analysis.
Additional tables can be added for metadata coming from other sources.
Multiple sources should not be combined in one table; this makes replication and back-filling simpler.

Finally, flexible metadata tables named ``exposure_flexdata`` and ``ccdexposure_flexdata`` are available to hold key/value information on a temporary or experimental basis.
(Visit flexdata can be added if there is a need.)
See :doc:`this page <flexible-metadata>` for more on flexible metadata.

The ``efd_*`` Transformed EFD tables, which have their own schemas, are described in :doc:`a separate page <transformed-efd>`.

Generally the tables within each schema are normalized so that there is minimal duplication of data other than exposure/visit identifiers between tables.
This may mean that a join is needed to get the desired information or to query on columns in more than one table.
Primary keys, unique keys, and foreign keys are defined to provide indexes for common queries and to speed up those joins.


Types of schemas
================

Summit for observers and Summit systems
---------------------------------------
Summit schemas may not have all tables populated.
They should contain primary key information from HeaderService and additional information from other Summit systems, including experimental and engineering data.

USDF for staff and analytical uses
----------------------------------
USDF schemas should be fully populated.
They contain a full replica of the Summit schemas plus additional information from USDF systems.
These other systems will grow to include Prompt Processing and Data Release Production, possibly Calibration Products Production, and human annotations from processing campaigns.

Release for science users
-------------------------
As of 2026-03, DM has decided that ConsDB will be internal-only, although information from it may be copied to Data Services for release to science users.

Use of a snapshot of ConsDB as an input to Data Release Production is contemplated but not yet implemented.


Versioning
==========

(https://rubin-obs.slack.com/archives/C07QJMQ7L4A/p1730482605167509)

- Schemas are using semantic versioning
- Should be consistent across all schemas, not just ConsDB

major: backward incompatible changes to the database objects (adding a table, deleting a column)
- except adding a table is not backwards incompatible

minor: backward compatible changes to the database objects (adding a column)
patch: updates or additions to semantics/metdata (units, UCDs, etc.)
- changing units can create incompatibilities

And we should say what should happen in the case of changes to primary/foreign keys.
- Semantic neutrality: becoming non-primary is unique and anything becoming primary was already unique

  - or there can be ones that are not neutral.

Think about the utility of these versions in terms of interaction with the ConsDB APIs, migrations, etc.

Do sdm_schemas versions appear in the db?

Currently the schemas are tagged and versioned as a set, at least w.r.t. the Science Platform.
So once ConsDB is available in TAP, it should be part of that set.

What do users see, how does TAP play into this, do the schema need this type of micro versioning?

- Services/cosndb repo versioning strategy - services of monthly YY.0M.DD
