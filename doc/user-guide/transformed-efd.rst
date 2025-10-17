Transformed EFD
===============


The Transformed EFD Dataset
---------------------------

Purpose and Context
~~~~~~~~~~~~~~~~~~~

This guide explains how to query the Transformed Engineering and Facilities Database (EFD) dataset. This dataset is part of the Vera C. Rubin Observatory's Consolidated Database (ConsDB), which combines information from multiple sources into a single format. The Transformed EFD tables contain summarized EFD telemetry, providing context for scientific analysis, such as instrument health and environmental conditions during observations.

Data Sources and Time Windows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The data originates from the EFD, a time-series database that stores high-frequency telemetry from observatory systems. The data in these tables is not the raw stream but has been aggregated over two time windows defined by the LSST Butler system:

- **By Exposure**: Data is summarized over the ``timespan`` of a single raw exposure.
- **By Visit**: Data is summarized over the ``timespan`` of a processed visit.

This link to Butler records ensures that every data point can be tied to a specific observational event.

Connecting to the Database
--------------------------

.. note::

   **Connection Methods**: The connection process may vary depending on your infrastructure or access method (direct database connection, TAP services, web interfaces, etc.). For the sake of understanding the data structure and query patterns, this documentation uses PostgreSQL syntax examples throughout.

Identifying the Correct Schema
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Data is organized into instrument-specific schemas to keep datasets separate and organized. This is important for writing correct queries, as you must specify the correct schema for your instrument.

Use the following mapping from instrument name to schema name when constructing queries:

- LATISS: ``efd_latiss``
- LSSTCam: ``efd_lsstcam``
- LSSTComCam: ``efd_lsstcomcam``

All queries must prepend the schema name to the table name. For example, to select data from the ``exposure_efd`` table for the LSSTCam instrument, the correct syntax is:

.. code-block:: sql

   SELECT * FROM efd_lsstcam.exposure_efd;

Understanding the Data Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The transformed EFD data structure is determined by configuration files that define which telemetry topics are processed and how they are transformed. All instruments use the same data model structure, but the specific columns and properties available depend on the instrument's configuration.

Key points about the data configuration:

- **Consistent Structure**: All instruments (LATISS, LSSTCam, LSSTComCam) use the same four table types with identical schemas
- **Instrument-Specific Content**: The actual columns and properties available depend on the telemetry topics configured for each instrument
- **Configuration-Driven**: The data you see in the database is determined by YAML configuration files that specify which EFD topics to process
- **Standardized Transformations**: Common transformation functions (mean, max, min, standard deviation, etc.) are applied consistently across instruments

To understand what data is available for a specific instrument, you can examine the configuration files or query the database schema directly.

Understanding the Database Schema
---------------------------------

The Four Core Tables
~~~~~~~~~~~~~~~~~~~~

The processing pipeline populates four tables for each instrument schema, generated from a master configuration to ensure consistency. The four tables are:

- ``exposure_efd``: Contains pivoted (columnar) data, with one row per exposure.
- ``visit1_efd``: Contains pivoted data, with one row per visit.
- ``exposure_efd_unpivoted``: Contains unpivoted (key-value) data related to exposures.
- ``visit1_efd_unpivoted``: Contains unpivoted (key-value) data related to visits.

The Pivoted vs. Unpivoted Data Model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The database uses both pivoted and unpivoted tables. This design is a practical choice to manage the large amount of telemetry data. The pivoted tables are optimized for ease of use and performance for common queries. The unpivoted tables provide a scalable solution for metrics that involve a large number of individual data points, such as readings from an array of sensors.

The unpivoted tables were created to handle cases where there were too many columns to include in a single table. Instead of creating hundreds of columns for every sensor, these metrics are stored in a key-value structure.

- **Pivoted Tables** (``exposure_efd``, ``visit1_efd``): These tables are the default choice for most analysis and contain the most common metrics. Each metric has its own column (e.g., ``mt_dome_temperature_mean``). This structure is intuitive for writing queries.

  .. note::

     Science Data Models:

     - LATISS: https://sdm-schemas.lsst.io/efd_latiss.html
     - LSSTCam: https://sdm-schemas.lsst.io/efd_lsstcam.html
     - LSSTComCam: https://sdm-schemas.lsst.io/efd_lsstcomcam.html

