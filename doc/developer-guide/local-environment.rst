#############################
Local Development Environment
#############################

This section describes how you can set up a copy of the Consolidated Database environment using
Docker on your local machine. This is useful for testing in a way that doesn't interfere with users
on the test stands or at USDF.

The ``docker/docker-compose.yml`` file starts a copy of ConsDB on your machine.
The copy contains a PostgreSQL database, the Alembic migrations, the ``pqserver`` REST API, and a database web interface.
Use it to test a change before you deploy it to a test stand or handling data in a way you would not be
able to do in a shared environment.

The stack also optionally starts a second copy of ``pqserver``.
You can send the same request to both copies and compare the two results.
The :ref:`local-env-compare` section gives this procedure.

Before you start
================

You must have Docker Engine and the Docker Compose plugin on your machine.

Start all commands from the ``docker/`` directory, because the Compose file is in that directory.
The build context of each image is the top directory of the repository.

.. note::

   This page uses the ``docker compose`` command.
   If your machine has the older stand-alone tool, use ``docker-compose`` instead.

Start the stack
===============

1. Go to the ``docker/`` directory:

   .. code-block:: bash

      cd docker

2. Get some Header Service YAML files.
   The three ``hinfo_*`` services read these files and write the data to the database.
   Each service reads one instrument.

   At the USDF you can find examples in ``/sdf/data/rubin/offline/s3-tmp-backup/``.
   That directory contains LATISS files only.
   The authoritative copies are in the LFA, in the ``ATHeaderService`` and the
   ``MTHeaderService`` buckets.

3. Give the path of each directory to the ``hinfo_*`` services.
   Put the paths in a file with the name ``.env`` in the ``docker/`` directory:

   .. code-block:: bash

      LATISS_YAML=/path/to/your/latiss/yaml
      COMCAM_YAML=/path/to/your/lsstcomcam/yaml
      LSSTCAM_YAML=/path/to/your/lsstcam/yaml

   A ``hinfo_*`` service does no work if you do not set its directory variable.
   The stack starts correctly in that condition, but the database contains no exposure data.
   The :ref:`local-env-variables` section gives all the other variables that you can set.

4. Start all the services:

   .. code-block:: bash

      docker compose up --build -d

5. Wait for the ``alembic`` service to apply the migrations.
   The database is not complete before this service stops its work.
   Read the progress with this command:

   .. code-block:: bash

      docker compose logs -f alembic

6. Wait for the ``hinfo_*`` services to load the YAML files.
   Each service reads all the files in its directory tree.
   A large tree takes a long time.
   Read the progress with this command:

   .. code-block:: bash

      docker compose logs -f hinfo_latiss

7. Open one of the URLs in the :ref:`local-env-services` section.

The first build takes a long time, because Docker must get the base images.
Later builds are much faster.

.. _local-env-services:

The services
============

.. list-table::
   :header-rows: 1
   :widths: 22 26 52

   * - Service
     - Address
     - Function
   * - ``db``
     - ``localhost:5432``
     - PostgreSQL 17 with the pgSphere extension.
   * - ``pgadmin``
     - http://localhost:8080
     - A web interface to the database.
   * - ``app``
     - http://localhost:8888
     - The ``pqserver`` REST API, built from your checkout.
   * - ``refapp``
     - http://localhost:8889
     - A second ``pqserver`` REST API, built from a reference checkout.
   * - ``alembic``
     - None
     - Prepares the database and applies the migrations. Then it waits.
   * - ``hinfo_latiss``
     - None
     - Loads LATISS header files into the database.
   * - ``hinfo_comcam``
     - None
     - Loads LSSTComCam header files into the database.
   * - ``hinfo_lsstcam``
     - None
     - Loads LSSTCam header files into the database.
   * - ``pgadmin-init``
     - None
     - Writes the configuration files that ``pgadmin`` reads. Then it waits.

The ``alembic`` and ``pgadmin-init`` services stay alive after they complete their work.
This lets the other services wait for a Docker health check.

To connect to the database with a SQL client, use the user ``postgres`` and the database ``postgres``.

The ``pgadmin`` service opens with the e-mail address ``admin@example.com`` and the password ``consdb``.
It already contains a connection to the ``db`` service.

.. _local-env-variables:

Environment variables
=====================

Put your settings in a file with the name ``.env`` in the ``docker/`` directory.
Git ignores this file.

.. warning::

   Do not commit the ``.env`` file.
   Change all the passwords to values that are unique to your machine.

The database and pgAdmin read their passwords only at the first start.
To change a password after the first start, remove the data directories.
The :ref:`local-env-stop` section gives this procedure.

.. list-table::
   :header-rows: 1
   :widths: 40 32 28

   * - Variable
     - Value if you do not set it
     - Function
   * - ``POSTGRES_PASSWORD``
     - ``pgpassword``
     - The password of the ``postgres`` role.
   * - ``PGADMIN_DEFAULT_EMAIL``
     - ``admin@example.com``
     - The pgAdmin account name.
   * - ``PGADMIN_DEFAULT_PASSWORD``
     - ``consdb``
     - The pgAdmin password.
   * - ``PGADMIN_CONFIG_SERVER_MODE``
     - ``False``
     - Set it to ``True`` for the pgAdmin multi-user mode.
   * - ``PGADMIN_CONFIG_MASTER_PASSWORD_REQUIRED``
     - ``False``
     - Set it to ``True`` to make pgAdmin ask for a master password.
   * - ``ALEMBIC_UPDATE``
     - ``1``
     - Set it to ``0`` to stop the migration step.
   * - ``ALEMBIC_TARGET``
     - ``head``
     - The target revision. Use ``head`` or ``prehead``.
   * - ``ALEMBIC_INSTRUMENTS``
     - ``latiss lsstcomcam lsstcomcamsim lsstcam``
     - The Alembic trees to upgrade, with a space between each name.
   * - ``REFERENCE_PQSERV``
     - ``../../consdb``
     - The build context of the ``refapp`` service.
   * - ``LATISS_YAML``
     - No value
     - A directory of LATISS header files.
   * - ``COMCAM_YAML``
     - No value
     - A directory of LSSTComCam header files.
   * - ``LSSTCAM_YAML``
     - No value
     - A directory of LSSTCam header files.
   * - ``EXP_COLUMNS_TO_UPDATE``
     - No value
     - The exposure columns that ``hinfo`` writes again.
   * - ``CCD_COLUMNS_TO_UPDATE``
     - No value
     - The CCD exposure columns that ``hinfo`` writes again.

