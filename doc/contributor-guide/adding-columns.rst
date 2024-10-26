##############
Adding Columns
##############

Structure
=========

- ConsDB content must relate to exposures or visits or observations structured like exposures.  General time series should go in the Engineering and Facilities Database (EFD).
- ConsDB content should generally be scalar values.  Large amounts of data, especially arrays or images or cubes, should generally go into the Large File Annex (LFA).
- Avoid arrays expressed as individual columns (e.g. ``something0``, ``something1``, ``something2``) where possible, as this increases the number of columns drastically (and there is `a limit <https://www.postgresql.org/docs/current/limits.html>`_), makes it hard to query (``SELECT`` clauses need to list all of these individually, and ``WHERE`` clauses may need to include large ``OR`` or ``AND`` conditions), and potentially requires a lot of database storage space.
- Columns should be named in all lowercase with underscore (``_``) separators, also known as "snake_case".

Data sources
============

- Columns added to the ``exposure`` and ``ccdexposure`` tables must be derived from the Header Service running at the Summit for a given instrument, which extracts information from the EFD in real time and is designed to provide information critical for Alert Production.  (This service also populates the ``visit1`` and ``ccdvisit1`` views.)  Changes must typically be coordinated with both the Header Service and the ConsDB teams, in addition to being added to `sdm_schemas <https://github.com/lsst/sdm_schemas>`__.
- The source for the ``exposure_efd*`` tables is the EFD Transformation service running at the US Data Facility, which extracts information from the EFD in batches and is designed for all other EFD data.  It has its own configuration.
- Ensure that the data source for the table to which the column is being added will in fact produce that column.

Column descriptions
===================

- Make sure the description is understandable to a non-staff scientist, and try to avoid internal jargon.
- Include `units <https://www.ivoa.net/documents/VOUnits/>`__ for measurements.  Note that these should follow IVOA standards, not Astropy unit standards.
- Include a `Unified Content Descriptor (UCD) <https://ivoa.net/documents/UCD1+/20230125/index.html>`__ indicating the meaning of the column.
