###########
Monitoring
###########

Reporting channels
==================

Users of ConsDB, ConsDBClient (``pqserver``) should report issues via #consolidated-database in rubin-obs.slack.com.

ConsDB operators monitor this channel and #ops-usdf, #ops-usdf-alerts for issues and outages reported, as well as escalate verified database issues.

Database
========

The ConsDB team is responsible for verifying whether or not the database is up when issues are reported.

They can check the method reported by the users, check using ``psql``/ ``pgcli``, and check in the #ops-usdf slack channel for currently reported issues.

Once the ConsDB team has confirmed there is an issue with the database, they should notify #ops-usdf slack channel and USDF DBAs should be responsible for fixing/restarting.

REST API Server
===============

If we suspect the API server died, the ConsDB team should be responsible for checking and restarting it.

Use the appropriate argo-cd deployment graph to check deployment logs, and potentially restart the service.


Other issues
------------

If the K8s infrastructure died then the ConsDB team can verify the problem, but there are likely to be wider issues seen.

USDF or Summit K8s/IT support should be responsible for fixing.


Daily table consistency checks
==============================

A scheduled job runs the per-instrument consistency checks once per day,
validating the previous night's data against the rules below.
By default it checks the previous UTC observing day; set the ``DAY_OBS``
environment variable (or pass a ``YYYYMMDD`` argument) to check a specific day,
and set ``INSTRUMENTS`` to a semicolon-separated list (for example
``lsstcam;latiss``) to restrict which instruments are checked.
The job connects to PostgreSQL using the ``DB_HOST``, ``DB_PORT``, ``DB_USER``,
``DB_PASS``, and ``DB_NAME`` environment variables.

The checks read the ``exposure`` and ``ccdexposure`` base tables and their
``*_quicklook`` companions directly.  The rules fall into two groups, defined in
the two sections below: structural invariants that must always hold, and
derived-product coverage that depends on image type.  Each rule has a name shown
in ``monospace`` (for example ``ccdvisit1_quicklook_coverage``); this is the
value of the ``rule`` field returned by the ``/table_consistency`` endpoint and
used in the alert messages, so it is the handle for tracing an alert back to the
rule that produced it.

Detector layout
---------------

The rules reference the LSSTCam focal plane of 205 detectors (0-204):

.. list-table::
   :header-rows: 1
   :widths: 20 55 25

   * - Role
     - Detectors
     - Count
   * - Science
     - 0-188
     - 189
   * - Guider
     - 189, 190, 193, 194, 197, 198, 201, 202
     - 8
   * - Wavefront
     - 191, 192, 195, 196, 199, 200, 203, 204
     - 8

The 197 *imaging* detectors are the science plus wavefront sensors.  Guider
detectors never carry derived imaging products.

Structural invariants
---------------------

These invariants are expected to hold for every exposure regardless of image
type.

#. ``ccdexposure_completeness`` -- confirms the per-detector table is fully
   populated for the exposure: there must be exactly 205 ``ccdexposure`` rows,
   one for each detector, covering 0-204 with none missing, duplicated, or out of
   range.  This is the per-detector completeness guarantee the rest of the
   database relies on.
#. ``exposure_id_encoding`` -- confirms the exposure's identifier is internally
   consistent: ``exposure_id`` must equal ``day_obs * 100000 + seq_num``, the
   encoding the system uses to translate between an exposure's id and its
   ``(day_obs, seq_num)``.  A mismatch means the two no longer refer to the same
   exposure.
#. ``ccdexposure_key_agreement`` -- confirms a ``ccdexposure`` row's two
   references to its parent agree: the ``day_obs`` and ``seq_num`` it stores must
   identify the same ``exposure`` as its ``exposure_id``.  The schema validates
   each foreign key independently, so the two can point at different exposures
   without it noticing; this rule catches that.
#. ``no_guider_products`` -- confirms guider detectors carry no imaging products:
   no ``ccdexposure_quicklook`` or ``ccdvisit1_quicklook`` row may reference a
   guider detector, which records only guide-star data and is never reduced into
   the per-detector products that science and wavefront detectors produce.

The job does not re-check relationships the database already enforces.  Primary
keys, unique keys (such as ``(exposure_id, detector)`` on ``ccdexposure``), and
the ``*_quicklook`` foreign keys already guarantee key uniqueness and that no
quicklook row exists without its parent, so those conditions are left to the
schema.

Derived-product coverage
------------------------

For each exposure the job checks that the derived ``*_quicklook`` products that
should exist for that exposure's ``img_type`` are present and complete; the
producing pipelines run only for the relevant image types, so each rule is scoped
accordingly.  The per-detector counts follow the focal plane: 197 imaging
detectors (the 189 science plus 8 wavefront sensors), and 193 for the
per-detector visit products (the 189 science detectors plus the four single-sided
corner wavefront sensors 191, 195, 199, 203).

#. ``exposure_quicklook_coverage`` -- confirms every on-sky exposure
   (``science``, ``acq``, ``cwfs``, ``focus``, ``engtest``) has its one
   ``exposure_quicklook`` row of summary mount-motion metrics; a missing row
   means that summary was never written for the exposure.
#. ``visit1_quicklook_coverage`` -- confirms every exposure except ``indome`` and
   ``test`` has its one ``visit1_quicklook`` row holding the visit-level summary.
#. ``ccdexposure_quicklook_coverage`` -- confirms every imaging exposure has a
   ``ccdexposure_quicklook`` row for each imaging detector: 197 rows, or 189 for
   ``cwfs`` exposures, which reduce only the science detectors.  Fewer than
   expected means some detectors were never reduced.
#. ``ccdvisit1_quicklook_coverage`` -- confirms every on-sky science exposure
   (``science``, ``acq``) has all 193 ``ccdvisit1_quicklook`` rows of per-detector
   photometry and astrometry; fewer means some detectors are missing their
   measurements.
#. ``no_calibration_science_products`` -- confirms calibration frames carry no
   science measurements: ``bias``, ``flat``, and ``dark`` exposures must have zero
   ``ccdvisit1_quicklook`` rows, since visit-level photometry and astrometry are
   never produced for them.

These products are written on the same observing day as the raw exposures, so for
an applicable image type a missing row is a real gap rather than processing
latency.  The only expected soft spot is the most recent night, which may still
be in progress when the check runs.

For ``cdb_latiss`` only the single-detector ``exposure_quicklook`` coverage rule
and the applicable structural invariants apply.

Alerts
------

When a run finds no violations it logs an informational record per instrument::

    event=consdb_table_consistency_ok instrument=lsstcam day_obs=20260519

When a run finds violations it logs an error record per instrument, summarizing
the failed rules and the compressed ``seq_num`` ranges they affect::

    event=consdb_table_consistency_alert instrument=lsstcam day_obs=20260519 num_inconsistencies=3 message='ccdexposure_completeness failed for seq_num 544; ccdvisit1_quicklook_coverage failed for seq_num 312,901'

Loki alert rules are configured to fire on the
``event=consdb_table_consistency_alert`` error logs.
The ``num_inconsistencies`` field counts the affected entries and is useful for
thresholding.

On-demand queries
-----------------

The same report is available for any observing day through the REST API::

    GET /consdb/table_consistency/{instrument}/{day_obs}

allowing an operator to re-check a day after a backfill without waiting for the
next scheduled run.
