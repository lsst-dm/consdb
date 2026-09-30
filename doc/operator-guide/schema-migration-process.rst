########################
Schema Migration Process
########################

This page gives the procedure that changes a ConsDB schema.
Do the steps in the given sequence.

This page applies to a data source at the Summit.
The Header Service and Rapid Analysis are the Summit data sources at this time.

If the data source is at the USDF, use the :doc:`../contributor-guide/transformed-efd` page instead.
The Transformed EFD is the only USDF data source at this time.

Before you start
================

Read the :doc:`../developer-guide/alembic` page once.
It gives the layout of the migrations: one tree for each schema, one version table for each tree in the ``cdb`` schema, and the ``-n`` option that selects a tree.

Collect this information in a Jira ticket:

- The names of the columns that you add.
- The source of the data. The source controls which tables receive the columns.
- The description, the unit, and the UCD of each column, if you have them.

One data source must fill each table.
One data source can write to more than one table.
Give each table a name that has a meaning for science users.
The name can also show the data source.

Step 1 — Make the pull request in sdm_schemas
=============================================

Make a pull request with the schema change in `lsst/sdm_schemas <https://github.com/lsst/sdm_schemas>`__.
Obey all the procedures of that repository.

Get these approvals:

- A member of the Data Engineering team approves the syntax, the column names, and the descriptions.
- The ConsDB Product Owner, or a designate, approves the usefulness and the absence of duplication.
- A member of the ConsDB team approves the table name, the agreement with the data source, and the maintainability.
- The maintainer of the data source for the target table approves the plan for the change.

.. important::

   Do not merge this pull request now.
   Step 13 merges it, after the migration is complete in all the environments.

If you have more than one ``sdm_schemas`` pull request, you can rebase them onto each other.
The last pull request then contains all the changes, and one migration is sufficient.
You can also make a separate migration for each pull request.

Step 2 — Generate the migration
===============================

Set ``SDM_SCHEMAS_DIR`` to a checkout of the ``sdm_schemas`` branch of your pull request.
Then run the ``alembic-autogenerate.py`` script from the top directory of the ``consdb`` repository.
Give a revision message as the argument:

.. code-block:: bash

   python alembic-autogenerate.py DM-12345 add the new columns

Commit the new migration files to a ticket branch of ``consdb``.

With no ``--instrument`` option, the script makes a revision in each of the four instrument trees that are in use.
For a change to an ``efd_*`` schema or to ``efd_scheduler``, give ``--instrument`` with the name of that tree.

.. note::

   The "Generate migration scripts" GitHub Action runs the same script.
   It makes a draft pull request with the result.
   The :doc:`../developer-guide/building-artifacts` page gives more about this workflow.

Step 3 — Edit the migration
===========================

The script cannot make a correct migration without your help.
Read the result and correct these three items:

- **The views.**
  The script deletes the ``visit1`` and ``ccdvisit1`` views and makes them again.
  Keep this part only if the ``exposure`` table or the ``ccdexposure`` table changes.
  If those tables do not change, delete this part from the ``upgrade`` function and from the
  ``downgrade`` function.
- **The constraints and the column names.**
  Make sure that the constraints are correct.
  Make sure that a renamed column is correct.
- **The other schemas.**
  The script makes one revision file in the ``versions/`` directory of each tree that it processes.
  Delete the files in the trees whose schema does not change.

Step 4 — Test the migration
===========================

Use the validation script:

.. code-block:: bash

   python tests/validate_schema_migrations.py --instrument latiss

The script does three tests:

1. It runs ``alembic-autogenerate.py`` again.
   A correct migration gives an empty result.
   Other output shows that a difference between the migration and the YAML files stays.
2. It starts a temporary PostgreSQL instance.
   It then upgrades to the revision before your migration, upgrades to your migration, and
   goes back one revision.
   It compares the database with the YAML files at each point.
3. It does two full upgrade and downgrade cycles against a live database.
   This test runs only if you set ``CONSDB_URL``.

The script needs two copies of ``sdm_schemas``:

- The new copy, with your change.
  The script reads ``SDM_SCHEMAS_DIR``, or you can give ``--sdm-schemas-dir``.
- The old copy, without your change.
  The script reads ``consdb/sdm_schemas-old``, or you can give ``--sdm-schemas-old-dir``.

If a test fails, the script exits with status 1 and writes the file ``validate_schema_debug.json`` next to the repository root.
This file contains the differences that the script found.
The :doc:`../developer-guide/alembic` page gives how to read it.
Add ``--keep-delete-me`` to keep the empty revision that the first test generates, if you want to read it.

.. warning::

   Point ``CONSDB_URL`` at a local database that you can lose.
   Never point it at the BTS, the TTS, the USDF, or the Summit.

Step 5 — Migrate a test stand
=============================

Apply the migration at the Base Test Stand (BTS) or the Tucson Test Stand (TTS):

1. Use ``psql`` or ``pgcli`` to make sure that the tables that you upgrade are present.
2. Go to the ``consdb/`` directory, where the ``alembic.ini`` file is.
   Then upgrade the database:

   .. code-block:: bash

      alembic upgrade head -n <database name>

If you must deploy a new ``hinfo`` container for the new schema:

1. Make a branch in ``phalanx``.
   Edit the environment file ``phalanx/applications/consdb/values-<test stand>.yaml`` to point to
   the Docker image of your branch (``tickets-DM-###``).
2. Announce in the applicable Slack channel that you start your tests.
3. Set the ``Target Revision`` of the ConsDB deployment in ``<url.to.teststand>/argo-cd`` to your
   ``phalanx`` branch.
   Refresh the application and read the pod logs.

Restart the ``pqserver`` deployment, because it reads the schema at start.

Then do these tests:

- Read the schema and make sure that it is correct.
- If ``hinfo`` changed, take an image.
  Then make sure that the correct data is in the database.
- For a different data source, do an integrated test with a new version of that data source.

The `TTS Start Guide <https://rubinobs.atlassian.net/wiki/spaces/LSSTCOM/pages/53739987/Tucson+Test+Stand+Start+Guide>`__
gives more about the test stands.

Take a test image with LATISS
-----------------------------

Open LOVE at ``<url.to.teststand>/love``.
Sign in with the 1Password admin information, or with your Summit user name and password.
Then go to the ATQueue, which is the Auxiliary Telescope (AuxTel) Script Queue.

.. note::

   Record the start configuration of each script before you edit it.
   You return each script to that configuration at the end of this procedure.

Take a simulated image with LATISS through the ATQueue.
Use these three scripts:

1. ``set_summary_state.py``.
   Change the configuration to set ATHeaderService and ATCamera to ENABLED.
2. ``enable_latiss.py``.
   Remove the configuration that is present.
3. ``take_image_latiss.py``.
   Change the configuration to keep ``nimages`` (1) and ``image_type``
   (BIAS, DARK, or FLAT) only.

Put the three scripts in the queue.
Then click ``run``.

Look for errors in the Script Queue, in the Argo-CD ConsDB pod logs, and in the ``hinfo-latiss``
deployment.
Correct each error and do the test again.

Read the database with ``psql``.
The ``\dt`` command shows the table names.
This command shows the most recent data:

.. code-block:: sql

   SELECT * FROM cdb_latiss.exposure WHERE day_obs = <YYYYMMDD>;

Then run ``set_summary_state`` to set ATHeaderService and ATCamera back to STANDBY.
Set LATISS back to STANDBY.
Return the three scripts to their start configurations.

.. warning::

   Do not continue to the Summit if you found an error.
   Correct the error first.
   Then point your ``phalanx`` branch at your corrected ``consdb`` branch and test again.

After a successful test
-----------------------

1. Merge the ``consdb`` pull request that contains the Alembic migration.
2. Tag the release. The :doc:`../developer-guide/standards-practices` page gives the rules.
3. Change your ``phalanx`` branch to point the deployments at this ``consdb`` tag.

You can test the test stand again at this point.
The pull request did not change, so this test is short.

Step 6 — Coordinate with the Summit and announce
================================================

Coordinate with the Summit before you deploy to the production systems.
Some changes need a time window when the cameras are not in use.
Decide if your change needs such a window.

To ask for a time window, write in the ``#summit-control-room`` Slack channel.
Put ``@os-day-shift`` in your message.

Announce your intention in these two Slack channels:

- ``#recap-software``.
  This announcement is for information only.
  The versioning board does not have to approve the migration.
- ``#summit-announce``.

Step 7 — Disable the subscription at the USDF
=============================================

Connect to the USDF database with ``psql``.
Then stop the logical replication from the Summit:

.. code-block:: sql

   ALTER SUBSCRIPTION usdf_exposurelog DISABLE;

Step 8 — Apply the migration
============================

Apply the migration at the Summit first, and then at the USDF.
The Summit database is the publisher, and the USDF database is the subscriber.

At each site, connect to the database and run the Alembic upgrade:

.. code-block:: bash

   alembic upgrade head -n <database name>

The `df-ops procedure <https://df-ops.lsst.io/usdf-applications/qa/summit-db-replica/procedures.html#schema-updates-consdb>`__
gives more about the Summit database and the replica.

Step 9 — Enable the subscription
================================

Start the logical replication again at the USDF:

.. code-block:: sql

   ALTER SUBSCRIPTION usdf_exposurelog ENABLE;
   ALTER SUBSCRIPTION usdf_exposurelog REFRESH PUBLICATION;

The second command gets the new tables and columns from the publication.
The subscription does not copy the new columns without it.

Then check the data at the USDF, as you agreed with the ConsDB team.

Step 10 — Complete the announcements
====================================

Put the DONE stamp on each of your Slack announcements.

Step 11 — Restart pqserver
==========================

Restart ``pqserver`` in all the environments, because it reads the schema at start.

The new schema is now in the database and in ``pqserver``.
The data sources can fill it for new exposures.
You can also fill it for exposures from the past.

Step 12 — Update the TAP schema
===============================

Make sure that a new version of the TAP Schema container for the ``consdbtap`` service is available.
The container is built from the ``sdm_schemas`` repository.
Deploy that container to all the environments.

Until this step is complete, the new columns are visible through SQL and the REST API but not through TAP.

Users can now see the new schema in their queries.

Step 13 — Merge the sdm_schemas pull request
============================================

Merge the pull request from step 1.
The new schema is now visible in the schema browser.

Rolling back
============

Each revision has a ``downgrade()`` function, and the validator in step 4 checks that it undoes ``upgrade()``.
To roll back at one site:

.. code-block:: bash

   alembic downgrade -1 -n <database name>

Roll back at both the Summit and the USDF, with the replication paused as in steps 7 to 9, or the two databases will differ and the replication will fail.
Restart ``pqserver`` afterwards, as in step 11.
Data written to a new column since the upgrade is lost.
