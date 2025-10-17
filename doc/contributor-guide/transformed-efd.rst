Transformed EFD
===============

The ``transformed-efd`` processing pipeline is configuration-driven. All transformations are defined in YAML files, separating the transformation logic (YAML) from the execution engine (Python). This allows contributors to add new data products by editing a configuration file.

This guide provides comprehensive instructions for contributors who need to add new columns, transformation functions, or telemetry topics to the transformed EFD system.

.. contents::
   :depth: 3
   :local:

Overview
--------

The transformed EFD system processes raw telemetry data from the Engineering and Facilities Database (EFD) **over specific exposure and visit timespans** into structured, queryable metrics. This is a key architectural constraint: the system only processes and transforms EFD data during:

- **Exposure timespans**: The time period when a camera exposure is being taken
- **Visit timespans**: The time period when a telescope visit (comprising multiple exposures) occurs

Contributors can extend this system by:

1. **Adding New Columns**: Define new metrics by configuring YAML files
2. **Creating Transformation Functions**: Add new mathematical operations for data processing
3. **Extending Telemetry Topics**: Include new data sources from the EFD

**Important**: All transformations are applied only to data within these defined timespans, not to continuous data streams.

Quick Reference for Experienced Contributors
---------------------------------------------

.. note::
   **For contributors familiar with the system**: Jump directly to the workflow below. See detailed explanations in subsequent sections.

**Adding a New Column (5-minute workflow):**

1. **Edit configuration file:**

.. code-block:: bash

   nano python/lsst/consdb/transformed_efd/config/config_latiss.yaml

2. **Add column definition:**

.. code-block:: yaml

   - name: new_metric_mean
     tables: ["exposure_efd", "visit1_efd"]
     function: mean
     datatype: float
     ivoa: {"unit": "deg_C", "ucd": "phys.temperature;stat.mean"}
     description: Mean value of new metric.
     packed_series: false
     topics:
       - name: lsst.sal.TOPIC.name
         fields:
           - name: fieldName

3. **Regenerate schema:**

.. code-block:: bash

   python ./python/lsst/consdb/transformed_efd/generate_schema_from_config.py --instrument latiss

4. **Create migration:**

.. code-block:: bash

   alembic -n efd_latiss revision --autogenerate -m "Add new metric"

5. **Test:**

.. code-block:: bash

   python -m pytest tests/

**Adding New Function (3-minute workflow):**

1. **Add method to Summary class:**

.. code-block:: python

   # In summary.py
   def new_function(self) -> float:
       """Description of new function."""
       values = self._get_numeric_values()
       if len(values) == 0:
           return np.nan
       return custom_calculation(values)

2. **Add tests:**

.. code-block:: python

   # In tests/transformed_efd/test_summary.py
   def test_new_function(summary_instance):
       assert summary_instance.new_function() == expected_value

3. **Use in configuration:**

.. code-block:: yaml

   function: new_function

The system supports multiple instruments:

- **LATISS**: Auxiliary Telescope Imaging Spectrograph and Slitless Spectrograph
- **LSSTComCam**: Commissioning Camera
- **LSSTCam**: Main LSST Camera

**Adding a New Instrument**: To add support for a new instrument, you need to create a new configuration file (``config_<instrument>.yaml``), generate the corresponding schema file, and set up Alembic migrations. The instrument must have defined exposure and visit timespans in the LSST Butler system, as the transformed EFD system depends on these temporal boundaries for data processing.

Configuration Data Model
------------------------

The YAML file structure is validated by Pydantic models in ``config_model.py``. The configuration follows Felis standards for astronomical data catalogs as defined in the `Felis documentation <https://felis.lsst.io/>`_. The top-level structure of a configuration file is:

.. code-block:: yaml

   version: "1.0.0"
   columns:
     - name: mt_salindex301_temperature_4_mean
       tables: ["exposure_efd","visit1_efd"]
       function: mean
       datatype: float
       ivoa: {"unit":"deg_C", "ucd":"meta.ucd;stat.mean"}
       description: Mean weather tower air temperature item 4.
       packed_series: False
       subset_field: salIndex
       subset_value: 301
       topics:
         - name: lsst.sal.ESS.temperature
           fields:
             - name: temperatureItem4
             - name: salIndex

