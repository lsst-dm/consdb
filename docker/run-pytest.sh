#!/usr/bin/env bash
# Entrypoint for Dockerfile.pytest. Loads the LSST stack, sets up the obs_lsst
# / felis / sdm_schemas EUPS packages, and runs the test suite.
#
# Any extra arguments are forwarded to pytest, so callers can pin a single
# test (e.g. ``docker run ... tests/test_pqserver.py::test_root``).

set -e

source /opt/lsst/software/stack/loadLSST.bash
setup obs_lsst
setup felis
setup -kr /home/lsst/sdm_schemas/

exec pytest \
    --cov=./ \
    --cov-report=html:/home/lsst/consdb/pytest_reports/htmlcov \
    --html=pytest_reports/pytest_report.html \
    --self-contained-html \
    -vv \
    tests "$@"
