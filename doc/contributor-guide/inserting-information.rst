#####################
Inserting Information
#####################

Four tools can be used to insert information into ConsDB.

- `ConsDB Python client library <https://github.com/lsst-so/summit_utils/blob/main/python/lsst/summit/utils/consdbClient.py>`__ in ``summit_utils``

  - This library is currently implemented using the Web service API, but it can be changed in the future to use Sasquatch.

- `ConsDB Web service API <https://usdf-rsp.slac.stanford.edu/consdb/docs/>`__

  - The Web service API (pqserver) provides some of the same advantages as Sasquatch, but it does not provide any buffering, retries, or resiliency.  We hope to phase out its usage when Sasquatch becomes available.

- Direct SQL ``INSERT``. This is discouraged. Currently only the ``hinfo`` service uses this
  method. Appropriate credentials would have to be arranged if you need this in a new data source.

Using the REST API
==================

The :doc:`../user-guide/rest-api-and-clients` page gives the endpoints and the interactive documentation gives their parameters.
A producer should follow these rules.

- Identify a row by ``day_obs`` and ``seq_num`` (and ``detector``), with the ``by_seq_num`` endpoints.
  The endpoints that take a single-column identifier remain for existing clients.
- Send many rows in one request with the bulk endpoint when you can.
  One request with fifty rows is one SQL statement; fifty requests are fifty.
- Send ``u=1`` if you retry a request after a failure, so that a row that did arrive is updated instead of rejected.
- Write a row only after the ``exposure`` or ``ccdexposure`` row of the image exists.
  The foreign keys reject the row otherwise.
  The Header Service writes those rows within seconds of the image, through ``hinfo``.
- Send every column that the table declares as not nullable, and only columns that the table has.
  A request that lacks a required column, or that names a column the table does not have, is rejected with the names of those columns.

A minimal request that writes one row with ``curl``:

.. code-block:: bash

   curl -s -X POST -H "Content-Type: application/json" \
       -d '{"values": {"mount_jitter_rms": 0.12, "psf_sigma_median": 1.9}}' \
       "http://consdb-pq.consdb:8080/consdb/insert/lsstcam/exposure_quicklook/by_seq_num/20250421/17?u=1"

The example names two columns for illustration; a real request must supply every column that the table requires.