- **Unpivoted Tables** (``exposure_efd_unpivoted``, ``visit1_efd_unpivoted``): These tables contain data from a large array of similar sensors or any metric that generates too many values to be stored as separate columns, such as vibration sensor data or actuator forces. Data is stored in a key-value format using three main columns:

  - ``property``: Corresponds to the base name of the measurement (e.g., ``mt_vibration_data_mean``).
  - ``field``: Identifies the specific sensor or data point (e.g., ``accelerationPSDX10``).
  - ``value``: The measured value for that field and property.

  This model is flexible for storing large sets of related data but requires more complex queries to analyze.

Core Identifying Columns
~~~~~~~~~~~~~~~~~~~~~~~~

These columns serve as primary keys and are used to identify records and join data between tables.

.. important::

   **Indexed Columns**:

   - **Standard tables** (``exposure_efd``, ``visit1_efd``): Only ``day_obs`` and ``seq_num`` are indexed
   - **Unpivoted tables** (``exposure_efd_unpivoted``, ``visit1_efd_unpivoted``): ``day_obs``, ``seq_num``, ``exposure_id``, ``property``, and ``field`` are indexed

   For optimal query performance, always use these indexed columns in your WHERE clauses and JOIN conditions.

- ``day_obs`` (integer): The date of observation in ``YYYYMMDD`` format (e.g., ``20250806``). Primary key column.
- ``seq_num`` (integer): The sequence number of the observation within that day. Primary key column.
- ``exposure_id`` (long): The unique Butler identifier for the exposure. Has a unique constraint in standard tables but is indexed in unpivoted tables.
- ``visit_id`` (long): The unique Butler identifier for the visit. Has a unique constraint in standard tables but is indexed in unpivoted tables.
- ``created_at`` (timestamp): The timestamp indicating when the row was generated. Not indexed.

Data Availability and Processing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Understanding when and how data becomes available is important for effective querying:

- **Processing Schedule**: Data is processed in regular intervals, typically every few minutes
- **Data Latency**: There may be a delay of 5-15 minutes between when observations occur and when transformed data becomes available
- **Missing Data**: Some exposures or visits may not have transformed EFD data if:
  - The EFD telemetry was not available during the observation
  - The transformation process encountered errors
  - The observation occurred before the transformation service was active
- **Data Completeness**: Not all telemetry topics may be available for every observation, depending on instrument configuration and operational status

To check data availability for a specific time period, you can query the count of records for your time range of interest using the indexed ``day_obs`` column.

Querying Transformed Data: Practical Examples
----------------------------------------------

Basic Pivoted Queries
~~~~~~~~~~~~~~~~~~~~~

**Example 1: Retrieve environmental data for a specific night**

This query fetches environmental conditions for all LSSTCam exposures on a given night.

.. code-block:: sql

   SELECT
       day_obs,
       seq_num,
       exposure_id,
       mt_dome_temperature_mean,
       mt_salindex110_sonic_temperature_mean,
       mt_salindex110_wind_speed_0_mean
   FROM
       efd_lsstcam.exposure_efd
   WHERE
       day_obs = 20250806
   ORDER BY
       seq_num
   LIMIT 100;

**Example 2: Find visits with good seeing conditions**

This query finds all visits for the LSSTCam instrument where the DIMM seeing was better than 0.7 arcseconds.

.. code-block:: sql

   SELECT
       day_obs,
       seq_num,
       visit_id,
       mt_dimm_fwhm_mean,
       mt_dome_temperature_mean
   FROM
       efd_lsstcam.visit1_efd
   WHERE
       day_obs = 20250806
       AND mt_dimm_fwhm_mean < 1.0
   ORDER BY
       seq_num
   LIMIT 50;

Basic Unpivoted Queries
~~~~~~~~~~~~~~~~~~~~~~~~

Querying unpivoted tables requires filtering on the ``property`` and ``field`` columns to isolate the desired metric. The ``property`` column corresponds to the ``name`` of a transformation, while the ``field`` column corresponds to a specific sensor or measurement source.

