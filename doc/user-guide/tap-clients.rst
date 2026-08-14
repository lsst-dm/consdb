###########
TAP Clients
###########

The `TAP <https://www.ivoa.net/documents/TAP/>`__ interface is the "official" required target for retrieving ConsDB data.
It provides the most stable, standards-compliant access method.
Asynchronous connections to TAP are recommended.

.. note::

   Columns holding JSON data are exposed through TAP as text, and ADQL provides no JSON operators.
   Their contents therefore cannot be searched or unpacked within a TAP query, unlike a
   :doc:`pqserver <rest-api-and-clients>` or :doc:`SQL <sql-clients>` query, which can use the
   native PostgreSQL JSON operators. A TAP query can still retrieve such a column in full and parse
   the JSON on the client side.

Connection information
======================

The ConsDB TAP service is only deployed at USDF within its Rubin Science Platform instances.
Accordingly, USDF RSP authentication is required to use it.

The production service URL is ``https://usdf-rsp.slac.stanford.edu/api/consdbtap/``.

Additional services run at ``usdf-rsp-dev.slac.stanford.edu`` and ``usdf-rsp-int.slac.stanford.edu`` for development purposes.

Each service can be tested for availability and capabilities (even by unauthenticated users) according to the TAP standard at, e.g., ``https://usdf-rsp.slac.stanford.edu/api/consdbtap/availability`` or ``https://usdf-rsp.slac.stanford.edu/api/consdbtap/capabilities``.
Those URLs return XML data but are mostly human-readable.


Notebook access
===============

Within a notebook at the USDF RSP, all that is necessary to use the ConsDB TAP service is:

.. code-block:: python

   from lsst.rsp import get_tap_service
   service = get_tap_service("consdbtap")

Token management is handled automatically.

The `DP1 tutorial notebooks for TAP access <https://dp1.lsst.io/tutorials/notebook/index.html#catalog-access>`__ provide a useful introduction to TAP, but tutorial notebook 102.1 section 4.3 "Use spatial constraints" does not apply to ConsDB.

Here are some very simple examples extracted from the tutorials; much more complex queries can be submitted, although there are limits on the size of the result sets that can be returned.

Schemas can be listed using:

.. code-block:: python

   results = service.search('SELECT * FROM tap_schema.schemas')
   results.to_table()

Tables in a schema can be listed using:

.. code-block:: python

   query = "SELECT * FROM tap_schema.tables " \
        "WHERE tap_schema.tables.schema_name = 'cdb_lsstcam'" \
        "ORDER BY table_index ASC"
   results = service.search(query).to_table()
   results

Columns can be listed using:

.. code-block:: python

   query = "SELECT column_name, datatype, description, unit " \
        "FROM tap_schema.columns " \
        "WHERE table_name = 'cdb_lsstcam.exposure'"
   results = service.search(query).to_table()
   results

Information about a particular exposure can be selected using:

.. code-block:: python

   query = "SELECT s_ra, s_dec, band " \
        "FROM cdb_lsstcam.exposure " \
        "WHERE day_obs=20250415 and seq_num=230"
   job = service.submit_job(query)
   job.run()
   job.wait(phases=['COMPLETED', 'ERROR'])
   print('Job phase is', job.phase)
   if job.phase == 'ERROR':
       job.raise_if_error()
   assert job.phase == 'COMPLETED'
   results = job.fetch_result().to_table()
   results
   job.delete()


TAP queries use ADQL, the Astronomical Data Query Language, which is close to SQL.
The `ADQL 2.1 specification <https://www.ivoa.net/documents/ADQL/>`__ gives the full language, and the ADQL tutorials in the `DP1 documentation <https://dp1.lsst.io/tutorials/index.html>`__ give an introduction with Rubin examples.
A join between two ConsDB tables looks the same as in SQL, and the ``TOP`` keyword takes the place of ``LIMIT``:

.. code-block:: python

   query = "SELECT TOP 20 e.day_obs, e.seq_num, e.exp_time, q.psf_sigma_median " \
        "FROM cdb_lsstcam.exposure AS e " \
        "JOIN cdb_lsstcam.visit1_quicklook AS q " \
        "ON e.day_obs = q.day_obs AND e.seq_num = q.seq_num " \
        "WHERE e.day_obs = 20250415 AND e.img_type = 'science'"
   results = service.search(query).to_table()

The column descriptions that TAP returns come from the ``sdm_schemas`` YAML files, through the TAP schema container.
After a schema migration, a new column is visible through SQL and the REST API before it is visible through TAP, because the TAP schema container must be rebuilt and deployed (see :doc:`../operator-guide/schema-migration-process`).

Client access
=============

Third-party TAP clients such as PyVO and TOPCAT can also be used with the TAP service.
`The examples for DP1 <https://dp1.lsst.io/tutorials/api/index.html#how-to-rsp-functionality>`__ show how to configure the clients, although the connection URL should be the ConsDB version given above.

To access the USDF RSP from an external client, you will need an authorized token with ``read:tap`` scope to use ``consdbtap``, or ``read:image`` scope for the ``pqserver`` REST app.
See `the RSP documentation <https://rsp.lsst.io/guides/auth/creating-user-tokens.html>`__ for instructions on creating a token.
