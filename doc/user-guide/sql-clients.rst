###########
SQL Clients
###########

Since ConsDB is stored in a PostgreSQL database, direct access using a SQL client is possible.
This interface can provide the highest performance, but access must come from the same network as the database.


Connection information
======================

ConsDB is located in the ``exposurelog`` Postgres database in order to facilitate future joins between the human-maintained exposure log and the machine-generated Consolidated Database metadata tables.

The read-only ``usdf`` (even at the Summit) credential should be automatically populated into ``~/.lsst/postgres-credentials.txt``.
Services that require it can request a credential to write to ConsDB via SQL.

Summit
------

Use connection URL ``postgresql://usdf@postgresdb01.cp.lsst.org/exposurelog``.
Equivalently:

- Host: ``postgresdb01.cp.lsst.org``
- User: ``usdf``
- Database: ``exposurelog``

Connections must come from within the Rubin "Pixel Zone" network.

USDF
----

Use connection URL ``postgresql://usdf@usdf-summitdb-logical-replica-svc.sdf.slac.stanford.edu/exposurelog``.

Equivalently:

- Host: ``usdf-summitdb-logical-replica-svc.sdf.slac.stanford.edu``
- User: ``usdf``
- Database: ``exposurelog``

Connections must come from within the SLAC network.


Clients
=======

Within the RSPs, the ``pgcli`` command-line utility is available.

On the USDF interactive sdfiana machines, the ``psql`` command-line utility is also available.

From Python, use of `SQLAlchemy <https://docs.sqlalchemy.org/>`__ is suggested.
