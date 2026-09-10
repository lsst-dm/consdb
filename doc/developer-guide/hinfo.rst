##################
The hinfo Service
##################

The ``hinfo`` service fills the ``exposure`` and the ``ccdexposure`` tables of each ``cdb_*`` schema.
It reads the metadata that the Header Service writes for each image.
It then maps that metadata to columns and writes the rows to ConsDB.

The service runs at the Summit only.
One instance runs for each instrument.
The :doc:`../operator-guide/deployment` page gives the deployment.

The source is ``python/lsst/consdb/hinfo.py``.

Data flow
=========

.. mermaid::

   flowchart TD
      A[Header Service] -->|largeFileObjectAvailable| B[Kafka topic]
      A -->|YAML header file| C[S3 bucket]
      B --> D[handle_message]
      D -->|wait for the file| C
      C --> E[process_resource]
      E --> F[KW_MAPPING and the instrument mapping]
      E --> G[ObservationInfo translation]
      G --> H[OI_MAPPING]
      E --> I[DETECTOR_MAPPING]
      F --> J[(exposure)]
      H --> J
      I --> K[(ccdexposure)]

      style E fill:#f3e5f5
      style J fill:#e8f5e8
      style K fill:#e8f5e8

Run modes
=========

The module has two run modes.
The number of command-line arguments selects the mode.

Kafka consumer mode
-------------------

.. code-block:: bash

   python -m lsst.consdb.hinfo

With no argument, the module calls ``main()``.
This is the mode that the Summit deployment uses.

``main()`` subscribes to one Kafka topic:

.. code-block:: text

   lsst.sal.<topic name>.logevent_largeFileObjectAvailable

``TOPIC_MAPPING`` gives the topic name for each instrument:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - ``INSTRUMENT``
     - Topic name
   * - ``LATISS``
     - ``ATHeaderService``
   * - ``LSSTComCam``
     - ``CCHeaderService``
   * - ``LSSTCam``
     - ``MTHeaderService``

The consumer uses the SASL_PLAINTEXT protocol with the SCRAM-SHA-512 mechanism.
It reads from the earliest offset, and it reads committed messages only.
A ``kafkit`` deserializer and the schema registry decode each message.

``main()`` starts a separate asyncio task for each message.
The task calls ``handle_message()``, which does three things:

1. It changes the URL in the message to an S3 URL.
   It replaces ``https://s3.<site>.lsst.org/`` with ``s3://``.
   It then adds ``BUCKET_PREFIX`` to the URL, if you set that variable.
2. It waits for the file to become available.
   ``wait_for_resource()`` looks for the file again after each interval of 0.1 to 2.0 seconds.
   The limit is 60 seconds.
   After the limit, the task writes a warning to the log and stops.
3. It calls ``process_resource()``.

Local file mode
---------------

.. code-block:: bash

   python -m lsst.consdb.hinfo /path/to/yaml

With one argument, the module calls ``process_local_path()``.
This mode needs no Kafka variables.

If the argument is a directory, the function walks the directory tree.
It processes each file with the ``.yaml`` suffix.
An error in one file does not stop the run.
The function writes the error to the log and continues with the next file.

If the argument is one ``.yaml`` file, the function processes that file only.

The local Compose stack uses this mode.
The :doc:`local-environment` page gives that procedure.

.. note::

   The module also contains ``process_date()``.
   This function reads all the headers of one observing day from the LFA bucket.
   The entry point does not call it.
   To use it, import the module and call the function.

Configuration
=============

The service reads its configuration from environment variables.

You must set these variables in both modes:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Variable
     - Function
   * - ``INSTRUMENT``
     - ``LATISS``, ``LSSTComCam``, or ``LSSTCam``.
   * - ``POSTGRES_URL``
     - The SQLAlchemy connection URL.
       As an alternative, set ``DB_HOST``, ``DB_USER``, ``DB_PASS``, and ``DB_NAME``.
       The four variables have precedence over ``POSTGRES_URL``.

You must set these variables in Kafka consumer mode only:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Variable
     - Function
   * - ``KAFKA_BOOTSTRAP``
     - The host and the port of the bootstrap server.
   * - ``KAFKA_PASSWORD``
     - The password for the SASL authentication.
   * - ``SCHEMA_URL``
     - The URL of the Kafkit schema registry.

You do not have to set these variables:

