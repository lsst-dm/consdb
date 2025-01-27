###########
Deployment
###########

Database
========

Deployments of the Consolidated Database are currently located at

-  Summit
-  USDF (+ dev, use the same underlying database, a replication of Summit)
-  Base Test Stand (BTS)
-  Tucson Test Stand (TTS)

Updates to these deployments may be needed when there are edits to the schema for any of the cdb_* tables defined in <link to> sdm_schemas.

Tools:
------

- Argo-CD
- LOVE
- Felis

Repositories:
-------------

- `phalanx <https://github.com/lsst-sqre/phalanx>`__
- `sdm_schemas <https://github.com/lsst/sdm_schemas>`__
- `consdb <https://github.com/lsst-dm/consdb>`__

Access needed:
--------------

- NOIRLab VPN
- Summit VPN
- USDF

Process:
--------


Deploy code to populate db at Summit and/or USDF
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Follow the testing steps above for testing alembic migration and code at TTS/BTS, before the you consider deploying at the summit.

The steps to deploy at the summit mirror the steps to test on a test stand with coordination and permission from the observers and site teams.
Access to argo-cd deployments is available via the Summit OpenVPN.
To coordinate your deployment update on the summit, you must attend Coordination Activities Planning (CAP) meeting on Tuesday mornings and announce your request.

Add your migration intentions to the CAP SITCOM confluence agenda `here <https://rubinobs.atlassian.net/wiki/spaces/LSSTCOM/pages/53765933/Agenda+Items+for+Future+CAP+Meetings>`__

The CAP members may tell you a time frame that is acceptable for you to perform these changes.

They may also tell you specific people to coordinate with to help you take images to test LATISS and LSSTCOMCAMSIM tables. There will be more tables to test eventually.

Channels to note: #rubinobs-test-planning; #summit-announce; #summit-auxtel, and `channel usage guide  <https://obs-ops.lsst.io/Communications/slack-channel-usage.html>`__.

When you get your final approval and designated time to perform the changes to ConsDB, announce on #summit-announce, and follow similar steps as test stand procedure above.

USDF Deployment Steps
^^^^^^^^^^^^^^^^^^^^^

These steps must happen in synchrony with a Summit migration.

1. Disable (pause) SUBSCRIPTION at USDF.
2. Perform the migration at the summit with the steps below.
3. Connect to the USDF database via psql and perform the alembic migration.
4. Check or test as agreed upon with the ConsDB team.
5. Enable and Refresh Subscription at USDF.

If there is no impact or coordination with Summit needed: Run alembic migration at USDF, and test as appropriate.

Summit Deployment Steps
^^^^^^^^^^^^^^^^^^^^^^^

1. Use a branch in ``phalanx`` to point to the ConsDB tag for deployment.
2. Set the Argo-CD application ``consdb's`` target revision to your ``phalanx`` branch.
3. Refresh the ConsDB application and review pod logs.
4. Connect to the summit database via psql and perform the alembic migration.
5. Have an image taken with the observing team, then verify database entries with a SQL query or Jupyter notebook.
6. Check your new entries in the database using a jupyter notebook or SQL query in RSP showing your new image has been inserted to the database as expected.

Once deployment succeeds, set the ``Target Revision`` in Argo-CD back to ``main`` and complete the ``phalanx`` PR for the tested ConsDB tag.


REST API Server
===============