##########
User Guide
##########

Introduction
============

The Consolidated Database (ConsDB) stores metadata about images that have been taken with the Rubin Observatory (including the LSSTCam, LSSTComCam, and LATISS instruments).
Its general goals and architecture are described in `DMTN-227 <https://dmtn-227.lsst.io/>`__.

ConsDB is targeted at Rubin staff for processing, analysis, engineering, debugging, and other internal uses.
It is not exposed to Rubin data rights holders at this time.

Similar (though more limited in scope) information is available through ObsLocTAP, the Butler Registry, visit summary Parquet tables, and other data products.

The following sections describe the contents of the Consolidated Database and provide information on how to access it.

What is Consolidated Database?
==============================

ConsDB is a per-image/per-visit metadata database.  For each image taken at the observatory, it
gathers metadata from many sources into a single place.  Some of that data is easy to retrieve from
its original source; some is not easy at all.

This aggregation serves two purposes.  First, it provides a tool for observatory engineering and
diagnostics, supporting efforts to understand the observatory's behavior and improve its
performance.  Second, it offers easy access to metadata in cases where using the original source of
truth is impractical, whether because of access restrictions (as when the Nightly Digest reads it)
or because of computational complexity (as with the Transformed EFD).

It is equally important to understand what ConsDB is not.  It is not itself a source of truth for
any observatory data: everything it holds can be reconstructed from other sources.  Nor, as noted
above, is it a tool for scientists outside the project. Its intended audience is internal members of
the project who have a pre-existing familiarility with the idiosyncrasies of Rubin data.


.. toctree::
   :maxdepth: 1

   schemas
   transformed-efd
   flexible-metadata
   tap-clients
   rest-api-and-clients
   sql-clients

Choosing an access method
=========================

.. list-table::
   :header-rows: 1
   :widths: 16 30 30 24

   * - Method
     - Use it for
     - Where
     - Page
   * - TAP
     - Stable, standards-based reads from notebooks and astronomy tools.
     - USDF only.
     - :doc:`tap-clients`
   * - REST API
     - Scripted reads from any language, schema introspection, and all writes.
     - Summit, test stands, and USDF.
     - :doc:`rest-api-and-clients`
   * - SQL
     - The fastest reads, and full PostgreSQL syntax.
     - From inside the network of each site.
     - :doc:`sql-clients`

The Transformed EFD schemas are available through all three methods, but only at the USDF, because that is where the service that fills them runs.

Terms
=====

.. glossary::

   day_obs
      The observing night of an image, as an integer in the form ``YYYYMMDD``.
      The night rolls over at local noon, so every image of one night has the same value.

   seq_num
      The sequence number of an image within its ``day_obs``, starting at 1.

   exposure
      One readout of the camera. The ``exposure`` table has one row for each.

   visit
      A unit of observation for science processing. In the current survey design, every exposure is one visit, and the ``visit1`` tables are views of the ``exposure`` tables.

   CCD exposure
      The part of one exposure read from one detector. The ``ccdexposure`` table has about 200 rows for each LSSTCam exposure.

   quicklook
      The tables written by Rapid Analysis shortly after each image, with measurements made on the image.

   Header Service
      The Summit service that writes the metadata of each image as a YAML file. ConsDB reads those files through ``hinfo``.

   Rapid Analysis
      The Summit service that processes each image as it is taken and writes the quicklook tables.

   EFD
      The Engineering Facilities Database, the time series of every telemetry topic. The Transformed EFD summarizes it for each exposure.

   Transformed EFD
      The service, and the ``efd_*`` schemas, that hold the EFD summaries. Available at the USDF only.

   flexible metadata
      Key and value tables for experimental quantities that do not yet have a column of their own.

   pqserver
      The REST API service of ConsDB.

   TAP
      The IVOA Table Access Protocol, and the ``consdbtap`` service that provides it at the USDF.

   sdm_schemas
      The repository that defines every ConsDB schema in YAML, and the source of the schema browser.

   USDF
      The United States Data Facility at SLAC, where the replica of the Summit database and most users are.

   BTS, TTS
      The Base Test Stand and the Tucson Test Stand, which have their own copies of ConsDB for testing.