**Example 1: Find a single unpivoted value**

This query retrieves the mean vibration for a specific accelerometer sensor (``accelerationPSDX10``) during a given LSSTCam exposure.

.. code-block:: sql

   SELECT
       value
   FROM
       efd_lsstcam.exposure_efd_unpivoted
   WHERE
       day_obs = 20250806
       AND seq_num = 55
       AND property = 'mt_vibration_data_mean'
       AND field = 'accelerationPSDX10'
   LIMIT 1;

**Example 2: Pivoting unpivoted data in a query**

The following query retrieves multiple vibration sensor readings for a single exposure and displays them as if they were in separate columns, effectively "pivoting" the data within the SQL query itself.

.. code-block:: sql

   SELECT
       day_obs,
       seq_num,
       exposure_id,
       MAX(CASE WHEN field = 'accelerationPSDX0' THEN value END) AS psdx0,
       MAX(CASE WHEN field = 'accelerationPSDX1' THEN value END) AS psdx1,
       MAX(CASE WHEN field = 'accelerationPSDY0' THEN value END) AS psdy0,
       MAX(CASE WHEN field = 'accelerationPSDY1' THEN value END) AS psdy1
   FROM
       efd_lsstcam.exposure_efd_unpivoted
   WHERE
       day_obs = 20250806
       AND seq_num = 55
       AND property = 'mt_vibration_data_mean'
   GROUP BY
       day_obs, seq_num, exposure_id
   LIMIT 1;

Joining Tables
~~~~~~~~~~~~~~

**Example 1: Combine standard metrics with specific sensor readings for a single exposure**

This query joins ``exposure_efd`` with ``exposure_efd_unpivoted`` to show the dome temperature alongside specific vibration sensor readings for an LSSTCam exposure.

.. code-block:: sql

   SELECT
       piv.day_obs,
       piv.seq_num,
       piv.exposure_id,
       piv.mt_dome_temperature_mean,
       unpiv.field AS sensor_name,
       unpiv.value AS vibration_psd
   FROM
       efd_lsstcam.exposure_efd AS piv
   JOIN
       efd_lsstcam.exposure_efd_unpivoted AS unpiv
       ON piv.day_obs = unpiv.day_obs AND piv.seq_num = unpiv.seq_num
   WHERE
       piv.day_obs = 20250806
       AND piv.seq_num = 55
       AND unpiv.property = 'mt_vibration_data_mean'
   LIMIT 10;

**Example 2: Combine and Pivot Data for a Specific Day**

This query combines data for all exposures on a specific day and uses conditional aggregation to pivot the unpivoted sensor data. The ``MAX(CASE WHEN... END)`` expressions transform the key-value pairs from the ``unpivoted`` table into distinct columns, creating a "wide" table format that is easier to analyze.

.. code-block:: sql

   SELECT
       piv.day_obs,
       piv.seq_num,
       piv.exposure_id,
       piv.mt_pointing_mount_position_ra_mean,
       MAX(CASE WHEN unpiv.field = 'accelerationPSDX0' THEN unpiv.value END) AS vibration_psd_x0,
       MAX(CASE WHEN unpiv.field = 'accelerationPSDX1' THEN unpiv.value END) AS vibration_psd_x1,
       MAX(CASE WHEN unpiv.field = 'accelerationPSDY0' THEN unpiv.value END) AS vibration_psd_y0,
       MAX(CASE WHEN unpiv.field = 'accelerationPSDY1' THEN unpiv.value END) AS vibration_psd_y1
   FROM
       efd_lsstcam.exposure_efd AS piv
   JOIN
       efd_lsstcam.exposure_efd_unpivoted AS unpiv
       ON piv.day_obs = unpiv.day_obs AND piv.seq_num = unpiv.seq_num
   WHERE
       piv.day_obs = 20250806
       AND unpiv.property = 'mt_vibration_data_mean'
   GROUP BY
       piv.day_obs, piv.seq_num, piv.exposure_id, piv.mt_pointing_mount_position_ra_mean
   ORDER BY
       piv.seq_num
   LIMIT 50;

