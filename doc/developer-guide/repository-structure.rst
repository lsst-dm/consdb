####################
Repository Structure
####################

This page gives the layout of the repository and the purpose of each module.
It does not describe the functions in a module.
The docstrings in the code do that.

Top level
=========

.. list-table::
   :header-rows: 1
   :widths: 26 74

   * - Path
     - Content
   * - ``python/lsst/consdb/``
     - The source code of the services. See below.
   * - ``alembic/``
     - The schema migrations, with one directory for each schema. The :doc:`alembic` page gives the layout.
   * - ``alembic.ini``, ``alembic-autogenerate.py``
     - The Alembic configuration and the script that generates a migration.
   * - ``docker/``
     - The Dockerfiles, the Compose configuration, and the scripts that the images use. The :doc:`building-artifacts` page gives each image.
   * - ``doc/``
     - The source of this site.
   * - ``tests/``
     - The tests and their fixtures, and the migration validation script. See below.
   * - ``pyproject.toml``, ``setup.cfg``, ``setup.py``, ``tox.ini``
     - The package metadata and the tool configuration. The :doc:`standards-practices` page gives the tools.

Every tool is started as ``python -m lsst.consdb.<module>`` or by the path of the script.
The package defines no console entry points.

The ``lsst.consdb`` package
===========================

The modules fall into four groups.
The first group forms the ``pqserver`` REST service.
The :doc:`pqserver` page gives the architecture of the service.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Module
     - Purpose
   * - ``pqserver.py``
     - Builds the FastAPI application, mounts the two routers, and installs the middleware and the exception handlers.
   * - ``handlers/external.py``
     - The public endpoints under the ``/consdb`` prefix.
   * - ``handlers/internal.py``
     - The health check endpoint at ``/``, which is not in the API documentation.
   * - ``handlers/consistency_page.py``
     - The HTML of the interactive table consistency report.
   * - ``config.py``
     - The settings of the service, read from environment variables, and the logging setup.
   * - ``dependencies.py``
     - The database engine, the sessions, and the cached schema objects that the endpoints share.
   * - ``models.py``
     - The request and response models, including the validation of units and UCDs.
   * - ``exceptions.py``
     - The exceptions that the service reports to the client as JSON.
   * - ``cdb_schema.py``
     - Reflection of one ``cdb_*`` schema from the database, and the key and flexible metadata logic built on it.

The second group fills the database.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Module
     - Purpose
   * - ``hinfo.py``
     - Reads Header Service files and fills the ``exposure`` and ``ccdexposure`` tables. The :doc:`hinfo` page gives the service.
   * - ``transformed_efd/``
     - The Transformed EFD pipeline, which summarizes the EFD into the ``efd_*`` schemas. The :doc:`transformed-efd` page gives the architecture.
   * - ``summarize_efd.py``
     - An earlier, stand-alone EFD summarizer with its own command line. No container and no test uses it. The ``transformed_efd`` package replaces it.

The third group checks the database.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Module
     - Purpose
   * - ``consistency_queries.py``
     - The SQL of each consistency rule, for each instrument that has rules. The :doc:`../operator-guide/monitoring` page gives the rules in words.
   * - ``daily_consistency_check.py``
     - The scheduled job that runs the rules for one day and writes the alert log records.

The fourth group is shared.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Module
     - Purpose
   * - ``cdb_pgsphere.py``
     - The SQLAlchemy type of a pgSphere polygon, and the function that adds the ``pgs_region`` column to a schema loaded from YAML. Every Alembic environment and the migration validator import it. The :doc:`alembic` page explains why.
   * - ``utils.py``
     - The database connection and the logging setup for the tools that do not use ``config.py``.

The ``pqserver`` image copies an explicit list of modules.
If you add a module to the service, add it to ``docker/Dockerfile.pqserver`` as well.

Tests
=====

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - File
     - Content
   * - ``tests/test_pqserver.py``
     - The REST endpoints, against a temporary database filled from the ``tests/lsstcomcamsim/`` fixtures.
   * - ``tests/test_insert_endpoints_lsstcam.py``
     - A row inserted into every LSSTCam table through each of the three insert endpoint forms, in foreign key order.
   * - ``tests/test_hinfo.py``
     - One LATISS header file, ``tests/ATHeaderService_header_AT_O_20240801_000302.yaml``, through the local file mode of ``hinfo``.
   * - ``tests/transformed_efd/``
     - The configuration model, the schema generator, the queue manager, the failure monitor, the summary functions, and the multi-database writes of the Transformed EFD.
   * - ``tests/lsstcomcamsim/*.ecsv``
     - Fixture tables for ``cdb_lsstcomcamsim``: exposure, CCD exposure, flexible metadata, and quicklook rows.
   * - ``tests/validate_schema_migrations.py``
     - Not a test. A script that validates a new migration. The :doc:`../operator-guide/schema-migration-process` page gives its use.
   * - ``tests/SConscript``
     - The EUPS build harness. The Docker test image does not use it.

The modules in the first group other than ``pqserver.py`` and the handlers have no tests of their own.
Neither do ``daily_consistency_check.py``, ``consistency_queries.py``, ``cdb_pgsphere.py``, or the transformation engine of the Transformed EFD.

The :doc:`local-environment` page gives the commands that run the tests.

