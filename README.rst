######
consdb
######

The Consolidated Database (ConsDB) contains metadata about the images of the Vera C. Rubin Observatory.
This repository contains the scripts and the services that fill the Summit Visit Database and ConsDB.
These services also summarize the Engineering and Facilities Database (EFD).

Documentation
=============

The full documentation is at `consdb.lsst.io <https://consdb.lsst.io>`__.
It has four guides:

- `User Guide <https://consdb.lsst.io/user-guide/index.html>`__ — the schemas, and how to query them with TAP, the REST API, or SQL.
- `Contributor Guide <https://consdb.lsst.io/contributor-guide/index.html>`__ — how to add tables and columns, and how to insert data.
- `Developer Guide <https://consdb.lsst.io/developer-guide/index.html>`__ — the repository structure, the build artifacts, and the standards.
- `Operator Guide <https://consdb.lsst.io/operator-guide/index.html>`__ — how to deploy ConsDB, how to migrate a schema, and how to monitor the services.

Repository layout
=================

- ``python/lsst/consdb/`` — the source code of the services.
- ``alembic/`` — the schema migrations, with one directory for each schema.
- ``doc/`` — the source of the documentation site.
- ``docker/`` — the Dockerfiles and the Docker Compose configuration.
- ``tests/`` — the tests.

References
==========

- `DMTN-227 <https://dmtn-227.lsst.io>`_ — the goals and the architecture of ConsDB.
- `Science Data Model Schemas <https://sdm-schemas.lsst.io>`__ — the browser for the ConsDB schemas.
