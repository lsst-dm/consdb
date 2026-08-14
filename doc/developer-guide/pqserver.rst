####################
The pqserver Service
####################

``pqserver`` is the REST API of ConsDB.
The :doc:`../user-guide/rest-api-and-clients` page gives the API from the point of view of a client, and the interactive documentation that the service serves gives every endpoint.
This page gives the architecture of the service for a developer who changes it.

Layout
======

``pqserver.py`` builds the FastAPI application.
It mounts two routers.

- ``handlers/internal.py`` provides ``GET /`` for the Kubernetes health check.
  It is excluded from the API documentation.
  A log filter in ``pqserver.py`` drops the access log line of each successful call, so that the health check does not fill the log.
- ``handlers/external.py`` provides every public endpoint, under the ``URL_PREFIX`` setting, which is ``/consdb`` by default.
  The interactive documentation is under the same prefix.

The application adds two pieces of middleware: the Safir ``X-Forwarded`` middleware, so that the service sees the client address behind the ingress, and gzip compression for responses over 1000 bytes.

Three exception handlers turn errors into JSON.
``BadValueException`` and its subclass ``UnknownInstrumentException`` become a 404 response with the invalid value and the list of valid values.
``SQLAlchemyError`` becomes a 500 response with the message of the database, and a log record with the traceback.
Anything else falls through to the FastAPI defaults.

There is no authentication in the service.
The ingress of the Rubin Science Platform performs it.

Configuration
=============

``config.py`` defines the settings as a ``pydantic-settings`` model, so each field is an environment variable with the same name in upper case.
The :doc:`building-artifacts` page lists the variables.
The module also configures logging as a side effect of validating the ``LOG_CONFIG`` field, which is why importing ``config`` is enough to get the log format.

The database URL comes from ``POSTGRES_URL``, then ``CONSDB_URL``, then the four ``DB_*`` variables, in that order of precedence.

Shared state
============

``dependencies.py`` holds the objects that the endpoints share.

- One SQLAlchemy engine for the process, with a pool that recycles a connection after fifty minutes.
  The Summit database closes an idle connection after sixty minutes, and the recycling avoids the race.
- One session factory bound to that engine.
  Each request gets its own session through ``get_db()``.
- The list of instruments, which is the list of schemas whose name starts with ``cdb_``, with the prefix removed.
  It is computed once.
- One ``InstrumentTable`` object for each instrument, created on first use.

``InstrumentTable`` in ``cdb_schema.py`` reflects the ``cdb_<instrument>`` schema from the database when it is created.
Everything that depends on the schema, such as the key columns of each table and the type of each timestamp column, comes from that reflection.
This is why the service must be restarted after a schema migration.
The one exception is the flexible metadata schema, which the ``addkey`` endpoint refreshes after each insert.

The tests call ``reset_dependencies()`` to discard all of this state between test databases.

The insert endpoints
====================

The insert endpoints share one helper.
It resolves the key columns of the target table, checks that the request supplies every non-nullable column and no column that the table lacks, converts timestamp strings with ``astropy.time.Time``, and builds a PostgreSQL ``INSERT ... ON CONFLICT`` statement.
The ``u`` parameter selects ``DO NOTHING`` or ``DO UPDATE``.
The bulk endpoint builds one statement with all the rows.

A table without a ``day_obs`` column cannot be written through these endpoints.

The query endpoint
==================

The ``/query`` endpoint runs the statement inside a transaction with a statement timeout.
It fetches rows in batches until the row limit of the settings is reached, and then it stops without reading the rest.
The ``commit`` parameter, when it is not 1, rolls the transaction back at the end.

Where to make a change
======================

.. list-table::
   :header-rows: 1
   :widths: 46 54

   * - Task
     - Location
   * - Add an endpoint
     - ``handlers/external.py``, with a request or response model in ``models.py``.
   * - Add a setting
     - A field in ``config.py``, and a row on the :doc:`building-artifacts` page.
   * - Add a consistency rule
     - The SQL in ``consistency_queries.py``, and the description on the :doc:`../operator-guide/monitoring` page.
   * - Add a module to the service
     - Add it to the ``COPY`` list in ``docker/Dockerfile.pqserver``. The image does not copy the whole package.
   * - Change how a key is resolved
     - ``InstrumentTable`` in ``cdb_schema.py``.

The tests in ``tests/test_pqserver.py`` and ``tests/test_insert_endpoints_lsstcam.py`` run the service with the FastAPI test client against a temporary database.
The :doc:`local-environment` page gives the command that runs them.
