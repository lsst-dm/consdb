##################
Building Artifacts
##################

This page gives the container images and the GitHub Actions workflows that make them.

To run the images on your machine, see the :doc:`local-environment` page.

The build context
=================

The ``docker/`` directory contains one Dockerfile for each image.
The build context of every image is the top directory of the repository, and not the ``docker/`` directory.

The ``.dockerignore`` file removes the ``docker/`` directory from the build context.
Two files are exceptions: ``docker/alembic-setup.sql`` and ``docker/run-pytest.sh``.
A Dockerfile that needs one of these two files must copy it with its own ``COPY`` command.

Container images
================

pqserver
--------

``docker/Dockerfile.pqserver`` makes the image of the ``pqserver`` REST API service.

- Base image: ``python:3.11``.
- The image copies only the modules that ``pqserver`` needs into ``/consdb_pq/``.
  If you add a new module to the service, you must add it to this list.
- The build argument ``GITHUB_TAG`` sets the ``VERSION`` environment variable.
- The service listens on port 8080.
- You must set ``POSTGRES_URL``.
  As an alternative, set ``DB_HOST``, ``DB_USER``, ``DB_PASS``, and ``DB_NAME``.
- Entry point: ``uvicorn consdb_pq.pqserver:app``.

The service reads these other variables.
None of them is required.

.. list-table::
   :header-rows: 1
   :widths: 34 22 44

   * - Variable
     - Value if you do not set it
     - Function
   * - ``URL_PREFIX``
     - ``/consdb``
     - The prefix of every public endpoint and of the API documentation.
   * - ``MAX_ROWS``
     - ``1000000``
     - The most rows that ``/query`` returns. The rest are discarded.
   * - ``FETCH_SIZE``
     - ``10000``
     - The number of rows that ``/query`` reads from the database at a time.
   * - ``STATEMENT_TIMEOUT_SECONDS``
     - ``600``
     - The time after which the database cancels a ``/query`` statement.
   * - ``POOL_RECYCLE_TIME``
     - ``3000``
     - The age in seconds at which a pooled connection is replaced. Keep it below the idle timeout of the database, which is 3600 at the Summit.
   * - ``LOG_CONFIG``
     - Empty
     - The log level of each component, in the form that the :ref:`hinfo page <hinfo-logging>` gives.
   * - ``NAME``, ``DESCRIPTION``, ``REPOSITORY_URL``, ``DOCUMENTATION_URL``
     - The values for ConsDB
     - Reported at the root endpoint and in the API documentation.

The service writes an access log line for each request, except for a successful health check at ``/``.
The :doc:`pqserver` page gives the architecture of the service.

hinfo
-----

``docker/Dockerfile.hinfo`` makes the image of the ``hinfo`` service.
This service reads Header Service metadata and writes it to ConsDB.

- Base image: ``ghcr.io/lsst/scipipe:al9-<OBS_LSST_VERSION>``.
  The build argument ``OBS_LSST_VERSION`` has the value ``w_2025_21``.
- The image installs the repository as an editable package.
- You must set these variables:

  - ``INSTRUMENT``: ``LATISS``, ``LSSTComCam``, or ``LSSTCam``.
  - ``POSTGRES_URL``: a SQLAlchemy connection URL.
  - ``KAFKA_BOOTSTRAP``: the host and the port of the bootstrap server.
  - ``KAFKA_PASSWORD``: the password for SASL_PLAIN authentication.
  - ``SCHEMA_URL``: the URL of the Kafkit registry schema.

- You do not have to set these variables:

  - ``BUCKET_PREFIX``: use ``rubin:`` at the USDF. The value is empty if you do not set it.
  - ``KAFKA_GROUP_ID``: the name of the consumer group. The value is ``consdb-consumer`` if you do not set it.
  - ``KAFKA_USERNAME``: the user for SASL_PLAIN authentication. The value is ``consdb`` if you do not set it.

transformed-efd
---------------

``docker/Dockerfile.transformed-efd`` makes the image of the Transformed EFD pipeline.

- Base image: ``ghcr.io/lsst/scipipe:al9-<OBS_LSST_VERSION>``.
  The build argument ``OBS_LSST_VERSION`` has the value ``w_2025_11``.
- The image installs ``kafkit`` 0.2.1 and ``lsst_efd_client`` 0.12.0.
- It copies the ``python`` directory into the stack.
- The command reads these variables: ``CONFIG_FILE``, ``INSTRUMENT``, ``BUTLER_REPO``,
  ``CONSDB_URL``, ``EFD``, ``TIMEDELTA``, and ``LOG_FILE``.
- Set ``S3_ENDPOINT_URL`` and ``LSST_RESOURCES_S3_PROFILE_embargo`` for access to the embargo Butler.

.. note::

   The command and the value of ``CONFIG_FILE`` in this Dockerfile point to a directory with the
   name ``efd_transform``.
   The package now has the name ``transformed_efd``, and the directory ``efd_transform`` does not exist.
   The command also passes no ``--mode`` argument, which the program requires, and it does not declare the ``EFD`` variable that it uses.
   You must correct these before this image can run.
   The :doc:`../operator-guide/transformed-efd` page gives the deployment that is in use.

daily consistency check
-----------------------

