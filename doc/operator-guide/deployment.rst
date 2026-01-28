###########
Deployment
###########

Database
========

Deployments of the Postgres database are currently located at

-  Summit (using ``postgresdb01.cp.lsst.org``)
-  Base Test Stand (BTS) (using ``postgresdb01.ls.lsst.org``)
-  Tucson Test Stand (TTS) (using TBD)
-  USDF

  - production (using ``usdf-summitdb-logical-replica-tx.sdf.slac.stanford.edu``, a logical replica of the Summit version with USDF additions)
  - integration (using TBD, a logical replica of the Summit version with USDF additions)
  - development (using TBD, a standalone test database)

When the Summit schema is migrated to a new version, corresponding migrations need to be applied to the USDF production and integration instances.

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


REST API Service
================

Deployments of the REST API service (``pqserver``) are currently located in Phalanx environments at

-  Summit
-  Base Test Stand (BTS)
-  Tucson Test Stand (TTS)?
-  USDF

  - production in ``usdf-rsp.slac.stanford.edu``
  - integration in ``usdf-rsp-int.slac.stanford.edu``
  - development IN ``usdf-rsp-dev.slac.stanford.edu``

Deployment and maintenance of this service is the same as for any other `Phalanx application <https://phalanx.lsst.io/developers/index.html>`__.


HInfo Service
=============

The ``hinfo`` service retrieves primary keys and associated values from HeaderService output metadata and inserts them into the appropriate tables in ConsDB.

It is only deployed in Phalanx at the Summit.

Deployment and maintenance of this service is the same as for any other `Phalanx application <https://phalanx.lsst.io/developers/index.html>`__.