Advanced Query Examples
~~~~~~~~~~~~~~~~~~~~~~~

**Example 1: Environmental Conditions Over Time Range**

This query retrieves environmental data for a specific time range using indexed columns:

.. code-block:: sql

   SELECT
       day_obs,
       seq_num,
       exposure_id,
       mt_dome_temperature_mean,
       mt_dimm_fwhm_mean,
       mt_salindex110_sonic_temperature_mean
   FROM
       efd_lsstcam.exposure_efd
   WHERE
       day_obs BETWEEN 20250801 AND 20250807
   ORDER BY
       day_obs, seq_num
   LIMIT 200;

**Example 2: Data Completeness Analysis**

This query shows how to check data completeness for instrument metrics:

.. code-block:: sql

   SELECT
       day_obs,
       COUNT(*) as total_exposures,
       COUNT(mt_dome_temperature_mean) as dome_temp_measurements,
       COUNT(mt_dimm_fwhm_mean) as seeing_measurements,
       COUNT(mt_salindex110_sonic_temperature_mean) as sonic_temp_measurements
   FROM
       efd_lsstcam.exposure_efd
   WHERE
       day_obs = 20250806
   GROUP BY
       day_obs;

**Example 3: Mount Performance Analysis**

Analyze mount encoder performance and pointing accuracy:

.. code-block:: sql

   SELECT
       day_obs,
       seq_num,
       exposure_id,
       mt_azimuth_encoder_absolute_position_0_rms_jitter,
       mt_elevation_encoder_absolute_position_0_rms_jitter,
       mt_pointing_mount_position_ra_mean,
       mt_pointing_mount_position_ra_stddev
   FROM
       efd_lsstcam.exposure_efd
   WHERE
       day_obs = 20250806
       AND mt_azimuth_encoder_absolute_position_0_rms_jitter IS NOT NULL
   ORDER BY
       seq_num
   LIMIT 100;

**Example 4: Wind and Seeing Conditions**

Query for good observing conditions:

.. code-block:: sql

   SELECT
       day_obs,
       seq_num,
       exposure_id,
       mt_dimm_fwhm_mean,
       mt_salindex110_wind_speed_0_mean,
       mt_salindex110_sonic_temperature_mean
   FROM
       efd_lsstcam.exposure_efd
   WHERE
       day_obs = 20250806
       AND mt_dimm_fwhm_mean < 0.8
       AND mt_salindex110_wind_speed_0_mean < 10.0
   ORDER BY
       seq_num
   LIMIT 50;

**Example 5: Unpivoted Data Analysis**

Query unpivoted data using the indexed columns for efficient performance:

.. code-block:: sql

   SELECT
       day_obs,
       seq_num,
       exposure_id,
       property,
       field,
       value
   FROM
       efd_lsstcam.exposure_efd_unpivoted
   WHERE
       day_obs = 20250806
       AND property = 'mt_vibration_data_mean'
       AND field IN ('accelerationPSDX0', 'accelerationPSDX1', 'accelerationPSDY0')
   ORDER BY
       seq_num, field
   LIMIT 100;

Unpivoted Tables Corresponding Data Model
------------------------------------------

These transformations produce multiple values per exposure or visit. The results are stored in the ``exposure_efd_unpivoted`` and ``visit1_efd_unpivoted`` tables. Each row contains a ``property``, a ``field`` (the specific sensor), and a ``value``.