- ``version``: A string to version the configuration file. This value is propagated into the schemas versioning.
- ``columns``: A list where each entry, a YAML object, defines a single column to be generated in the database.

Each item in the ``columns`` list is a dictionary defining a single transformation. The following sections detail all available configuration keys.

Core Attributes
~~~~~~~~~~~~~~~

**name** (string, required)
  The name of the column in the database (e.g., ``mt_dome_temperature_mean``). Must be a valid SQL column name.

**description** (string, required)
  A clear, concise description of the metric used for schema documentation. Should explain what the metric represents and its significance.

**datatype** (string, required)
  The target database data type. Must be a valid Felis type as defined in the `Felis Data Types documentation <https://felis.lsst.io/>`_:

  - ``float``: For decimal numbers (64-bit floating point)
  - ``int``: For whole numbers (32-bit signed integer)
  - ``long``: For large integers (64-bit signed integer)
  - ``boolean``: For true/false values
  - ``timestamp``: For date/time values
  - ``string``: For text data (with optional length specification)

  **Reference**: See the `Felis User Guide <https://felis.lsst.io/>`_ for complete data type specifications and additional types available for astronomical data catalogs.

**tables** (list, required)
  Specifies which tables this column should be written to. You must explicitly specify which tables to use. Valid options are:

  - ``exposure_efd``: Standard exposure-level metrics
  - ``visit1_efd``: Visit-level metrics
  - ``exposure_efd_unpivoted``: Key-value format for exposure data
  - ``visit1_efd_unpivoted``: Key-value format for visit data

  **Compatibility Rules**:

  - **Pivoted vs Unpivoted**: You cannot mix pivoted and unpivoted tables in the same column configuration
  - **When ``store_unpivoted: true``**: Only unpivoted tables (``exposure_efd_unpivoted``, ``visit1_efd_unpivoted``) are allowed
  - **When ``store_unpivoted: false`` or omitted**: Only regular tables (``exposure_efd``, ``visit1_efd``) are allowed
  - **Validation**: The system automatically validates table compatibility and will raise an error for incompatible combinations

IVOA Metadata
~~~~~~~~~~~~~

**ivoa** (dictionary, optional)
  Contains standardized International Virtual Observatory Alliance (IVOA) metadata fields for TAP queries and data discovery:

  - **ucd** (string): The IVOA Unified Content Descriptor (e.g., ``phys.temperature``, ``stat.mean``)
  - **unit** (string): The physical unit of the value (e.g., ``deg_C``, ``m/s``, ``Pa``)

  **Documentation References**:

  - `IVOA UCD List <https://www.ivoa.net/documents/UCD1+/20221024/PR-UCDlist-1.4-20221024.html>`_: Official UCD vocabulary and definitions
  - `IVOA Units <https://www.ivoa.net/documents/VOUnits/>`_: Standard unit specifications for astronomical data
  - `IVOA Standards <https://www.ivoa.net/documents/>`_: Complete IVOA documentation suite

  **Common UCD Patterns**:

  - ``phys.temperature``: Temperature measurements
  - ``phys.pressure``: Pressure measurements
  - ``stat.mean``: Mean values
  - ``stat.rms``: Root mean square values
  - ``stat.max``: Maximum values
  - ``stat.min``: Minimum values
  - ``meta.ucd;stat.mean``: Statistical means

  **Common Units**:

  - ``deg_C``: Degrees Celsius
  - ``deg``: Degrees (angular)
  - ``m/s``: Meters per second
  - ``Pa``: Pascals
  - ``V``: Volts
  - ``A``: Amperes
  - ``""``: Dimensionless (empty string)

Data Sources and Filters
~~~~~~~~~~~~~~~~~~~~~~~~

