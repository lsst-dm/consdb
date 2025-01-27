########
Schemas
########

Types of schemas
================
Summit for observers and Summit systems
---------------------------------------
Summit schemas are the smallest. They should contain primary key information from HeaderService and additional information from other Summit systems, including experimental and engineering data.

USDF for staff and analytical uses
----------------------------------
USDF schemas are the largest. They contain a full replica of the Summit schemas plus additional information from USDF systems.
These other systems include Prompt Processing and Data Release Production, possibly Calibration Products Production, and human annotations from processing campaigns.

Release for science users
-------------------------
* Near-real-time "prompt" ConsDB replicates a subset of the USDF version
* Data Release (DR) ConsDB is a snapshot of a subset of the USDF version with data pertaining to the exposures/visits in the DR

Schema browser
==============

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
