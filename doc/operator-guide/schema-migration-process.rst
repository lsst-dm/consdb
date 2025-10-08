########################
Schema Migration Process
########################

Gather information
==================

Gather the following information in a Jira ticket:

- Names of columns to be added
- Source of information for the columns, which will help determine the tables to which the columns will be added
- If possible, descriptions, units, and UCDs for the columns, ideally via a PR to sdm_schemas

Each table in the ConsDB schema should be filled by a single data source (e.g. the ``hinfo`` service at the Summit or Rapid Analysis).
Each data source can write to multiple tables.
The name of each table can be related to the name of the data source, but it's best for it to be something meaningful to science users.

Get approvals
=============

- Get the ``sdm_schemas`` PR approved as to syntax, column naming, and description content by a member of the Data Engineering team.
- Get the ``sdm_schemas`` PR approved as to usefulness and non-redundancy by the ConsDB Product Owner or designate.
- Get the ``sdm_schemas`` PR approved as to table name, agreement with data source, and maintainability by a member of the ConsDB team.

If the data source is at the USDF (currently only the Transformed EFD), follow the process in Transformed EFD Contributor Guide (transformed-efd.rst).
If the data source is at the Summit (currently the Header Service or Rapid Analysis), follow this process.

Create the schema migration in lsst-dm/consdb
=============================================

If there is more than one ``sdm_schema`` PR being requested, you can rebase them onto each other such that the last one contains all previous ones to simplify deployment (but you can also do each one as a separate migration).

Build an Alembic migration based on the desired PR branch.
The "Generate migration scripts" GitHub Action in ``lsst-dm/consdb`` can be used to generate this.
There are some manual steps that need to occur:

- Remove view drop/creates from both upgrade and downgrade if the ``exposure``/``ccdexposure`` tables are not being modified.  On the other hand, make sure they're present if those tables are being modified.
- Ensure constraints and renamed columns are correct.
- Remove any migrations for schemas that are not actually changing.

Apply and test the migration at BTS
===================================

If the data source is at the Summit, apply the migration at the Base Test Stand (BTS) using this procedure:

1. Verify the tables that you will be upgrading exist using ``psql`` or ``pgcli``.
2. From the ``consdb/`` directory, (where the ``alembic.ini`` file is) use the alembic commands to upgrade the existing database tables: ``alembic upgrade head -n <database name>``

If the data sources is at USDF, apply the migration to the ``dev`` database and test with the ``usdf-rsp-int`` environment.

If you need to deploy a new ``hinfo`` container to write to the new schema:

1. Create a branch in ``phalanx`` and edit the corresponding test stand environment file ``phalanx/applications/consdb/values-<test stand>.yaml`` to point to your branch's built docker image (tickets-DM-###).
2. Coordinate and announce in the appropriate Slack channel that you will begin testing your migrations.
3. Update the ConsDB deployment in ``<url.to.teststand>/argo-cd`` to use your ``phalanx`` branch in the ``Target Revision``. Refresh and check pod logs.

You will need to restart the ``pqserver`` deployment in order to pick up the new schema.

Test:

- Hand-check the schema to make sure it looks correct.
- If ``hinfo`` changed, take an image and check that the right data is written to the database.
- For other data sources, try to do an integrated test with a new version of that data source.

See `TTS Start Guide <https://rubinobs.atlassian.net/wiki/spaces/LSSTCOM/pages/53739987/Tucson+Test+Stand+Start+Guide>`__ for guidelines on using the test stands.

Access LOVE via ``<url.to.teststand>/love`` and use the 1Password admin information to sign in, or your Summit username and password.
Navigate to the ATQueue or Auxiliary Telescope (AuxTel) Script Queue.

.. note::

  Before editing these scripts, note their starting configurations, as we will return the scripts to this configuration when we are done.

Take a test/simulated picture with LATISS through the ATQueue using these three scripts:

1. ``set_summary_state.py`` Change the configuration to set ATHeaderService and ATCamera to ENABLED.
2. ``enable_latiss.py`` Remove any existing configuration.
3. ``take_image_latiss.py`` Update the configuration to remove anything that is not 'nimages' (1) and 'image_type' (BIAS or DARK or FLAT)

Once you have put these three scripts in the queue, click ``run``.
Watch for errors in both the Script Queue and the Argo-CD ConsDB pod logs and ``hinfo-latiss`` deployment.
Address any errors and retest.

Check the database by using ``psql`` commands like ``\dt`` to display the table names and maybe even ``SELECT * from cdb_latiss.exposure where day_obs == <YYYYMMDD>;`` to view the most recent data.

Run ``set_summary_state`` to set ATHeaderService and ATCamera back to STANDBY, and return LATISS back to STANDBY.
Then return these three scripts to their original configurations.

If you have encountered errors in this process, do not proceed to the summit, but address those errors and retest them with your ``phalanx`` branch pointing to your ConsDB branch with the fix to these errors.

If tests are successful, merge the ConsDB PR containing the Alembic migration.
Tag the release according to ``standards-practices`` guidelines.
Update your existing ``phalanx`` branch to point the environment based deployments to this ConsDB tag.

You are able to retest on the test stand at this point; hopefully there were no changes to your ConsDB pull request so this step is trivial.

Migrate the Summit and update logical replication
=================================================

Follow the process in https://df-ops.lsst.io/usdf-applications/qa/summit-db-replica/procedures.html#schema-updates-consdb to update the Summit and USDF databases.

Restart pqserver
================

Restart ``pqserver`` in all environments to pick up the new schema.

The new schema is now visible in the database and ``pqserver`` and can start to be filled in for new exposures as well as back-filled as needed.

Update TAP Schema
=================

Make sure that a new version of the TAP Schema container for the ``consdbtap`` service has been generated.
Deploy that to all environments.

The new schema is now visible for user queries.

Merge the sdm_schemas PR
========================

The final step is to merge the PR in ``sdm_schemas``.
This makes the new schema visible in the schema browser.