**topics** (list of dictionaries, required)
  Specifies the input data from the Engineering and Facilities Database (EFD). Each dictionary must contain:

  - **name** (string): The full name of the EFD topic (e.g., ``lsst.sal.ESS.temperature``)
  - **fields** (list of dictionaries): One or more fields to query from that topic. Each dictionary must contain a ``name`` key.

  **Topic Examples**:

  - ``lsst.sal.ESS.temperature``: Environmental sensor temperature
  - ``lsst.sal.MTMount.encoder``: Main telescope mount encoder
  - ``lsst.sal.Dome.position``: Dome position data

**subset_field** and **subset_value** (optional)
  These keys select a subset of time-series data from a topic before applying the transformation:

  - **subset_field**: The name of a field within the topic to use as a filter key
  - **subset_value**: The value (or list of values) to match in the ``subset_field``

  **Critical Requirement**: The ``subset_field`` **must be included** in the ``fields`` list of the topic. If the field is not present in the topic fields, the filtering will fail because there's no data column to filter on.

  **Use Cases**:

  - Filter by sensor index (e.g., ``salIndex: 301``)
  - Filter by component type (e.g., ``componentType: "temperature"``)
  - Filter by multiple values: ``subset_value: [301, 302, 303]``

Transformation Logic
~~~~~~~~~~~~~~~~~~~~

**function** (string, required)
  The name of a method from the ``Summary`` class (in ``summary.py``) to apply to the time-series data **within the exposure or visit timespan**.

  **Available Functions**:

  - ``mean``: Calculate the arithmetic mean of data points within the timespan
  - ``stddev``: Calculate the standard deviation of data points within the timespan (with configurable degrees of freedom)
  - ``max``: Find the maximum value within the timespan
  - ``min``: Find the minimum value within the timespan
  - ``rms_from_polynomial_fit``: Calculate RMS after polynomial fitting of data within the timespan
  - ``most_recent_value``: Return the most recent scalar value within the timespan

  **Timespan Context**: All functions operate on data that falls within the specific exposure or visit timespan boundaries. Data outside these timespans is ignored.

**function_args** (dictionary, optional)
  Parameters to pass to the selected function. Keys and values must match the method signature in the ``Summary`` class.

  **Common Parameters**:

  - For ``stddev``: ``{"ddof": 1}`` (degrees of freedom)
  - For ``rms_from_polynomial_fit``: ``{"degree": 4, "fit_basis": "index"}``
  - For ``most_recent_value``: ``{"start_offset": 0}`` (offset in hours)

**pre_aggregate_interval** (string, optional)
  For simple functions (``mean``, ``max``, ``min``), enables server-side aggregation in InfluxDB to improve performance. Use time strings like ``"1s"``, ``"5m"``, or ``"1h"``.

  **Critical Performance Guidelines**:

  - **Avoid if topic is used in multiple columns**: The system optimizes queries to fetch each topic only once per processing interval. Using ``pre_aggregate_interval`` on a topic that appears in multiple column definitions will cause the system to query that topic twice (once with aggregation, once without), which is counterproductive and degrades performance.
  - Only use with simple aggregation functions (``mean``, ``max``, ``min``)
  - Test performance impact before deployment
  - Consider the impact on InfluxDB load and query complexity

Advanced Data Structures
~~~~~~~~~~~~~~~~~~~~~~~~

**packed_series** (boolean, required)
  EFD convention for storing array-like data across multiple fields with numeric suffixes (e.g., ``waveform0``, ``waveform1``, ``waveform2``).

  - Set to ``true`` to reconstruct fields into a single time-ordered dataset
  - The system automatically sorts fields by numeric suffix
  - Useful for waveform data, sensor arrays, or multi-channel measurements
  - Note: Packed series topics include ``cRIO_timestamp``, but this field is not required for the packed series functionality

**store_unpivoted** (boolean, optional, default: false)
  When ``true``, stores the transformation in unpivoted tables using a key-value format:

  - The ``name`` of the column definition becomes the ``property``
  - Individual EFD field names become the ``field``
  - Calculated values are stored in the ``value`` column

  **Validation Rule**: A column with ``store_unpivoted: true`` **MUST ONLY** list unpivoted tables in its ``tables`` attribute. The system validates this automatically and will raise a ``ValueError`` if any regular tables are included when ``store_unpivoted: true``. You cannot mix pivoted and unpivoted tables in the same column configuration.


