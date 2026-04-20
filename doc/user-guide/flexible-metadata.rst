#################
Flexible Metadata
#################

Goals
=====

The flexible metadata tables provided within each instrument's schema support metadata that needs to be added rapidly, especially if it is not expected to be needed permanently.
This facility, available at both exposure and CCD-exposure levels of detail, enables experimental, investigatory, debug-oriented values to be inserted into the database without a long-term commitment.
It should not be used for values that are part of automated control loops.

Replication
===========

Since these tables are replicated from the Summit to USDF, insertion of flexible metadata should only occur at the Summit, although multiple systems there could write values.
If flexible metadata is needed at USDF, additional USDF-only tables would need to be created.
(Writing rows into the replication destination makes recovery after a replication pause or failure extremely difficult.)

Insertion
=========

To insert into the flexible metadata for a given instrument and level of detail (which is termed the observation type, either ``exposure`` or ``ccdexposure``), first define the metadata key to be added using a POST to the ``/flex/{instrument}/{obs_type}/addkey`` REST API endpoint.
The data content is a JSON object containing:

 - ``key``: The name of the added key
 - ``dtype``: Data type for the added key (``bool``, ``int``, ``float``, ``str``)
 - ``doc``: Documentation string for the new key (optional)
 - ``unit``: Unit for value (optional, must be an ``astropy.units.Unit``)
 - ``ucd``: IVOA Unified Content Descriptor (optional, must be valid by ``astropy.io.votable.ucd.check_ucd()``)

This API is also available via ``lsst.summit.utils.ConsDbClient`` as the ``add_flexible_metadata_key()`` method.

After the key has been added, values can be added or updated using a POST to the ``/flex/{instrument}/{obs_type}/obs/{obs_id}`` REST API endpoint.
The ``obs_id`` is either the ``exposure_id`` or ``ccdexposure_id`` as an integer.
(It will automatically be converted to ``day_obs`` and ``seq_num`` as needed.)
A ``?u=1`` query parameter can be added to the URL to indicate that the values should be updated rather than inserted if the primary key is already present.
The data content is a JSON object containing:

 - ``data``: a dictionary of key/value data to insert or update

For optimal performance, batch as many key/value pairs as possible into a single POST.
(Note, however, that the current implementation does a separate SQL insert and commit for each key/value pair, which is less than optimal.)

This API is also available via ``lsst.summit.utils.ConsDbClient`` as the ``insert_flexible_metadata()`` method.

Introspection
=============

The flexible metadata available for a given observation type (exposure or CCD-exposure) can be retrieved using a GET to the ``/flex/{instrument}/{obs_type}/schema`` REST API endpoint.
The result content is a JSON object containing key/tuple pairs, where each key is a flexible metadata key and each value is the ``dtype``, ``doc``, ``unit``, and ``ucd`` information for that key.

This API is also available via ``lsst.summit.utils.ConsDbClient`` as the ``get_flexible_metadata_keys()`` method.

Querying
========

The flexible metadata for a given observation (exposure or CCD-exposure) can be retrieved using a GET to the ``/flex/{instrument}/{obs_type}/obs/{obs_id}`` REST API endpoint.
The ``obs_id`` is either the ``exposure_id`` or ``ccdexposure_id`` as an integer.
(It will automatically be converted to ``day_obs`` and ``seq_num`` as needed.)
If one or more specific keys are desired, ``?k={key}`` or ``?k={key1}&k={key2}...`` query parameters can be added to the URL.
The result content is a JSON object containing key/value pairs.

This API is also available via ``lsst.summit.utils.ConsDbClient`` as the ``get_flexible_metadata()`` method.

In addition, a GET to the ``/query/{instrument}/{obs_type}/obs/{obs_id}`` REST API endpoint with optional query parameter ``?flex=1`` will include all available flexible metadata along with the normal "wide view" joined metadata columns for the given observation type and identifier.

This API is also available via ``lsst.summit.utils.ConsDbClient`` as the ``get_all_metadata()`` method.

Finally, a SQL query can be used with the ``/query`` REST API endpoint to retrieve flexible metadata or use a flexible metadata value as a filter in a ``WHERE`` clause.
The query will need to join to the ``exposure_flexdata`` or ``ccdexposure_flexdata`` tables in the appropriate ``cdb_{instrument}`` schema using the ``obs_id`` column or the ``day_obs`` and ``seq_num`` column pair as the join key, giving the desired flexible metadata key in the ``WHERE`` clause.
Note that all flexible metadata values are stored as SQL character strings; they may require conversion to an appropriate data type for further computation or manipulation.
