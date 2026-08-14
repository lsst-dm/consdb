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

- Argo-CD, to deploy the Phalanx applications and to read the pod logs.
- LOVE, to take a test image at a test stand.
- Felis and Alembic, to apply a schema migration.
- ``psql`` or ``pgcli``, to run the migration and to check the result.

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

Test the Alembic migration and the code at the TTS or the BTS before you deploy at the Summit.
The :doc:`schema-migration-process` page gives the test procedure.

The steps that deploy at the Summit are the same as the steps that test at a test stand.
The observers and the site teams must agree to the work.
The Summit OpenVPN gives access to the Argo-CD deployments.

Coordinate with the Summit before you deploy.
Some changes need a time window when the cameras are not in use.
To ask for a time window, write in the ``#summit-control-room`` Slack channel.
Put ``@os-day-shift`` in your message.

Announce your intention in the ``#recap-software`` and the ``#summit-announce`` Slack channels.
The announcement in ``#recap-software`` is for information only.
The versioning board does not have to approve the migration.
Put the DONE stamp on each announcement when the migration is complete.

The `channel usage guide <https://obs-ops.lsst.io/Communications/slack-channel-usage.html>`__
gives the function of each Slack channel.

USDF Deployment Steps
^^^^^^^^^^^^^^^^^^^^^

A migration at the USDF must happen in synchrony with the same migration at the Summit, with the replication paused between the two.
Steps 7 to 9 of the :doc:`schema-migration-process` page give the sequence.
This page does not repeat it.

If the change has no effect on the Summit, apply the Alembic migration at the USDF and test it.

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


To learn which version is deployed at a site, read the ``version`` field of the root endpoint, or the image tag in the Phalanx values file of that environment.

HInfo Service
=============

The ``hinfo`` service retrieves primary keys and associated values from HeaderService output metadata and inserts them into the appropriate tables in ConsDB.

It is only deployed in Phalanx at the Summit.

Deployment and maintenance of this service is the same as for any other `Phalanx application <https://phalanx.lsst.io/developers/index.html>`__.

TAP Service
===========

The ``consdbtap`` service is a Phalanx application at the USDF only.
Its schema comes from a TAP schema container built from ``sdm_schemas``.
After a migration, that container must be rebuilt and deployed before the new columns appear in TAP.
Step 12 of the :doc:`schema-migration-process` page gives this.

Daily Consistency Check
=======================

A scheduled job at the USDF runs the image described on the :doc:`../developer-guide/building-artifacts` page once each day.
The :doc:`monitoring` page gives what it checks and how it reports.

Transformed EFD
===============

The Transformed EFD runs at the USDF only, from the ``slaclab/usdf-consdb-deploy`` repository rather than from Phalanx.
The :doc:`transformed-efd` page gives its deployment.