Architectural Constraints
-------------------------

**Timespan-Based Processing**
The transformed EFD system is fundamentally designed around exposure and visit timespans:

- **Exposure Timespan**: Each camera exposure has a defined start and end time. All EFD data within this window is processed and aggregated into a single metric value for that exposure.

- **Visit Timespan**: Each telescope visit (comprising multiple exposures) has a broader timespan. EFD data within this visit window is processed and aggregated into visit-level metrics.

- **No Continuous Processing**: The system does not process continuous data streams. It only operates on discrete time windows defined by exposures and visits.

- **Data Filtering**: Raw EFD data is automatically filtered to include only data points that fall within the relevant timespan boundaries before applying transformation functions.

This timespan-based architecture ensures that all metrics are contextually relevant to specific astronomical observations rather than arbitrary time periods.

Configuration Examples
-----------------------

This section provides practical examples of common configuration patterns, all operating within exposure and visit timespan boundaries.

Basic Temperature Metric (Pivoted)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   - name: mt_dome_temperature_mean
     tables: ["exposure_efd", "visit1_efd"]
     function: mean
     datatype: float
     ivoa: {"unit": "deg_C", "ucd": "phys.temperature;stat.mean"}
     description: Mean dome air temperature during exposure/visit timespan.
     packed_series: false
     topics:
       - name: lsst.sal.ESS.temperature
         fields:
           - name: domeAirTemperature

   **Note**: This metric uses regular (pivoted) tables. The ``store_unpivoted`` field is omitted (defaults to ``false``), so only regular tables are specified.

RMS Jitter Calculation
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   - name: mt_azimuth_encoder_jitter_rms
     tables: ["exposure_efd"]
     function: rms_from_polynomial_fit
     function_args: {"degree": 4, "fit_basis": "index"}
     datatype: float
     ivoa: {"unit": "", "ucd": "stat.rms"}
     description: RMS jitter after 4th order polynomial fit of azimuth encoder position.
     packed_series: false
     topics:
       - name: lsst.sal.MTMount.encoder
         fields:
           - name: azimuthEncoderAbsolutePosition0

Subset Filtering Example
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   - name: mt_salindex301_temperature_4_mean
     tables: ["exposure_efd", "visit1_efd"]
     function: mean
     datatype: float
     ivoa: {"unit": "deg_C", "ucd": "phys.temperature;stat.mean"}
     description: Mean weather tower air temperature item 4 from sensor index 301.
     packed_series: false
     subset_field: salIndex
     subset_value: 301
     topics:
       - name: lsst.sal.ESS.temperature
         fields:
           - name: temperatureItem4
           - name: salIndex

   **Note**: The ``subset_field`` (``salIndex``) is included in the topic fields list. This is required for the filtering to work correctly.

Packed Series Example
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   - name: mt_waveform_rms_jitter
     tables: ["exposure_efd"]
     function: rms_from_polynomial_fit
     function_args: {"degree": 2, "fit_basis": "index"}
     datatype: float
     ivoa: {"unit": "V", "ucd": "stat.rms"}
     description: RMS jitter of reconstructed waveform data after polynomial fit.
     packed_series: true
     topics:
       - name: lsst.sal.MTMount.waveform
         fields:
           - name: waveform

Unpivoted Storage Example
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   - name: mt_multi_sensor_temperature
     tables: ["exposure_efd_unpivoted", "visit1_efd_unpivoted"]
     function: mean
     datatype: float
     ivoa: {"unit": "deg_C", "ucd": "phys.temperature;stat.mean"}
     description: Mean temperature from multiple sensors stored in unpivoted format.
     packed_series: false
     store_unpivoted: true
     topics:
       - name: lsst.sal.ESS.temperature
         fields:
           - name: sensor1Temperature
           - name: sensor2Temperature
           - name: sensor3Temperature

   **Note**: This metric uses unpivoted tables only. When ``store_unpivoted: true``, only unpivoted tables are allowed in the ``tables`` list.