.. list-table:: Unpivoted Data Model
   :widths: 20 10 10 50 10
   :header-rows: 1

   * - Property Name
     - Data Type
     - IVOA Unit
     - Description
     - IVOA UCD
   * - ``mt_vibration_data_mean``
     - float
     - m**2.s**-4.Hz**-1
     - Mean acceleration PSD in the sensor direction. Fields: ``accelerationPSDX0-99``, ``accelerationPSDY0-99``, ``accelerationPSDZ0-99``
     - meta.ucd;stat.mean
   * - ``mt_vibration_data_stddev``
     - float
     - m**2.s**-4.Hz**-1
     - Standard deviation of the acceleration PSD in the sensor direction. Fields: ``accelerationPSDX0-99``, ``accelerationPSDY0-99``, ``accelerationPSDZ0-99``
     - stat.stdev
   * - ``mt_vibration_data_max``
     - float
     - m**2.s**-4.Hz**-1
     - Maximum acceleration PSD in the sensor direction. Fields: ``accelerationPSDX0-99``, ``accelerationPSDY0-99``, ``accelerationPSDZ0-99``
     - meta.ucd;stat.max
   * - ``mt_vibration_data_min``
     - float
     - m**2.s**-4.Hz**-1
     - Minimum acceleration PSD in the sensor direction. Fields: ``accelerationPSDX0-99``, ``accelerationPSDY0-99``, ``accelerationPSDZ0-99``
     - meta.ucd;stat.min
   * - ``mt_logevent_annular_zernike_coeff``
     - float
     - um
     - z4-z22 terms of annular Zernike polynomials. Fields: ``annularZernikeCoeff0-18``
     -
   * - ``mt_logevent_aggregated_dof``
     - float
     - um
     - Aggregated degree of freedom in the control algorithm. The unit of angle-related elements is arcsec instead of micron. Fields: ``aggregatedDoF0-49``
     -
   * - ``mt_logevent_visit_dof``
     - float
     - um
     - Calculated degree of freedom in the last visit. The unit of angle-related elements is arcsec instead of micron. Fields: ``visitDof0-49``
     -
   * - ``mt_logevent_m1m3_correction``
     - float
     - N
     - Actuator force in z direction. Fields: ``zForces0-155``
     -
   * - ``mt_logevent_m2_correction``
     - float
     - N
     - Actuator force in z direction. Fields: ``zForces0-71``
     -
   * - ``mt_m1m3_applied_forces_mean``
     - float
     - N
     - Mean forces in Z axis. Fields: ``zForces0-155``
     - meta.ucd;stat.mean
   * - ``mt_m1m3_applied_elevation_forces_mean``
     - float
     - N
     - Mean forces in Z axis. Fields: ``zForces0-155``
     - meta.ucd;stat.mean
   * - ``mt_m1m3_applied_thermal_forces_mean``
     - float
     - N
     - Mean forces in Z axis. Fields: ``zForces0-155``
     - meta.ucd;stat.mean
   * - ``mt_m1m3_applied_azimuth_forces_mean``
     - float
     - N
     - Mean forces in Z axis. Fields: ``zForces0-155``
     - meta.ucd;stat.mean
   * - ``mt_m2_axial_force_applied_mean``
     - float
     - N
     - Mean force applied by SAL command or script for each actuator in sequence. Fields: ``applied0-71``
     - meta.ucd;stat.mean
   * - ``mt_m2_axial_force_lut_gravity_mean``
     - float
     - N
     - Mean gravity component (F_e + F_0 + F_a + F_f) of look-up table (LUT) force for each actuator in sequence. Fields: ``lutGravity0-71``
     - meta.ucd;stat.mean
   * - ``mt_m2_axial_force_lut_temperature_mean``
     - float
     - N
     - Mean temperature component (T_u + T_x + T_y + T_r) of look-up table (LUT) force for each actuator in sequence. Fields: ``lutTemperature0-71``
     - meta.ucd;stat.mean
   * - ``mt_logevent_annular_zernike_indices``
     - float
     -
     - z4-z22 terms of Noll Zernike polynomial indices. Fields: ``nollZernikeIndices0-50`` and ``61-99``
     -

Common Query Scenarios
----------------------

This section provides complete end-to-end examples for typical analysis scenarios.

Scenario 1: Environmental Conditions Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal**: Analyze environmental conditions (temperature, seeing, wind) for a specific night to understand observing quality.

**Complete workflow:**