``docker/Dockerfile.daily_consistency_check`` makes the image of the daily consistency check.
A scheduled job runs this image once each day.
The :doc:`../operator-guide/monitoring` page gives the rules that the check applies.

- Base image: ``python:3.12-slim``.
- The image copies only three modules, so it is small and it starts quickly.
- You must set ``DB_HOST``, ``DB_USER``, ``DB_PASS``, and ``DB_NAME``.
- You do not have to set ``DB_PORT``, ``DAY_OBS``, or ``INSTRUMENTS``.
- Entry point: ``python -m lsst.consdb.daily_consistency_check``.

pytest
------

``docker/Dockerfile.pytest`` makes the image that runs the test suite.
The "Run PyTest" workflow builds this image for each pull request.

- Base image: ``ghcr.io/lsst/scipipe:al9-<OBS_LSST_VERSION>``.
  The build argument ``OBS_LSST_VERSION`` has the value ``w_2025_21``.
- The build argument ``BRANCH_NAME`` selects the branch of ``sdm_schemas``.
  If a branch with that name is on the ``sdm_schemas`` remote, the image uses that branch.
  If not, the image uses the ``main`` branch.
- The entry point is ``docker/run-pytest.sh``.
  This script sets up the ``obs_lsst``, ``felis``, and ``sdm_schemas`` EUPS packages.
  Then it runs ``pytest`` and sends all further arguments to it.
- The image writes the reports to ``/home/lsst/consdb/pytest_reports``.

The :doc:`local-environment` page gives the commands that run this image on your machine.

database
--------

``docker/Dockerfile.db`` makes the PostgreSQL image for the local Compose stack.

- Base image: ``postgres:17.6-bookworm``.
- The image adds the ``postgresql-17-pgsphere`` package.
  The ``pgs_region`` columns need this extension.
- No GitHub Actions workflow builds this image.
  Only the local Compose stack builds it.
  The Summit and the USDF use their own PostgreSQL servers.

alembic
-------

``docker/Dockerfile.alembic`` makes the image that applies the migrations in the local Compose stack.

- Base image: ``python:3.12-slim``.
- The image installs ``git`` and ``postgresql-client``.
- It gets the ``sdm_schemas`` repository into ``/sdm_schemas``, and ``SDM_SCHEMAS_DIR`` points to it.
- It copies ``docker/alembic-setup.sql`` with its own ``COPY`` command, because ``.dockerignore``
  removes the ``docker/`` directory.
- No GitHub Actions workflow builds this image.
  Only the local Compose stack builds it.

GitHub Actions workflows
========================

The ``.github/workflows/`` directory contains eight workflows.

Workflows that make artifacts
-----------------------------

.. list-table::
   :header-rows: 1
   :widths: 22 30 48

   * - Workflow
     - Trigger
     - Function
   * - ``build.yaml``
     - A push to ``main``, a tag, or a pull request
     - Builds three images and pushes them to the GitHub Container Registry.
   * - ``pytest.yaml``
     - A push to ``main`` or a pull request
     - Builds ``Dockerfile.pytest``, runs the tests, and keeps the two reports.
   * - ``docs.yaml``
     - A push, a pull request, or a release
     - Builds this site with ``tox`` and sends it to LSST the Docs.

``build.yaml`` makes these three images:

.. list-table::
   :header-rows: 1
   :widths: 34 66

   * - Dockerfile
     - Image name
   * - ``Dockerfile.hinfo``
     - ``ghcr.io/lsst-dm/consdb-hinfo``
   * - ``Dockerfile.pqserver``
     - ``ghcr.io/lsst-dm/consdb-pq``
   * - ``Dockerfile.transformed-efd``
     - ``ghcr.io/lsst-dm/consdb-transformed-efd``

For a tag, ``build.yaml`` gives the tag name to the ``GITHUB_TAG`` build argument.
For all other events, the value is ``noversion``.

``build.yaml`` does not make the ``db``, ``alembic``, ``pytest``, or daily consistency check images.

Workflows that check the code
-----------------------------

.. list-table::
   :header-rows: 1
   :widths: 26 74

   * - Workflow
     - Function
   * - ``lint.yaml``
     - Runs the Rubin shared lint workflow and ``ruff``.
   * - ``formatting.yaml``
     - Runs the Rubin shared format check.
   * - ``rebase_checker.yaml``
     - Fails if the branch contains a merge of ``main``. Rebase the branch instead.

Workflows that make pull requests
---------------------------------

``migrate.yaml`` makes the Alembic migration for a schema change.
The ``sdm_schemas`` repository starts it, or you can start it by hand.
It needs a branch name and a commit hash from ``sdm_schemas``.
The branch name must have the form ``tickets/DM-<number>``.
The workflow runs ``alembic-autogenerate.py`` and then makes a draft pull request in this repository.
The :doc:`../operator-guide/schema-migration-process` page gives the manual steps that come after this.

``efd_schema_sync.yaml`` copies the Transformed EFD schema files to ``sdm_schemas``.
A merged pull request starts it, or you can start it by hand.
The branch name must have the form ``tickets/DM-<number>``.
The workflow copies the files from ``python/lsst/consdb/transformed_efd/schemas/yml`` to
``python/lsst/sdm/schemas`` and makes a pull request in ``sdm_schemas``.
It does not copy ``efd_scheduler.yaml``, and it deletes no files.