Pre-aggregation Performance Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**❌ WRONG: Using pre-aggregation on shared topic**

If you have multiple columns using the same topic:

.. code-block:: yaml

   # Column 1
   - name: temperature_mean
     topics:
       - name: lsst.sal.ESS.temperature
         fields:
           - name: domeAirTemperature
     function: mean
     pre_aggregate_interval: "1s"  # This causes duplicate queries!
     # ... other attributes

   # Column 2
   - name: temperature_max
     topics:
       - name: lsst.sal.ESS.temperature  # Same topic!
         fields:
           - name: domeAirTemperature
     function: max
     # ... other attributes

**✅ CORRECT: No pre-aggregation on shared topic**

.. code-block:: yaml

   # Column 1
   - name: temperature_mean
     topics:
       - name: lsst.sal.ESS.temperature
         fields:
           - name: domeAirTemperature
     function: mean
     # No pre_aggregate_interval - topic is shared!

   # Column 2
   - name: temperature_max
     topics:
       - name: lsst.sal.ESS.temperature
         fields:
           - name: domeAirTemperature
     function: max
     # ... other attributes

Invalid Table Configuration Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**❌ WRONG: Mixing pivoted and unpivoted tables**

.. code-block:: yaml

   - name: invalid_mixed_tables
     tables: ["exposure_efd", "exposure_efd_unpivoted"]  # This will fail!
     store_unpivoted: true
     function: mean
     datatype: float
     description: This configuration is invalid
     packed_series: false
     topics:
       - name: lsst.sal.ESS.temperature
         fields:
           - name: temperature

**❌ WRONG: Regular tables with unpivoted flag**

.. code-block:: yaml

   - name: invalid_unpivoted_with_regular_tables
     tables: ["exposure_efd", "visit1_efd"]  # This will fail!
     store_unpivoted: true
     function: mean
     datatype: float
     description: This configuration is invalid
     packed_series: false
     topics:
       - name: lsst.sal.ESS.temperature
         fields:
           - name: temperature

**✅ CORRECT: Explicit table specification**

.. code-block:: yaml

   - name: valid_explicit_tables
     tables: ["exposure_efd", "visit1_efd"]  # Explicitly specified
     function: mean
     datatype: float
     description: This configuration is valid
     packed_series: false
     topics:
       - name: lsst.sal.ESS.temperature
         fields:
           - name: temperature

Contributor Workflow
--------------------

This section describes the complete workflow for contributing new columns or modifying existing ones.

Adding New Columns
~~~~~~~~~~~~~~~~~~

Follow these steps to add or modify a transformed metric:

1. **Identify the Data Source**

   - Determine which EFD topic contains your data
   - Identify the specific fields you need
   - Understand the data structure (packed series, subset filtering, etc.)
   - **Important**: Ensure your data is relevant to exposure or visit timespans, as the system only processes data within these specific time windows

2. **Edit the YAML Configuration**
   Add or modify a ``Column`` definition in the appropriate instrument configuration file:

   - **LATISS**: ``python/lsst/consdb/transformed_efd/config/config_latiss.yaml``
   - **LSSTComCam**: ``python/lsst/consdb/transformed_efd/config/config_lsstcomcam.yaml``
   - **LSSTCam**: ``python/lsst/consdb/transformed_efd/config/config_lsstcam.yaml``

3. **Regenerate the Schema**
   Update the database schema definition. This step automatically validates your configuration using Pydantic models:

   .. code-block:: bash

      # From the root of the consdb repository
      python ./python/lsst/consdb/transformed_efd/generate_schema_from_config.py --instrument <your_instrument>

   Replace ``<your_instrument>`` with ``latiss``, ``lsstcomcam``, or ``lsstcam``.

   **Note**: The schema generation process automatically validates your configuration against the Pydantic models, so any configuration errors will be caught at this step.