.. _local-env-compare:

Compare two versions of pqserver
================================

The ``app`` service and the ``refapp`` service run the same code by default.
Point ``refapp`` at a second checkout to compare two versions of ``pqserver``.

1. Make a second checkout of the repository.
   For example, use a checkout of the ``main`` branch.

2. Give the path of that checkout to the ``refapp`` service:

   .. code-block:: bash

      REFERENCE_PQSERV=/path/to/reference/consdb

3. Start the stack again.

4. Send the same request to http://localhost:8888 and to http://localhost:8889.
   Then compare the two results.

Both services use the same database.

Run pqserver outside the containers
===================================

The ``app`` image must be built again after each change to the code.
To skip that step while you work, run ``pqserver`` on your machine against the ``db`` service of the stack:

.. code-block:: bash

   cd ..    # the top directory of the repository
   PYTHONPATH=python POSTGRES_URL=postgresql://postgres:pgpassword@localhost:5432/postgres \
       uvicorn lsst.consdb.pqserver:app --reload --port 8890

Use the password from your ``.env`` file if you changed it.
The ``--reload`` option restarts the service when a source file changes.
The API is then at ``http://localhost:8890/consdb``.

The same ``POSTGRES_URL`` runs the daily consistency check against the stack:

.. code-block:: bash

   DB_HOST=localhost DB_USER=postgres DB_PASS=pgpassword DB_NAME=postgres \
       PYTHONPATH=python python -m lsst.consdb.daily_consistency_check 20240801

Apply a migration from your machine
===================================

To test a new migration, keep the ``alembic`` service from changing the database, and run Alembic yourself.
Set ``ALEMBIC_UPDATE=0`` in ``.env``, start the stack, and then run from the top directory of the repository:

.. code-block:: bash

   export CONSDB_URL=postgresql://postgres:pgpassword@localhost:5432/postgres
   export SDM_SCHEMAS_DIR=/path/to/sdm_schemas
   alembic -n latiss upgrade head

This is also the way to protect a database that took a long time to fill.
The migration step runs at every start of the stack, and a revision on a branch that you later abandon leaves the database at a revision that the tree no longer has.
The :doc:`alembic` page gives the commands that show and repair the recorded revision.

Control the migration step
==========================

The ``alembic`` service does three things.
First, it runs ``docker/alembic-setup.sql``.
This file makes the ``cdb`` schema, the ``pg_sphere`` extension, and the ``usdf`` and ``oods`` roles.
Second, it makes a ``cdb_<instrument>`` schema for each instrument in ``ALEMBIC_INSTRUMENTS``.
Third, it upgrades each of those Alembic trees to the target revision.

Set ``ALEMBIC_INSTRUMENTS`` to one name when you work on one instrument.
This makes the start much faster:

.. code-block:: bash

   ALEMBIC_INSTRUMENTS=latiss

``ALEMBIC_TARGET`` accepts two values.
Each Alembic tree has an independent revision graph, so only these two symbolic values apply to all the trees.

- ``head`` upgrades each tree to its most recent revision.
- ``prehead`` upgrades each tree to the parent of its most recent revision.

Use ``prehead`` to test a new migration.
It gives you a database at the revision before your migration.
You can then apply your migration by hand and examine the result.

Set ``ALEMBIC_UPDATE`` to ``0`` to keep the database as it is.

.. _local-env-stop:

Stop the stack
==============

To stop all the services, use this command:

.. code-block:: bash

   docker compose down

The database keeps its data, because the ``db`` service writes to the ``docker/pgdata`` directory.
The next start uses the same data.

To start again with an empty database, remove the data directories:

.. code-block:: bash

   docker compose down
   rm -rf pgdata pgadmin-data pgadmin-cfg

Git ignores these three directories.

Run the tests in a container
============================

The ``docker/Dockerfile.pytest`` image runs the test suite in the same way as the GitHub Actions workflow.
Use it when a test passes on your machine but fails in CI.

1. Build the image from the top directory of the repository:

   .. code-block:: bash

      docker build --build-arg BRANCH_NAME=$(git branch --show-current) \
          -f docker/Dockerfile.pytest -t pytest_image .

2. Run the tests:

   .. code-block:: bash

      docker run --rm -v $PWD/pytest_reports:/home/lsst/consdb/pytest_reports pytest_image

3. Read the reports in the ``pytest_reports`` directory.
   The file ``pytest_report.html`` gives the test results.
   The ``htmlcov`` directory gives the coverage report.

The image gets the ``sdm_schemas`` repository during the build.
If a branch with your branch name is on the ``sdm_schemas`` remote, the image uses that branch.
If not, the image uses the ``main`` branch.

The entry point sends all further arguments to ``pytest``.
Use this to run one test:

.. code-block:: bash

   docker run --rm pytest_image tests/test_pqserver.py::test_root

This container does not need the Compose stack.
It makes its own temporary database.
