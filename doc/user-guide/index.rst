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



.. toctree::
   :maxdepth: 1

   schemas
   transformed-efd
   flexible-metadata
   tap-clients
   rest-api-and-clients
   sql-clients