4. **Generate Alembic Migrations**
   Create database migration scripts:

   .. code-block:: bash

      # For LSSTCam
      alembic -n efd_lsstcam revision --autogenerate -m "Add mean dome temperature"

      # For LSSTComCam
      alembic -n efd_lsstcomcam revision --autogenerate -m "Add mean wind speed"

      # For LATISS
      alembic -n efd_latiss revision --autogenerate -m "Remove old focus_z column"


   .. important::

       Migrations are built from SDM schemas and may require manual editing. For example, renaming an existing column will be interpreted as dropping the old column and creating a new one.


5. **Review Generated Files**
   Check the following files were created/updated:

   - Modified ``config_<instrument>.yaml`` file
   - Updated schema YAML file (``schemas/yml/efd_<instrument>.yaml``)
   - New Alembic migration script (``alembic/versions/``)

6. **Test Your Changes**

   .. code-block:: bash

      # Run unit tests
      python -m pytest tests/

7. **Submit Pull Request**
   Your commit should include:

   - Modified configuration file
   - Updated schema YAML file
   - New Alembic migration script
   - Any associated test files

   Submit to the ``lsst-dm/consdb`` repository for review.

8. **Schema Propagation**
   Once approved and merged, an automated workflow propagates schema changes to the ``lsst/sdm_schemas`` repository. Follow the checklist in the generated SDM schemas pull request.

Adding New Transformation Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If existing functions don't meet your needs, you can add new transformation methods to the ``Summary`` class.

1. **Understand the Summary Class**

   The ``Summary`` class in ``summary.py`` processes time-series data and provides statistical methods. It handles:

   - Data validation and preprocessing
   - NaN value handling
   - Method application with error handling

2. **Define the Method**

   Add a new public method to the ``Summary`` class:

   .. code-block:: python

      # In summary.py
      import numpy as np

      class Summary:
          # ... existing methods ...

          def median(self) -> float:
              """Calculate the median, ignoring NaN values.

              Returns
              -------
              float
                  The median value, or NaN if no valid data points exist.
              """
              values = self._get_numeric_values()
              if len(values) == 0:
                  return np.nan
              return np.nanmedian(values)

          def percentile(self, q: float = 50.0) -> float:
              """Calculate a percentile, ignoring NaN values.

              Parameters
              ----------
              q : float, optional
                  Percentile to calculate (0-100), by default 50.0

              Returns
              -------
              float
                  The percentile value, or NaN if no valid data points exist.
              """
              values = self._get_numeric_values()
              if len(values) == 0:
                  return np.nan
              return np.nanpercentile(values, q)

3. **Add Comprehensive Tests**

   Add tests to the existing ``tests/transformed_efd/test_summary.py`` file:

   .. code-block:: python

      # Add to existing tests/transformed_efd/test_summary.py
      def test_median(summary_instance):
          """Test median calculation with valid data."""
          assert summary_instance.median() == 3.0

      def test_median_with_nan_values():
          """Test median calculation with NaN values."""
          # Create DataFrame with NaN values
          times = ["2023-01-01 00:00:00", "2023-01-01 00:00:30", "2023-01-01 00:01:00",
                   "2023-01-01 00:01:30", "2023-01-01 00:02:00"]
          idx = pd.to_datetime(times).tz_localize("UTC")
          df = pd.DataFrame({"value": [1.0, np.nan, 3.0, np.nan, 5.0]}, index=idx)

          start = Time("2023-01-01T00:00:00.000", scale="utc")
          end = Time("2023-01-01T00:02:00.000", scale="utc")
          summary = Summary(dataframe=df, exposure_start=start, exposure_end=end)

          assert summary.median() == 3.0

4. **Update Documentation**

   Add your new function to the available functions list in this guide and include usage examples.

5. **Use in Configuration**

   The new method is immediately available in YAML configurations:

   .. code-block:: yaml

      - name: "dome_air_temp_median"
        description: "Median dome air temperature during exposure."
        function: "median"
        datatype: float
        ivoa: {"unit": "deg_C", "ucd": "phys.temperature;stat.median"}
        tables: ["exposure_efd"]
        packed_series: false
        topics:
          - name: lsst.sal.ESS.temperature
            fields:
              - name: domeAirTemperature