.. code-block:: sql

   -- Get environmental conditions for all exposures on a specific night
   SELECT
       day_obs,
       seq_num,
       exposure_id,
       mt_dome_temperature_mean,
       mt_dimm_fwhm_mean,
       mt_salindex110_wind_speed_0_mean,
       mt_salindex110_sonic_temperature_mean
   FROM efd_lsstcam.exposure_efd
   WHERE day_obs = 20250806
   ORDER BY seq_num;

   -- Find exposures with good seeing conditions
   SELECT
       day_obs,
       seq_num,
       exposure_id,
       mt_dimm_fwhm_mean,
       mt_dome_temperature_mean
   FROM efd_lsstcam.exposure_efd
   WHERE day_obs = 20250806
   AND mt_dimm_fwhm_mean < 0.8
   ORDER BY mt_dimm_fwhm_mean;

   -- Summary statistics for the night
   SELECT
       COUNT(*) as total_exposures,
       AVG(mt_dome_temperature_mean) as avg_temp,
       AVG(mt_dimm_fwhm_mean) as avg_seeing,
       MIN(mt_dimm_fwhm_mean) as best_seeing,
       MAX(mt_dimm_fwhm_mean) as worst_seeing
   FROM efd_lsstcam.exposure_efd
   WHERE day_obs = 20250806
   AND mt_dimm_fwhm_mean IS NOT NULL;

Scenario 2: Mount Performance Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal**: Analyze telescope mount performance by examining encoder jitter and pointing accuracy.

**Complete workflow:**

.. code-block:: sql

   -- Get mount encoder performance for a specific day
   SELECT
       day_obs,
       seq_num,
       exposure_id,
       mt_azimuth_encoder_absolute_position_0_rms_jitter,
       mt_elevation_encoder_absolute_position_0_rms_jitter,
       mt_pointing_mount_position_ra_mean,
       mt_pointing_mount_position_ra_stddev
   FROM efd_lsstcam.exposure_efd
   WHERE day_obs = 20250806
   AND mt_azimuth_encoder_absolute_position_0_rms_jitter IS NOT NULL
   ORDER BY seq_num;

   -- Find exposures with high jitter
   SELECT
       day_obs,
       seq_num,
       exposure_id,
       mt_azimuth_encoder_absolute_position_0_rms_jitter,
       mt_elevation_encoder_absolute_position_0_rms_jitter
   FROM efd_lsstcam.exposure_efd
   WHERE day_obs = 20250806
   AND (mt_azimuth_encoder_absolute_position_0_rms_jitter > 0.01
        OR mt_elevation_encoder_absolute_position_0_rms_jitter > 0.01)
   ORDER BY mt_azimuth_encoder_absolute_position_0_rms_jitter DESC;

Scenario 3: Vibration Sensor Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal**: Analyze vibration data from multiple sensors stored in unpivoted format.

**Complete workflow:**

.. code-block:: sql

   -- Get vibration data for a specific exposure
   SELECT
       day_obs,
       seq_num,
       exposure_id,
       property,
       field,
       value
   FROM efd_lsstcam.exposure_efd_unpivoted
   WHERE day_obs = 20250806
   AND seq_num = 55
   AND property = 'mt_vibration_data_mean'
   ORDER BY field;

   -- Pivot vibration data for easier analysis
   SELECT
       day_obs,
       seq_num,
       exposure_id,
       MAX(CASE WHEN field = 'accelerationPSDX0' THEN value END) AS psdx0,
       MAX(CASE WHEN field = 'accelerationPSDX1' THEN value END) AS psdx1,
       MAX(CASE WHEN field = 'accelerationPSDY0' THEN value END) AS psdy0,
       MAX(CASE WHEN field = 'accelerationPSDY1' THEN value END) AS psdy1
   FROM efd_lsstcam.exposure_efd_unpivoted
   WHERE day_obs = 20250806
   AND property = 'mt_vibration_data_mean'
   GROUP BY day_obs, seq_num, exposure_id
   ORDER BY seq_num;

   -- Combine vibration data with environmental conditions
   SELECT
       piv.day_obs,
       piv.seq_num,
       piv.mt_dome_temperature_mean,
       unpiv.field AS sensor_name,
       unpiv.value AS vibration_psd
   FROM efd_lsstcam.exposure_efd AS piv
   JOIN efd_lsstcam.exposure_efd_unpivoted AS unpiv
   ON piv.day_obs = unpiv.day_obs AND piv.seq_num = unpiv.seq_num
   WHERE piv.day_obs = 20250806
   AND unpiv.property = 'mt_vibration_data_mean'
   ORDER BY piv.seq_num, unpiv.field;

