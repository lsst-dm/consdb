###########
TAP Clients
###########

The `TAP <https://www.ivoa.net/documents/TAP/>`__ interface is the "official" required target for retrieving ConsDB data.
It provides the most stable, standards-compliant access method.
Asynchronous connections to TAP are recommended.

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


Client access
=============

Third-party TAP clients such as PyVO and TOPCAT can also be used with the TAP service.
`The examples for DP1 <https://dp1.lsst.io/tutorials/api/index.html#how-to-rsp-functionality>`__ show how to configure the clients, although the connection URL should be the ConsDB version given above.

To access the USDF RSP from an external client, you will need an authorized token with ``read:tap`` scope.
See `the RSP documentation <https://rsp.lsst.io/guides/auth/creating-user-tokens.html>`__ for instructions on creating a token.
