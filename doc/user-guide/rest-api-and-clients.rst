####################
REST API and Clients
####################

A REST API is available to access ConsDB.
It can be used to query the database, including its schema.
It can also be used to insert or update rows in the database, although this should be reserved for production services or maintenance.
(The modification interface may be restricted to a particular token authorization scope in the future.)

The REST API is implemented by a service called the `pqserver <https://github.com/lsst-dm/consdb/blob/main/python/lsst/consdb/pqserver.py>`__ (which stands for "Postgres Query").

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


Test Stands
-----------

The Base Test Stand (BTS) and Tucson Test Stand (TTS) have implementations of Consolidated Database.
The internal URL is the same: ``http://consdb-pq.consdb:8080/consdb``. There is no Squid proxy, so
there is no need to adjust the ``no_proxy`` environment variable. The test stands include Rapid
Analysis, but they do not provide consdbtap as a service.

The BTS base URL is ``base-lsp.lsst.codes`` and the TTS base URL ``tucson-teststand.lsst.codes``.
You will need to have VPN access for either of these test stands.

Endpoint families
=================

All endpoints are below the ``/consdb`` prefix of the connection URL.
The :ref:`rest-api-docs` section gives the interactive documentation, which lists every endpoint with its parameters and response model.
This page does not repeat that list.
It gives the purpose of each family and the behavior that the interactive documentation cannot show.
Most users of the REST API will need only the ``/query`` endpoint.

``/`` (root)
   Returns the name and version of the service, the list of instruments, the observation types (``exposure``, ``visit1``, ``ccdexposure``, ``ccdvisit1``), and the data types that the flexible metadata accepts.
   Call it first from a new client to discover what the site offers, and to read which version of ``pqserver`` is deployed.

``/query``
   Runs an arbitrary SQL query against the database.
   See :ref:`rest-api-query` below.

``/query/{instrument}/{obs_type}/obs/{obs_id}``
   Returns every column that ConsDB holds for one observation, joined from all the tables of that observation type.
   With the ``flex`` parameter, the flexible metadata is merged into the same result.
   This endpoint depends on the wide views, which are not yet present in any schema, so it returns an error at this time.
   The :doc:`../developer-guide/wide-views` page gives the status.

``/schema``, ``/schema/{instrument}``, ``/schema/{instrument}/{table}``
   List the available instruments, the tables for an instrument, and the columns of a table with their types and descriptions.
   The table name may be given with or without its ``cdb_{instrument}.`` prefix.

``/flex/{instrument}/{obs_type}/...``
   Defines keys and reads or writes values in the flexible metadata tables.
   The :doc:`flexible-metadata` page describes the workflow.

``/insert/{instrument}/{table}/by_seq_num/{day_obs}/{seq_num}`` and ``.../{detector}``
   Insert or update one row, identified by the multi-column key.
   These are the recommended forms for new code, because the multi-column keys are the declared primary keys of the tables.

``/insert/{instrument}/{table}/obs/{obs_id}``
   Insert or update one row, identified by the single-column key (``exposure_id``, ``ccdexposure_id``, and so on).
   This form remains for existing clients.
   Prefer the ``by_seq_num`` form in new code, because the single-column keys are deprecated (see :doc:`schemas`).

``/insert/{instrument}/{table}``
   Insert or update many rows in one request.
   The body maps each observation identifier to a dictionary of column values.
   All the rows go into the same table in one SQL statement, so this form is much faster than one request per row.

``/table_consistency/{instrument}/{day_obs}``
   Reports the consistency rule violations for one observing day.
   The path ``/table_consistency`` with no parameters serves an interactive web page for the same report.
   The :doc:`../operator-guide/monitoring` page gives the rules.

All the insert endpoints, including the flexible metadata insert, accept the ``u`` query parameter.
With ``u=0`` (the default), a row whose key is already present causes an error.
With ``u=1``, the request updates the row that is present.
Producers that retry a request after a failure should use ``u=1``.

A row in a table other than ``exposure`` or ``ccdexposure`` needs a parent row in one of those two tables, because the foreign keys require it.
A producer must therefore not write before the Header Service data for the image has arrived.

.. _rest-api-query:

The ``/query`` endpoint
=======================

Send a POST request with a JSON body that contains one ``query`` key:

.. code-block:: bash

   curl -s -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
       -d '{"query": "SELECT day_obs, seq_num, exp_time FROM cdb_lsstcam.exposure WHERE day_obs = 20250421 LIMIT 3"}' \
       https://usdf-rsp.slac.stanford.edu/consdb/query

The response is a JSON object with two keys.
``columns`` is the list of column names.
``data`` is a list of rows, and each row is a list of values in the same order as ``columns``:

.. code-block:: json

   {"columns": ["day_obs", "seq_num", "exp_time"],
    "data": [[20250421, 1, 30.0], [20250421, 2, 30.0], [20250421, 3, 15.0]]}

Values arrive as JSON types.
Timestamps arrive as strings, and you must parse them on the client side.
The two client libraries below do this for you.

Keep these limits in mind:

- The service returns at most one million rows.
  Rows beyond that limit are discarded, and the response does not say that it was cut.
  Put an explicit ``LIMIT`` in your query, or filter on ``day_obs``, when the full result could be large.
