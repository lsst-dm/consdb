#####################
Inserting Information
#####################

Four tools can be used to insert information into ConsDB.

- `Sasquatch <https://sasquatch.lsst.io/user-guide/sendingdata.html>`__

  - Sasquatch will be configured to write via a Kafka Connector to tables in ConsDB.  This should become the preferred interface for data sources to insert information.  It provides isolation from SQL details (and does not require a SQL client library), and it can be used from any programming language.  The Kafka messaging system provides resiliency.
  - `REST Proxy <https://sasquatch.lsst.io/user-guide/restproxy.html>`__
  - `Direct Kafka messages <https://sasquatch.lsst.io/user-guide/directconnection.html>`__

- `ConsDB Python client library <https://github.com/lsst-sitcom/summit_utils/blob/main/python/lsst/summit/utils/consdbClient.py>`__ in ``summit_utils``

  - This library is currently implemented using the Web service API, but it can be changed in the future to use Sasquatch.

- `ConsDB Web service API <https://usdf-rsp.slac.stanford.edu/consdb/docs/>`__

  - The Web service API (pqserver) provides some of the same advantages as Sasquatch, but it does not provide any buffering, retries, or resiliency.  We hope to phase out its usage when Sasquatch becomes available.

- Direct SQL ``INSERT``.  This is discouraged.  Appropriate credentials would have to be arranged.