Best Practices
--------------

Configuration Guidelines
~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Column Naming**

   - Use descriptive, consistent names
   - Avoid abbreviations that aren't widely understood
   - Follow existing patterns in the configuration files

2. **Description Quality**

   - Write clear, concise descriptions
   - Explain what the metric represents
   - Include units and context
   - Mention any special processing (e.g., "after polynomial detrending")

3. **IVOA Metadata**

   - Always include appropriate UCD and unit information
   - Use standard UCD patterns for consistency (refer to `IVOA UCD List <https://www.ivoa.net/documents/UCD1+/20221024/PR-UCDlist-1.4-20221024.html>`_)
   - Choose units that match the original data or scientific convention (refer to `IVOA Units <https://www.ivoa.net/documents/VOUnits/>`_)
   - Follow Felis standards for metadata as described in the `Felis documentation <https://felis.lsst.io/>`_
   - Consult the complete `IVOA Standards <https://www.ivoa.net/documents/>`_ for comprehensive metadata guidelines

4. **Performance Considerations**

   - Use ``pre_aggregate_interval`` judiciously - avoid if the topic is used in multiple columns
   - **Critical**: Never use ``pre_aggregate_interval`` on topics that appear in multiple column definitions as this causes duplicate queries
   - Avoid redundant transformations on the same topic
   - Consider the impact on InfluxDB load and query complexity
   - Test performance with realistic data volumes

5. **Data Validation**

   - Validate your YAML syntax before committing
   - Test with sample data when possible
   - Ensure subset filtering works correctly
   - Verify packed series reconstruction
   - Confirm your data is relevant within exposure/visit timespan contexts

Testing Strategies
~~~~~~~~~~~~~~~~~~

1. **Unit Testing**

   - Test new transformation functions thoroughly
   - Include edge cases (empty data, NaN values, single points)
   - Test with realistic time ranges and data patterns

2. **Integration Testing**

   - Test complete configuration files
   - Verify schema generation works correctly
   - Test with actual EFD data when available

3. **Validation Testing**

   - Use the Pydantic model validation
   - Test YAML syntax parsing
   - Verify database schema compatibility

Common Pitfalls
~~~~~~~~~~~~~~~

1. **YAML Syntax Errors**

   - Incorrect indentation (use spaces, not tabs)
   - Missing required fields
   - Invalid data types in configuration

2. **Topic/Field Mismatches**

   - Incorrect EFD topic names
   - Missing required fields for specific configurations
   - Invalid subset field names
   - Using subset_field without including it in the topic fields list

3. **Schema Generation Issues**

   - Column name conflicts
   - Invalid datatype specifications
   - Missing table specifications for unpivoted columns

4. **Migration Problems**

   - Alembic interpreting column renames as drops/creates
   - Missing manual migration edits
   - Incompatible schema changes

5. **Table Configuration Errors**

   - Mixing pivoted and unpivoted tables in the same column (not allowed)
   - Specifying regular tables when ``store_unpivoted: true``
   - Missing required tables for unpivoted columns

Troubleshooting
~~~~~~~~~~~~~~~

1. **Configuration Validation Errors**

   The schema generation process automatically validates your configuration. If you encounter validation errors, check:

   - YAML syntax errors (indentation, missing fields, etc.)
   - Invalid data types in configuration
   - Missing required fields
   - Table compatibility issues (mixing pivoted/unpivoted tables)

2. **Schema Generation Issues**

   .. code-block:: bash

      # Verbose schema generation
      python ./python/lsst/consdb/transformed_efd/generate_schema_from_config.py --instrument lsstcam --verbose

3. **Migration Problems**

   .. code-block:: bash

      # Check migration status
      alembic -n efd_lsstcam current

      # Validate migration script
      alembic -n efd_lsstcam check

4. **Data Processing Issues**

   - Check EFD topic availability and field names
   - Verify time range specifications
   - Test with smaller data samples first
