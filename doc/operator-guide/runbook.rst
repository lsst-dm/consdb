########
RunBook
########

This page collects what an operator needs in one place.
Each section links to the page that gives the detail.
A `Confluence draft <https://rubinobs.atlassian.net/wiki/spaces/LSSTOps/pages/45665320/Consolidated+Database+ConsDB+Runbook+draft+incomplete>`__ of this runbook also exists.

Overview
========

ConsDB holds metadata about every image that the Rubin Observatory takes: pointing, timing, and instrument state from the image headers, quality measurements from Rapid Analysis, and summaries of the Engineering Facilities Database.
Its design and architecture are documented in `DMTN-227 <https://dmtn-227.lsst.io/>`__.
The :doc:`../user-guide/index` gives the contents and the access methods.

Architecture
============

Systems
-------

.. list-table::
   :header-rows: 1
   :widths: 22 36 42

   * - Component
     - Where it runs
     - Function
   * - PostgreSQL database
     - The Summit, each test stand, and the USDF.
     - Holds the data. The USDF database is a logical replica of the Summit database, with USDF-only additions.
   * - ``hinfo``
     - The Summit and the test stands, in the ``consdb`` Phalanx application.
     - Reads the Header Service files and writes the ``exposure`` and ``ccdexposure`` rows. One deployment for each instrument.
   * - ``pqserver``
     - Every site, in the ``consdb`` Phalanx application.
     - The REST API. Reads the schema at start.
   * - ``consdbtap``
     - The USDF only, as a Phalanx application.
     - The TAP service.
   * - Transformed EFD
     - The USDF only, in the ``usdf-consdb-deploy`` repository.
     - Fills the ``efd_*`` schemas. The :doc:`transformed-efd` page gives it.
   * - Daily consistency check
     - The USDF, as a scheduled job.
     - Checks the tables of the previous night. The :doc:`monitoring` page gives the rules.
   * - Rapid Analysis
     - The Summit and the test stands.
     - Writes the ``*_quicklook`` tables through ``pqserver``. Not operated by the ConsDB team.

Data flow
---------

.. mermaid::

   flowchart LR
      HS[Header Service] -->|Kafka + S3| HI[hinfo]
      HI --> S[(Summit database)]
      RA[Rapid Analysis] -->|REST| PQ[pqserver<br>insert endpoint]
      PQ --> S
      S -->|logical replication| U[(USDF database)]
      EFD[(EFD)] --> TE[Transformed EFD]
      TE --> U
      U --> TAP[consdbtap]
      U --> PQU[pqserver at USDF<br>query endpoint]
      U --> CC[daily consistency check]

Dependencies
------------

- Kubernetes at each site, through Phalanx and Argo CD.
- The Summit Kafka cluster and the LFA S3 buckets, for ``hinfo``.
- The Butler and the EFD InfluxDB at the USDF, for the Transformed EFD.
- The PostgreSQL logical replication from the Summit to the USDF, operated by the USDF database administrators.

Backups and replication
-----------------------

The USDF database administrators operate the Summit database, the replica, and their backups.
The `df-ops procedures <https://df-ops.lsst.io/usdf-applications/qa/summit-db-replica/procedures.html>`__ give the replication.
A schema change must be applied at both ends with the replication paused.
The :doc:`schema-migration-process` page gives the steps.

Access
======

- The Summit and test stand databases are reachable from the network of each site, and their Argo CD instances from the Summit VPN.
- The USDF database is reachable from the SLAC network.
  The REST API and TAP are reachable from outside with a Rubin Science Platform token.
- The read-only ``usdf`` credential is placed in each user's home directory.
  A service that must write requests a credential from the USDF database administrators.
- The :doc:`../user-guide/sql-clients` and :doc:`../user-guide/rest-api-and-clients` pages give the hosts and URLs of each site.

Configuration
=============

- `phalanx <https://github.com/lsst-sqre/phalanx>`__, application ``consdb``: the deployment of ``hinfo`` and ``pqserver`` at every site, and the image tags in use.
- `consdb <https://github.com/lsst-dm/consdb>`__: the code, the migrations, and this site.
- `sdm_schemas <https://github.com/lsst/sdm_schemas>`__: the schemas.
- ``slaclab/usdf-consdb-deploy``: the Transformed EFD deployment.

To learn which version of ``pqserver`` runs at a site, read the ``version`` field of its root endpoint.

To find out the database Alembic schema version, you can use the following query:

.. code-block:: sql

   SELECT * FROM cdb.cdb_lsstcam_version;

You will need to use an account that has SELECT privilege for the ``cdb`` schema, such as ``oods``
on USDF. The string returned by this query can be compared to the history reported by Alembic in the
repository:

.. code-block:: sh

   alembic -n lsstcam history

Monitoring
==========

The :doc:`monitoring` page gives the channels, the checks, and the alerts.

Maintenance
===========

Testing procedures
------------------

First, test changes and schema migrations in the USDF dev environment.
The database in this environment contains only test data, but that data should ideally exercise most corner cases.
When done with tests, restore the database (if necessary) to its normal schema and test content.

Next, "claim" the USDF int environment by informing ConsDB consumers in the ``#consolidated-database`` channel.
Pause the replication from the Summit (and the EFD Transformer if necessary).
Apply any migrations, modifications, and application synchronizations needed.
Test ConsDB services (such as the ``pqserver`` REST API, TAP, and direct SQL access) as well as downstream applications such as the Nightly Digest.
When done, either restore the USDF int environment by backing out any migrations and changes or roll forward as in the next paragraph.

When all testing is successful, roll forward by updating the Summit and USDF production and restoring replication to both USDF production and int, following the procedures in :doc:`schema-migration-process`.

Standard procedures
-------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Task
     - Where
   * - Change a schema
     - :doc:`schema-migration-process`
   * - Deploy a new version of ``hinfo`` or ``pqserver``
     - :doc:`deployment`
   * - Restart ``pqserver`` after a migration
     - Restart the deployment in Argo CD. The service reads the schema at start.
   * - Pause and resume the replication
     - Steps 7 and 9 of :doc:`schema-migration-process`
   * - Re-run the consistency check for one day
     - The ``/table_consistency`` endpoint, on the :doc:`monitoring` page
   * - Fill a new column for images from the past
     - The selective update section of the :doc:`../developer-guide/hinfo` page
   * - Re-run a failed Transformed EFD task
     - :doc:`transformed-efd`

Known issues
============

- The wide views, and with them the per-observation endpoint of the REST API, are not implemented.
  The :doc:`../developer-guide/wide-views` page gives the status.
- No system writes to the flexible metadata tables.
- The three ``cdb_startracker*`` schemas are empty and are not in use.
- The Transformed EFD container image in this repository does not run as built.
  The :doc:`../developer-guide/building-artifacts` page gives the reason.

Support
=======

``#consolidated-database`` channel in Rubin Observatory Slack

Overall complaints:
-------------------

- Product Owner: Lynne Jones

ConsDB services (hinfo, pqserver):
--------------------------------------

- Developer: Brian Brondel
- OSW project, ``ConsDB`` label in Jira

Transformed EFD component:
--------------------------

- Developer: Rodrigo Boufleur
- DM project, ``consdb`` component in Jira.

Documentation
=============

Primary documentation is located at `consdb.lsst.io <https://consdb.lsst.io>`__.