- A statement is cancelled after ten minutes.
- The service does not restrict the type of statement.
  A statement other than ``SELECT`` runs if the database role of the service permits it.
  The response to such a statement has one column named ``commit`` and one row.
- The ``commit`` query parameter controls the transaction.
  With ``commit=0``, the service rolls the transaction back after the statement.
  Use this to test a statement, or to run ``EXPLAIN``, without a permanent effect.

Error responses
===============

The service reports errors as JSON.
The HTTP status tells you which kind of error it is:

.. list-table::
   :header-rows: 1
   :widths: 14 40 46

   * - Status
     - Cause
     - Body
   * - 404
     - An unknown instrument, table, key, or observation type, or a value of the wrong type for a flexible metadata key.
     - ``message``, ``value``, and ``valid``, where ``valid`` lists the accepted values.
   * - 404
     - The observation is not present (per-observation query only).
     - ``detail``.
   * - 422
     - The request body does not match the model, for example an invalid unit or UCD in a flexible metadata key.
     - The standard FastAPI validation report.
   * - 500
     - The database rejected the statement, for example a SQL syntax error or a constraint violation.
     - ``message``, with the text of the database error.

Note that a bad value gives a 404, not a 400.
A client that looks for 400 to detect a bad table name must look for 404 instead.

Authentication and transport
============================

The service itself does not check credentials.
The Rubin Science Platform ingress at each site checks the token and forwards the request.
That is why the in-cluster URL needs no token and the external URL needs one.
It is also why the service must not be exposed outside the cluster without such an ingress.

Responses larger than about one kilobyte are compressed with gzip when the client accepts it.
Most HTTP libraries handle this transparently.
With ``curl``, add the ``--compressed`` option.

The local Compose stack described on the :doc:`../developer-guide/local-environment` page serves the same API at ``http://localhost:8888/consdb``, with no token.
Use it to test a client without touching a shared database.

.. _rest-api-docs:

API documentation
=================

The ``pqserver`` service gives its own API documentation in three forms.
Add one of these paths to the connection URL of your site:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Path
     - Content
   * - ``/docs``
     - The Swagger interface.
       It shows each endpoint, and you can send a request to the API from your browser.
   * - ``/redoc``
     - The ReDoc interface.
       It shows the same information as one page.
       This form is easier to read and to search, but you cannot send a request from it.
   * - ``/openapi.json``
     - The OpenAPI schema of the API.
       Use it to make a client, or to read the API with a different tool.

At the USDF, the three addresses are:

- `Swagger <https://usdf-rsp.slac.stanford.edu/consdb/docs>`__ --- an interactive form for each endpoint, from which you can send a request in your browser.
- `ReDoc <https://usdf-rsp.slac.stanford.edu/consdb/redoc>`__ --- the same information laid out as a single page, for reading and searching.
- `OpenAPI schema <https://usdf-rsp.slac.stanford.edu/consdb/openapi.json>`__ --- a machine-readable definition of the API, for generating a client or feeding another tool.

All three forms come from the same source, which is the code of the service.
They therefore always agree with the version of ``pqserver`` that is deployed at your site.

REST API clients
================

Two Python client libraries are available that use the REST API to access ConsDB.

``lsst.summit.utils`` is available via ``eups distrib install summit_utils``.
It contains a ``ConsDbClient`` class and some convenience functions.
Results are returned as Astropy Tables.
The source, with embedded docstrings, is available `here <https://github.com/lsst-so/summit_utils/blob/main/python/lsst/summit/utils/consdbClient.py>`__.

``rubin_nights`` provides access to many data sources that support survey scheduling and performance evaluation, including ConsDB.
It is documented at `rubin-nights.lsst.io <https://rubin-nights.lsst.io/>`__, including a specific `ConsDB REST API client <https://rubin-nights.lsst.io/query_api.html#rubin_nights.consdb_query.ConsDbFastAPI>`__.

``ConsDbClient`` covers the query, schema, flexible metadata, and insert endpoints, and it uses the ``by_seq_num`` form for inserts.
It does not cover the root endpoint or the table consistency report; use a plain HTTP request for those.
If you do not give it a URL, it reads the ``LSST_CONSDB_PQ_URL`` environment variable.

Both clients wrap the same ``/query`` endpoint, so the two examples below fetch the same rows and differ only in what they hand back.

``ConsDbClient`` takes the connection URL and token explicitly, and returns an Astropy Table.

.. code-block:: python

   from lsst.summit.utils import ConsDbClient

   client = ConsDbClient("https://usdf-rsp.slac.stanford.edu/consdb", token=token)
   table = client.query(
       "SELECT day_obs, seq_num, exp_time FROM cdb_lsstcam.exposure"
       " WHERE day_obs = 20250421 LIMIT 10"
   )

``rubin_nights`` works out the site and locates your RSP token itself, and returns a pandas DataFrame.

.. code-block:: python

   from rubin_nights.connections import get_clients

   consdb = get_clients()["consdb"]
   frame = consdb.query(
       "SELECT day_obs, seq_num, exp_time FROM cdb_lsstcam.exposure"
       " WHERE day_obs = 20250421 LIMIT 10"
   )
