####################
REST API and Clients
####################

A REST API is available to access ConsDB.
It can be used to query the database, including its schema.
It can also be used to insert or update rows in the database, although this should be reserved for production services or maintenance.
(The modification interface may be restricted to a particular token authorization scope in the future.)

The REST API is implemented by a service called the `pqserver <https://github.com/lsst-dm/consdb/blob/main/python/lsst/consdb/pqserver.py>`__ (which stands for "publish/query").

Connection information
======================

Summit
------

Within the Summit Kubernetes cluster (including all notebooks and services running on that cluster), use the connection URL ``http://consdb-pq.consdb:8080/consdb``.

USDF
----

Inside the USDF RSP (i.e. from a notebook or an authenticated RSP service), use the connection URL ``http://consdb-pq.consdb:8080/consdb``.
You will need to add ``.consdb`` to the ``no_proxy`` environment variable (``set no_proxy=$no_proxy,.consdb`` in a Terminal tab, ``os.environ["no_proxy"] += ",.consdb"`` in a notebook) to bypass the S3DF Squid proxy.

Outside the USDF RSP, including access from the sdfiana interactive machines, use the connection URL ``https://usdf-rsp.slac.stanford.edu/consdb``.
There is no need for proxy manipulation in this case.
An authorized USDF RSP token with ``read:image`` scope (may change to ``read:tap`` later) is required.
See `the RSP documentation <https://rsp.lsst.io/guides/auth/creating-user-tokens.html>`__ for instructions on creating a token.
Best practice is to keep the token in a file that is readable only by you (Unix mode 600).


API documentation
=================

Full documentation for the REST API and in-browser access to it are available via `Swagger interface <https://usdf-rsp.slac.stanford.edu/consdb/docs>`__.


REST API clients
================

Two Python client libraries are available that use the REST API to access ConsDB.

``lsst.summit.utils`` is available via ``eups distrib install summit_utils``.
It contains a ``ConsDbClient`` class and some convenience functions.
Results are returned as Astropy Tables.
The source, with embedded docstrings, is available `here <https://github.com/lsst-so/summit_utils/blob/main/python/lsst/summit/utils/consdbClient.py>`__.

``rubin_nights`` provides access to many data sources that support survey scheduling and performance evaluation, including ConsDB.
It is documented at `rubin-nights.lsst.io <https://rubin-nights.lsst.io/>`__, including a specific `ConsDB REST API client <https://rubin-nights.lsst.io/query_api.html#rubin_nights.consdb_query.ConsDbFastAPI>`__.
