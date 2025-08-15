##############
Adding Columns
##############

.. _add-columns-checklist:

Checklist
=========
- Ensure that the structure of the data is suitable for ConsDB.
  See the :ref:`add-columns-structure` section below.

- Identify the source of the data.
  ConsDB does not produce any data itself, nor does the ConsDB team request that sources produce data.
  All values must be generated from other systems.
  See the :ref:`add-columns-data-sources` section below.

- Identify consumers of the data.
  ConsDB should not be write-only storage.

- Provide information about the requested columns including a brief description in the appropriate Confluence page: `Transformed EFD <https://rubinobs.atlassian.net/wiki/x/Ii7pAg>`__ or `Non-EFD <https://rubinobs.atlassian.net/wiki/x/GICzDg>`__.
  This provides an opportunity for discussion and comment on the suitability of the columns.

- For non-EFD columns, file a Jira ticket and start a corresponding pull request to modify the `sdm_schemas <https://github.com/lsst/sdm_schemas>`__ repository with appropriate entries for the desired columns.
  See the :ref:`add-columns-descriptions` section below for more details on how to write a good Felis description for a column.

  - Get the ``sdm_schemas`` pull request reviewed by a member of the Data Engineering team for syntax, description, unit, and IVOA compliance.

  - Get the ``sdm_schemas`` pull request reviewed by a member of the ConsDB team for structure, table location, and data source.

- For Transformed EFD columns, file a Jira ticket to request that the a member of the ConsDB team will arrange to include the columns in the EFD Transformer configuration.
  You will need to provide the Felis description information in addition to how the value is to be computed from the EFD.

- The ConsDB team will then generate a schema migration and deploy it at an appropriate time.
  After the schema has been migrated, the data source can begin to populate it.


.. _add-columns-structure:

Structure
=========

- ConsDB content must relate to exposures or visits or observations structured like exposures.  General time series should go in the Engineering and Facilities Database (EFD).
- ConsDB content should generally be scalar values.  Large amounts of data, especially arrays or images or cubes, should generally go into the Large File Annex (LFA).
- Avoid arrays expressed as individual columns (e.g. ``something0``, ``something1``, ``something2``) where possible, as this increases the number of columns drastically (and there is `a limit <https://www.postgresql.org/docs/current/limits.html>`__), makes it hard to query (``SELECT`` clauses need to list all of these individually, and ``WHERE`` clauses may need to include large ``OR`` or ``AND`` conditions), and potentially requires a lot of database storage space.
- Columns should be named in all lowercase with underscore (``_``) separators, also known as "snake_case".

.. _add-columns-data-sources:

Data sources
============
Possible sources of data include:

- EFD:

  - Determine whether the information is required at the Summit or if the information is required with very low latency (less than a few minutes).
    In those cases, the Header Service is the recommended source for ConsDB.
    Arrangements must be made for the data to appear in the headers before ConsDB can store it.
    Arrangements must also be made with the ConsDB team for the value to be extracted from the headers.
    This data will go into the ``exposure`` or ``ccdexposure`` table.

  - If the original data source is the EFD but the data is only needed at USDF and can wait for a few minutes before appearing, the Transformed EFD service should be used.
    This data will go into a ``*_efd`` table.

- A system (e.g. the Camera Control System), service (e.g. Rapid Analysis), or campaign/pipeline (e.g. Nightly Validation) executing at the Summit or USDF.
  This data will go into a table with a suffix specific to the source.

.. _add-columns-descriptions:

Column descriptions
===================

- Make sure the description is understandable to a non-staff scientist, and try to avoid internal jargon.
- Ensure that descriptions sufficiently explain the values within the columns, providing details like how they are summarized (if they are) or at what time point they are measured during the exposure.
- Explain what the column values can be used for if it's not self-evident.
- The description can be several sentences; completeness is more important than conciseness.
- Include `units <https://www.ivoa.net/documents/VOUnits/>`__ for measurements.  Note that these should follow IVOA standards, not Astropy unit standards.
- Include a `Unified Content Descriptor (UCD) <https://ivoa.net/documents/UCD1+/20230125/index.html>`__ indicating the meaning of the column.