.. list-table::
   :header-rows: 1
   :widths: 40 22 38

   * - Variable
     - Value if you do not set it
     - Function
   * - ``KAFKA_USERNAME``
     - ``consdb``
     - The user for the SASL authentication.
   * - ``KAFKA_GROUP_ID``
     - ``consdb-consumer``
     - The name of the consumer group.
   * - ``KAFKA_SESSION_TIMEOUT_MS``
     - ``30000``
     - The Kafka session timeout.
   * - ``KAFKA_HEARTBEAT_INTERVAL_MS``
     - ``10000``
     - The Kafka heartbeat interval.
   * - ``KAFKA_MAX_POLL_INTERVAL_MS``
     - ``300000``
     - The maximum interval between two polls.
   * - ``BUCKET_PREFIX``
     - Empty
     - Set it to ``rubin:`` at the USDF.
       A value also sets ``LSST_DISABLE_BUCKET_VALIDATION``.
   * - ``EXP_COLUMNS_TO_UPDATE``
     - Empty
     - Limits the ``exposure`` columns. See :ref:`hinfo-selective`.
   * - ``CCD_COLUMNS_TO_UPDATE``
     - Empty
     - Limits the ``ccdexposure`` columns. See :ref:`hinfo-selective`.
   * - ``LOG_CONFIG``
     - Empty
     - Sets the log level of each component, as ``component=LEVEL``.
       Put a comma between two settings.
       The component ``.`` sets the root level of the LSST loggers.

Instruments and controllers
===========================

``get_instrument_dict()`` makes one ``Instrument`` object for each controller of an instrument.
The key of the dictionary is the value of the ``CONTRLLR`` header keyword.

.. list-table::
   :header-rows: 1
   :widths: 26 16 24 34

   * - ``INSTRUMENT``
     - ``CONTRLLR``
     - Schema
     - Translator
   * - ``LATISS``
     - ``O``
     - ``cdb_latiss``
     - ``LatissTranslator``
   * - ``LSSTComCam``
     - ``O``
     - ``cdb_lsstcomcam``
     - ``LsstComCamTranslator``
   * - ``LSSTComCam``
     - ``S``
     - ``cdb_lsstcomcamsim``
     - ``LsstComCamSimTranslator``
   * - ``LSSTCam``
     - ``O``
     - ``cdb_lsstcam``
     - ``LsstCamTranslator``

The ``CONTRLLR`` keyword thus sends the simulated LSSTComCam data to a different schema.
If the header contains a controller that the dictionary does not have, ``process_resource()``
writes a warning to the log and processes no data from that file.

Each ``Instrument`` object holds the translator, the two mappings, the camera geometry, and the two
SQLAlchemy tables.
The tables come from the database at start.
The service therefore reads the schema at start, and it does not see a schema change until it starts
again.

The processing sequence
=======================

``process_resource()`` does the full sequence for one header file:

1. It reads the YAML file.
2. It makes an ``info`` dictionary from the ``PRIMARY`` section.
   Each ``keyword`` becomes a key, and each ``value`` becomes a value.
3. It reads ``CONTRLLR`` from ``info`` and selects the ``Instrument`` object.
4. It puts the camera and the translator into ``info``.
5. If the image type is ``OBJECT``, and ``RA``, ``DEC``, and ``ROTPA`` are present, it computes the
   sky position of the corners of each CCD.
6. It applies ``KW_MAPPING`` and then the instrument mapping.
7. It makes an ``ObservationInfo`` object with the translator of the instrument.
8. It applies ``OI_MAPPING``.
   It changes an ``astropy`` quantity or a NumPy float to a Python float.
   If a column raises an exception, the value becomes ``None`` and the error goes to the log.
9. It writes the row to the ``exposure`` table.
10. It finds each section with the ``_PRIMARY`` suffix.
    Each of these sections is one detector.
11. For each detector, it applies ``DETECTOR_MAPPING`` and collects the row.
12. It writes all the detector rows to the ``ccdexposure`` table.
13. It commits the transaction.

Steps 9 to 13 are one transaction.
The ``exposure`` row and the ``ccdexposure`` rows of one image are therefore always consistent.

The detector name comes from the name of the section.
The first three characters are the raft, and the next three characters are the sensor.
For LATISS, the service changes the name ``R00_S00`` to ``RXX_S00``.

If the ``ccdexposure`` table has a ``day_obs`` column, the service copies ``day_obs`` and ``seq_num``
from the exposure row.
Schema version 3.2.0 added these columns.

The column mappings
===================

Five dictionaries control which header keyword fills which column.
A key is always a ConsDB column name.

