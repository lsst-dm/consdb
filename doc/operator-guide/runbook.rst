########
RunBook
########

Confluence runbook initial incomplete version `here <https://rubinobs.atlassian.net/wiki/spaces/LSSTOps/pages/45665320/Consolidated+Database+ConsDB+Runbook+draft+incomplete>`__

Overview
========

This application does ...

Its design and architecture are documented at ...

Usage
=====

Most users
----------

Administration
--------------

Architecture
============

Kubernetes vclusters used

Relevant policies

S3DF Dependencies
-----------------

- Kubernetes
- Weka storage for Kubernetes

Systems
-------

Components, Kubernetes namespaces, deployments

Backups
-------

Associated Systems
------------------

IAM
===

Requesting Access
-----------------

Key Roles
---------

Service Accounts
----------------

Network
=======

External endpoints, IP and port, encryption, authentication, clients, API

SLAC-internal endpoints, IP and port, encryption, authentication, clients, API

Configuration
=============

GitHub repos with deployments

Monitoring
==========

Grafana or other links

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

Documentation and Training
==========================

Primary documentation is located at `consdb.lsst.io <https://consdb.lsst.io>`__

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

Known Issues
============

Standard Procedures
===================