Scenario 4: Data Completeness Check
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal**: Verify data availability and completeness for a time period.

**Complete workflow:**

.. code-block:: sql

   -- Check data availability for a week
   SELECT
       day_obs,
       COUNT(*) as total_exposures,
       COUNT(mt_dome_temperature_mean) as dome_temp_measurements,
       COUNT(mt_dimm_fwhm_mean) as seeing_measurements,
       COUNT(mt_salindex110_wind_speed_0_mean) as wind_measurements
   FROM efd_lsstcam.exposure_efd
   WHERE day_obs BETWEEN 20250801 AND 20250807
   GROUP BY day_obs
   ORDER BY day_obs;

   -- Check for missing data patterns
   SELECT
       day_obs,
       COUNT(*) as total_exposures,
       COUNT(mt_dome_temperature_mean) as temp_data,
       ROUND(COUNT(mt_dome_temperature_mean)::numeric / COUNT(*) * 100, 2) as temp_coverage_pct
   FROM efd_lsstcam.exposure_efd
   WHERE day_obs BETWEEN 20250801 AND 20250807
   GROUP BY day_obs
   HAVING COUNT(mt_dome_temperature_mean) < COUNT(*) * 0.9
   ORDER BY day_obs;

   -- Check unpivoted data availability
   SELECT
       day_obs,
       COUNT(DISTINCT seq_num) as exposures_with_unpivoted_data,
       COUNT(DISTINCT property) as unique_properties,
       COUNT(*) as total_unpivoted_records
   FROM efd_lsstcam.exposure_efd_unpivoted
   WHERE day_obs = 20250806
   GROUP BY day_obs;

Troubleshooting Common Issues
-----------------------------

**No Data Returned for Expected Time Range**

If your query returns no results for a time period when you expect data:

1. **Check Data Availability**: Query using indexed columns to see if data exists for your time range
2. **Verify Schema Name**: Ensure you're using the correct schema name for your instrument
3. **Check for NULL Values**: Some columns may be NULL if telemetry wasn't available

**Missing Columns or Properties**

If you're looking for specific telemetry data that doesn't appear:

1. **Check Schema Files**: For pivoted tables, refer to the Science Data Models linked in the "Pivoted vs. Unpivoted Data Model" section above, which list all available columns for each instrument.
2. **Check Unpivoted Properties**: For unpivoted tables, refer to the "Unpivoted Tables Corresponding Data Model" section in this documentation, which lists all available properties.
3. **Check Unpivoted Tables**: Some data may be stored in unpivoted format:

.. code-block:: sql

   SELECT
        DISTINCT property
   FROM
        efd_lsstcam.exposure_efd_unpivoted
   WHERE
        day_obs = 20250806
   LIMIT 20;

**Performance Issues with Large Queries**

For queries over long time periods:

1. **Use Indexed Columns**: Always include ``day_obs`` and ``seq_num`` filters to use the primary key index
2. **For Unpivoted Tables**: Use ``day_obs``, ``seq_num``, ``property``, and ``field`` for optimal performance (``exposure_id`` is not indexed)
3. **Limit Result Sets**: Use ``LIMIT`` clauses for exploratory queries
4. **Avoid Non-Indexed Filters**: Filtering on ``exposure_id`` or other non-indexed columns can be slow for large datasets
5. **Use Composite Keys**: When joining tables, use ``day_obs`` and ``seq_num`` together instead of ``exposure_id``

**Understanding NULL Values**

NULL values in the data typically indicate:

- **No Telemetry Available**: The EFD topic wasn't available during the observation
- **Transformation Failed**: The transformation function couldn't process the data
- **Configuration Issue**: The telemetry topic isn't configured for the instrument

Use ``IS NOT NULL`` filters when you need complete data:

.. code-block:: sql

  SELECT
        day_obs,
        seq_num,
        exposure_id,
        mt_dome_temperature_mean
  FROM
        efd_lsstcam.exposure_efd
  WHERE
        day_obs = 20250806
        AND mt_dome_temperature_mean IS NOT NULL
  LIMIT 50;
