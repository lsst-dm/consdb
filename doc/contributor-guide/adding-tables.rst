##############
Adding Tables
##############

Design rules
============

- Each source of data should have its own table(s).
- Conversely, each new table being added should have its data source identified.
- Each dimension combination (exposure, visit, exposure+detector, visit+detector, etc.) should have its own table(s).
- Normalize when possible.  Try not to repeat non-key columns between tables with the same dimensions.
- De-normalize via views to make querying easier.

Requirements of the services
============================

The services make assumptions about every table in a ``cdb_*`` schema.
A new table must satisfy them.

- The table has ``day_obs`` and ``seq_num`` columns, and ``detector`` at the CCD level, and these form its primary key.
  The insert endpoints of the REST API refuse a table without a ``day_obs`` column.
- The table has a foreign key to ``exposure`` or ``ccdexposure`` on those columns.
  The consistency checks and the replication depend on this.
- The single-column key (``exposure_id`` or ``ccdexposure_id``) is present as a unique column, for the clients that still use it.
  The :doc:`../user-guide/schemas` page gives the pattern.
- The ``usdf`` and ``oods`` roles get ``SELECT`` on the table.
  The Alembic environment adds these grants to each generated migration.

Procedure
=========

A new table follows the same procedure as a new column.
The :doc:`adding-columns` checklist gives the ticket, the reviews, and the ``sdm_schemas`` pull request.
The :doc:`../operator-guide/schema-migration-process` page gives the migration and the deployment.
Two steps differ for a table:

- The migration must add the grants and the foreign keys.
  Read the generated migration for both before you test it.
- If the table joins to ``exposure`` or ``ccdexposure`` for a view, the view must be written by hand.
  Alembic does not generate views, and it does not compare them.
  The :doc:`../developer-guide/alembic` page explains how the ``visit1`` and ``ccdvisit1`` views are maintained.

The data source can begin to write when the migration is deployed and ``pqserver`` has been restarted.
The :doc:`inserting-information` page gives the ways to write.