.. list-table::
   :header-rows: 1
   :widths: 30 22 48

   * - Dictionary
     - Target table
     - Source
   * - ``KW_MAPPING``
     - ``exposure``
     - Header keywords, for all the instruments.
   * - ``LATISS_MAPPING``, ``LSSTCAM_MAPPING``, ``LSSTCOMCAM_MAPPING``, ``LSSTCOMCAMSIM_MAPPING``
     - ``exposure``
     - Header keywords, for one instrument.
   * - ``OI_MAPPING``
     - ``exposure``
     - Attributes of the ``ObservationInfo`` object.
   * - ``DETECTOR_MAPPING``
     - ``ccdexposure``
     - Header keywords of one detector section.
   * - ``TOPIC_MAPPING``
     - None
     - The Kafka topic name of each instrument.

The format of a value
---------------------

A value has one of two forms.

A **string** names the source keyword.
The service copies the value with no change:

.. code-block:: python

   "band": "FILTBAND",

A **tuple** starts with a function.
The other items are the arguments of that function.
Each argument is itself a mapping value, so a tuple can contain a tuple:

.. code-block:: python

   "s_region": (fp_region_ivoa, "vertices", "IMGTYPE"),

``process_column()`` and ``process_oi_column()`` read these values.
If one argument is missing, the result is ``None`` and the function does not run.

``OI_MAPPING`` accepts one more form.
If the item after the function is the string ``ACCEPTS_NULL``, the function runs even when an
argument is ``None``.
The ``azimuth``, ``altitude``, and ``zenith_distance`` columns use this form, because
``altaz_midpoint()`` selects between two sources of data.

Sky regions
-----------

Four columns hold the sky position of the image:

- ``s_region`` in ``exposure`` and in ``ccdexposure`` holds an IVOA polygon.
  The unit is degrees.
- ``pgs_region`` in ``exposure`` and in ``ccdexposure`` holds a pgSphere ``spoly`` literal.
  The unit is radians.

``get_vertices()`` computes the four corners of each CCD from the boresight and the rotator angle.
``fp_region()`` then selects the corners that make the shape of the focal plane.
Each instrument has its own list of corners, because the shape of each focal plane is different.

All four columns are ``None`` if the image type is not ``OBJECT``.

.. _hinfo-selective:

Selective column updates
========================

``EXP_COLUMNS_TO_UPDATE`` and ``CCD_COLUMNS_TO_UPDATE`` limit the columns that the service writes.
Put a colon between two column names:

.. code-block:: bash

   EXP_COLUMNS_TO_UPDATE=s_region:pgs_region

``parse_columns_to_update()`` adds the primary key columns to your list.
For ``exposure`` these columns are ``exposure_id``, ``exposure_name``, ``day_obs``, ``seq_num``, and
``controller``.
For ``ccdexposure`` these columns are ``ccdexposure_id``, ``exposure_id``, ``day_obs``, ``seq_num``,
and ``detector``.

The value ``@skip`` in ``CCD_COLUMNS_TO_UPDATE`` stops all work on the ``ccdexposure`` table.

.. important::

   These two variables also change how the service writes a row that is already present.

   With no value, the service uses ``ON CONFLICT DO NOTHING``.
   It keeps the row that is present.

   With a value, ``process_local_path()`` uses ``ON CONFLICT DO UPDATE``.
   It writes the new values over the row that is present.

   Use these variables to fill in a new column for images from the past.

.. _hinfo-logging:

Logging
=======

``setup_logging()`` in ``utils.py`` makes the logger with the name ``consdb.hinfo``.
The default level is INFO, and the messages go to standard error.
The logger of ``astro_metadata_translator`` is set to ERROR, because it is very loud.

Use ``LOG_CONFIG`` to change a level:

.. code-block:: bash

   LOG_CONFIG=consdb.hinfo=DEBUG

Where to make a change
======================

.. list-table::
   :header-rows: 1
   :widths: 46 54

   * - Task
     - Location
   * - Add a column from a header keyword
     - ``KW_MAPPING``, or the mapping of one instrument.
   * - Add a column from translated metadata
     - ``OI_MAPPING``.
   * - Add a per-detector column
     - ``DETECTOR_MAPPING``.
   * - Add a computed value
     - Write a function, then name it in the first item of a tuple.
   * - Add an instrument
     - ``get_instrument_dict()``, ``TOPIC_MAPPING``, and a new instrument mapping.
   * - Change the shape of the focal plane
     - ``fp_region()``.

A new column must be in the database before the service can write to it.
The :doc:`../contributor-guide/adding-columns` page gives that procedure.
