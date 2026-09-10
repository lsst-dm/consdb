#######################
Standards and Practices
#######################

Versions and tags
=================

* The consdb repository will be tagged using `calendar-based versioning <https://calver.org>`__.  We are using a ``YY.0M.N`` format with a two-digit short year, a zero-padded month number, and a 1-based sequence number within a month.
* Tags should be annotated git tags (``git tag -a``).
* The package version comes from the tag through ``setuptools_scm``.
  The ``pqserver`` image gets the tag name from the ``GITHUB_TAG`` build argument and reports it at its root endpoint.

Branches and pull requests
==========================

* Work on a ticket branch, named ``tickets/DM-<number>`` or ``tickets/OSW-<number>`` after the Jira ticket.
  The migration and schema synchronization workflows only accept a ``tickets/DM-<number>`` name.
* Rebase a branch onto ``main``.
  The ``rebase_checker`` workflow fails a pull request that contains a merge of ``main``.
* For full details about the team workflow, refer to the `developer guide <https://tssw-developer.lsst.io/>`__.
* A change to a schema needs a matching pull request in ``sdm_schemas``.
  The :doc:`../operator-guide/schema-migration-process` page gives the order of the two merges.

Code style
==========

The line length is 110 characters.
These tools enforce the style, with their settings in ``pyproject.toml`` and ``setup.cfg``:

* `Black <https://black.readthedocs.io/>`__ formats the code.
  Alembic also runs it on each generated migration.
* `isort <https://pycqa.github.io/isort/>`__ orders the imports, with the Black profile.
* `flake8 <https://flake8.pycqa.org/>`__ and `ruff <https://docs.astral.sh/ruff/>`__ check the code.
  ``setup.cfg`` gives the flake8 rules that are ignored.
  The generated migrations, ``doc/``, and the ``__init__.py`` files are excluded.

The ``.pre-commit-config.yaml`` file runs all of these, and also checks YAML syntax, trailing whitespace, and the final newline.
Install the hooks once with ``pre-commit install``.
The ``lint`` and ``formatting`` workflows run the same checks on each pull request.

Black targets Python 3.13.
The container images use several versions: 3.11 for ``pqserver``, 3.12 for the consistency check and the migrations, and the version of the LSST stack for ``hinfo`` and the Transformed EFD.
Write code that runs on all of them.

Tests
=====

* Run the tests in the Docker test image, as the :doc:`local-environment` page describes.
  The image provides the LSST stack packages that the tests import, and the host environment usually does not.
* The test image runs ``pytest`` with coverage.
  ``pyproject.toml`` sets the ``pytest`` options.

The ``tox.ini`` file has environments for the tests, the coverage report, ``mypy``, the pre-commit hooks, and the documentation.
Only the ``docs`` environment is in use; CI runs it.
The ``typing`` environment points at a path that does not exist, and the ``docs-linkcheck`` environment needs a ``Makefile`` that does not exist.

Dependencies
============

The Dockerfiles are the record of what each service needs.
``pyproject.toml`` declares only four runtime dependencies, which is far fewer than the code imports.
When you add an import to a service, add the package to the Dockerfile of that service.
