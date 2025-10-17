Transformed EFD
===============

This guide provides detailed technical information about the transformed EFD service architecture, class relationships, and code organization for developers who need to understand, modify, or extend the codebase.


Quick Reference for Experienced Developers
------------------------------------------

.. note::
   **For developers familiar with the system**: Jump directly to the sections below. See detailed explanations in subsequent sections.

**Core Classes:**

- ``Transform``: Main processing engine (transform.py)
- ``Summary``: Statistical processing (summary.py)
- ``ConfigModel``: Configuration validation (config_model.py)
- ``QueueManager``: Task scheduling (queue_manager.py)

**Key Extension Points:**

- Add transformation functions: ``Summary`` class methods
- Add data sources: Create new DAO classes inheriting from ``DBBase``
- Add output formats: Extend ``_process_column()`` method
- Add processing logic: Override ``_compute_column_value()``

**Common Development Tasks:**

- Add new statistical function: Add method to ``Summary`` class
- Add new instrument: Create config file + schema generation
- Modify data processing: Edit ``Transform.process_interval()``
- Add new database table: Create DAO class + update schemas

**Testing Commands:**

.. code-block:: bash

   python -m pytest tests/
   python -m pytest tests/transformed_efd/test_summary.py -v

Architecture Overview
---------------------

The transformed EFD service is a configuration-driven data processing pipeline that transforms raw Engineering and Facilities Database (EFD) telemetry into structured queryable metrics organized by exposure and visit timespans.

The core architectural principle is that everything stems from configuration files. This design permeates every aspect of the system:

- Data Sources: EFD topics and fields are defined in YAML
- Transformations: Statistical functions and their parameters are specified in config
- Output Schema: Database tables and column structures are generated from config
- Processing Logic: Exposure/visit boundary processing is configured, not hardcoded
- Instrument Support: New instruments require only configuration changes

Key Architectural Principles:

1. **Configuration-Driven**: All transformations, schemas, and processing logic defined in YAML files
2. **Separation of Concerns**: Business logic (YAML) separated from execution engine (Python)
3. **Timespan-Based Processing**: Data processed only within exposure/visit boundaries
4. **Extensible Design**: New instruments, metrics, and functions added through configuration
5. **Schema Generation**: Database schemas automatically generated from configuration definitions

High-Level Architecture Flow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following diagram shows the overall data flow and component relationships:

.. mermaid::

   flowchart TD
      A[YAML Config Files] --> B[ConfigModel Validation]
      B --> C[Schema Generation]
      C --> D[Database Tables]

      E[EFD InfluxDB] --> F[InfluxDbDao]
      G[LSST Butler] --> H[ButlerDao]

      F --> I[Transform Engine]
      H --> I
      B --> I

      I --> J[Summary Statistics]
      J --> K[Result Storage]
      K --> L[Exposure/Vist EFD Tables]

      M[Task Queue] --> N[QueueManager]
      N --> I

      O[CLI Interface] --> P[TransformEfd Main]
      P --> N
      P --> I

      style A fill:#e1f5fe
      style I fill:#f3e5f5
      style L fill:#e8f5e8

Core Components
---------------

Configuration Layer (config_model.py)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pydantic models that define and validate YAML configuration files:

**Field Model**

- Defines individual EFD field specifications with data types, units, and validation rules
- Handles field mapping between EFD topic names and output column names
- Supports field transformations and unit conversions
- Validates data types (float, int, string, boolean) with proper error handling

**Topic Model**

- Groups related EFD fields under a single topic specification
- Defines query parameters (time ranges, aggregation settings, packed series handling)
- Maps EFD topic names to database table structures
- Handles topic-level configuration like server-side aggregation preferences

**Column Model**

- Complete transformation definition including name, function, target tables, and aggregation settings
- Links statistical functions to specific EFD data sources
- Defines output schema structure and data types
- Handles column-level configuration like null value handling and precision settings

**ConfigModel**

- Top-level configuration container that orchestrates all processing
- Validates entire configuration against schema requirements
- Manages configuration versioning and compatibility
- Provides configuration introspection and debugging capabilities

Configuration Flow: YAML files → Pydantic validation → Database schema generation → Runtime processing

This layer handles:

- Configuration validation before processing begins
- Database schema generation from config definitions
- Type safety throughout the transformation pipeline
- Runtime configuration changes without code modifications

Data Access Layer (dao/)
~~~~~~~~~~~~~~~~~~~~~~~~

Database access objects for different data sources:

**DBBase (base.py)**

- Abstract base class providing common database operations and connection management
- Implements SQLAlchemy engine creation with NullPool for connection management
- Provides transaction management with automatic commit handling
- Handles database-specific SQL dialect differences (SQLite and PostgreSQL)
- Includes upsert and bulk insert operations with chunked processing
- Provides query execution methods (fetch_all_dict, fetch_one_dict, fetch_scalar)

**InfluxDbDao (influxdb.py)**

- EFD data querying with optimized batching and time-series specific operations
- Implements efficient query construction for time-range based data retrieval with server-side aggregation
- Handles packed series reconstruction using _merge_packed_time_series method
- Manages InfluxDB connection parameters via environment variables (EFD_HOST, EFD_USERNAME, etc.)
- Supports field batching to avoid query complexity limits (max_fields_per_query=100)
- Provides both regular time series queries and packed time series queries

**ButlerDao (butler.py)**

- Exposure/visit metadata retrieval from LSST Butler system
- Queries exposure and visit information within specified time ranges using timespan overlaps
- Handles Butler repository configuration through Butler object initialization
- Provides metadata filtering by instrument and time period
- Converts Butler resultsets to pandas DataFrames and dictionaries
- Handles EmptyQueryResultError gracefully by returning empty lists

**ExposureEfdDao, VisitEfdDao**

- Output database operations for storing transformed EFD data in PostgreSQL
- Implements upsert operations using execute_upsert method from DBBase
- Manages both regular and unpivoted table variants (exposure_efd, exposure_efd_unpivoted)
- Handles primary key validation and missing column detection
- Provides row counting and retrieval by ID operations
- Uses chunked processing for large dataset inserts (commit_every=100)

**TransformdDao (transformd.py)**

- Task scheduling metadata management for the transformed\_efd\_scheduler table
- Manages processing queue state with status tracking (pending, running, completed, failed)
- Handles task lifecycle methods: task\_started, task\_completed, task\_failed, task\_retries\_increment
- Provides task selection methods: select\_next, select\_last, select\_recent, select\_queued
- Implements orphaned task detection and cleanup via fail\_orphaned\_tasks
- Manages execution time tracking and retry counting for failed tasks

Scheduler Tables and Task Management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The transformed EFD system uses a dedicated ``efd_scheduler`` schema to manage processing tasks across all instruments. This schema contains separate tables for each instrument, tracking task lifecycle, execution status, and providing coordination for distributed processing.

**Scheduler Schema Structure**

The ``efd_scheduler`` schema contains individual tables for each instrument:

- **efd_scheduler.latiss**: LATISS instrument task management
- **efd_scheduler.lsstcam**: LSSTCam instrument task management
- **efd_scheduler.lsstcomcam**: LSSTComCam instrument task management

Each instrument table has the following columns:

- **id**: Auto-incrementing primary key for unique task identification
- **start_time**: Start time of the transformation interval (required)
- **end_time**: End time of the transformation interval (required)
- **timewindow**: Time window expansion in minutes for query boundaries
- **status**: Task processing status (pending, idle, running, completed, failed)
- **process_start_time**: Timestamp when task processing began
- **process_end_time**: Timestamp when task processing completed
- **process_exec_time**: Total execution time in seconds
- **exposures**: Number of exposures processed in this task
- **visits1**: Number of visits processed in this task
- **retries**: Number of retry attempts for failed tasks
- **error**: Error message if task failed
- **butler_repo**: Butler repository path used for this task
- **created_at**: Timestamp when task record was created

**Task Lifecycle and Status Management**

Tasks progress through the following lifecycle with different initial statuses based on execution mode:

1. **Task Creation**:
   - **Jobs**: Tasks created with status "idle" (waiting for processing)
   - **CronJobs**: Tasks created with status "pending" (waiting for processing)
2. **Task Selection**: Available tasks are selected using ``select_next()`` or similar methods
3. **Task Execution**: Status updated to "running" via ``task_started()``
4. **Task Completion**: Status updated to "completed" via ``task_completed()`` with execution metrics
5. **Task Failure**: Status updated to "failed" via ``task_failed()`` with error details
6. **Task Retry**: Failed tasks can be retried with exponential backoff via ``task_retries_increment()``

**Task Status Meanings**:

- **pending**: Default status for CronJob tasks, ready for processing
- **idle**: Status for Job tasks, ready for processing
- **running**: Task currently being processed
- **completed**: Task finished successfully
- **failed**: Task failed with error (eligible for retry)
- **stale**: Task marked as stale after 72 hours (no longer eligible for retry)

**Task Creation Process**

The ``QueueManager.create_tasks()`` method:

- Divides time ranges into processing intervals (default: 5-minute chunks)
- Checks for existing tasks to avoid duplicates
- Creates tasks with appropriate time boundaries and Butler repository references
- Uses bulk insert operations for efficient database operations
- Handles both one-time job creation and continuous cronjob task generation

**Task Selection and Processing**

The system provides multiple task selection strategies:

- **select_next()**: Gets the next available task for processing
- **select_last()**: Retrieves the most recently created task
- **select_recent()**: Gets tasks within a recent time window
- **select_queued()**: Finds tasks with specific status (pending, idle, etc.)
- **waiting_tasks()**: Gets tasks ready for processing
- **failed_tasks()**: Retrieves failed tasks eligible for retry

**Orphaned Task Management**

The system includes orphaned task detection and cleanup:

- **fail_orphaned_tasks()**: Identifies and marks abandoned tasks as failed
- **Orphaned Task Criteria**: Tasks in "running" status for extended periods
- **Automatic Cleanup**: Prevents resource leaks and enables task recovery
- **Retry Logic**: Failed tasks can be retried with exponential backoff (2.8^retries hours)
- **Stale Task Management**: Tasks older than 72 hours are marked as "stale" and no longer eligible for retry

**Task Coordination Features**

- **Duplicate Prevention**: Checks for existing tasks before creation
- **Time Window Management**: Handles overlapping time windows and gaps
- **Butler Repository Tracking**: Links tasks to specific Butler repository versions
- **Execution Metrics**: Tracks processing counts, execution times, and success rates
- **Error Handling**: Comprehensive error logging and retry mechanisms

Transformation Engine
~~~~~~~~~~~~~~~~~~~~~~

The transformation engine is the core of the system, orchestrating the entire data processing pipeline from EFD telemetry to structured database records.

**Main Transformation Process Flow**

The transformation process follows this sequence:

1. **Time Interval Processing** (process\_interval)
    - Retrieves exposures and visits from Butler within the time window
    - Calculates topic query intervals based on exposure/visit timespans
    - Processes each topic and column according to configuration

2. **Topic Optimization** (\_map\_topics)
    - Groups columns by topic, packed\_series, start\_offset, and aggregation settings
    - Minimizes duplicate EFD queries by batching similar requests
    - Enables server-side aggregation when configured (pre\_aggregate\_interval)

3. **EFD Data Retrieval** (\_query\_efd\_values)
    - Queries InfluxDB for telemetry data within calculated time windows
    - Handles both regular time series and packed time series data
    - Applies start\_offset adjustments for time window modifications

4. **Column Value Computation** (\_compute\_column\_value)
    - Filters EFD data to exact exposure/visit time boundaries
    - Applies statistical transformations via Summary class
    - Handles time offset adjustments and data validation

5. **Result Storage** (\_store\_results)
    - Stores computed metrics in PostgreSQL tables (exposure\_efd, visit1\_efd)
    - Supports both pivoted and unpivoted table formats
    - Uses chunked processing for large datasets

**Transform (transform.py)**

Key methods and their responsibilities:

- **process\_interval()**: Main entry point that orchestrates the entire transformation pipeline
- **\_map\_topics()**: Critical optimization that groups similar queries to minimize EFD roundtrips
- **\_compute\_column\_value()**: Core computation engine that applies transformations within timespans
- **\_process\_topic()**: Handles individual topic processing and data retrieval
- **\_process\_column()**: Manages column-level processing and result aggregation
- **get\_schema\_by\_instrument()**: Maps instrument names to database schemas

**Summary (summary.py)**

Statistical processing framework with the following transformation functions:

- **mean()**: Arithmetic mean ignoring NaN values
- **stddev()**: Standard deviation with configurable degrees of freedom (ddof parameter)
- **max()/min()**: Maximum/minimum values ignoring NaN
- **rms\_from\_polynomial\_fit()**: RMS after polynomial detrending (degree and fit\_basis parameters)
- **most\_recent\_value()**: Most recent scalar value with optional start\_offset
- **apply()**: Generic method dispatcher with comprehensive error handling

**Developer Extension Points**

When adding new functionality that may not fit the current workflow:

1. **New Transformation Functions**
    - Add method to Summary class in summary.py
    - Ensure proper NaN handling and error management
    - Add comprehensive tests for edge cases

2. **New Data Sources**
    - Create new DAO class inheriting from DBBase
    - Add data retrieval methods to Transform class
    - Update \_map\_topics() if new grouping logic is needed

3. **New Output Formats**
    - Extend \_process\_column() method to handle new table types
    - Add new storage methods similar to \_process\_exposures()
    - Update schema generation if new table structures are needed

4. **Custom Processing Logic**
    - Override \_compute\_column\_value() for specialized computation
    - Modify \_map\_topics() for custom query optimization
    - Extend \_process\_interval() for additional processing steps

5. **Performance Optimizations**
    - Adjust commit\_every parameter for batch processing
    - Modify \_map\_topics() grouping logic for better query batching
    - Implement custom caching in Summary class if needed

**Critical Integration Points**

- **Configuration Validation**: All new features must work with existing Pydantic models
- **Error Handling**: Use @handle\_processing\_errors decorator for consistent error management
- **Logging**: Maintain detailed logging for debugging and monitoring
- **Timespan Processing**: All transformations must respect exposure/visit boundaries
- **Database Compatibility**: Ensure new features work with existing schema generation

Application Entry Point
~~~~~~~~~~~~~~~~~~~~~~~~

**Transform EFD (transform\_efd.py)**

The main application entry point that orchestrates the entire transformed EFD workflow. This module handles CLI argument parsing, component initialization, task coordination, and graceful shutdown management.

**Core Workflow Functions**

- **main()**: Primary application entry point that initializes all components and coordinates execution
- **build\_argparser()**: Constructs comprehensive CLI interface with required and optional arguments
- **get\_logger()**: Configures structured logging with console and file output, UTC timestamps
- **read\_config()**: Loads and validates YAML configuration files using Pydantic models

**Task Processing Functions**

- **\_process\_task()**: Processes individual tasks with error handling, status updates, and retry logic
- **process\_tasks()**: Executes task batches with graceful shutdown support and progress tracking
- **handle\_job()**: Manages one-time job execution with custom time windows and resume capabilities
- **handle\_cronjob()**: Handles periodic cronjob execution with automatic task creation and retry management

**Utility Functions**

- **parse\_utc\_naive()**: Converts ISO datetime strings to UTC-naive datetime objects
- **\_to\_astropy\_time()**: Converts datetime objects to Astropy Time objects in UTC scale
- **\_get\_retryable\_tasks()**: Implements exponential backoff logic for failed task retries

**Component Initialization Sequence**

1. **CLI Parsing**: Validates command-line arguments and configuration requirements
2. **Logging Setup**: Configures structured logging with environment variable control
3. **Butler Initialization**: Creates Butler instance for metadata access
4. **EFD Connection**: Establishes InfluxDB connection with optimized query parameters
5. **Transform Setup**: Initializes main transformation processor with all dependencies
6. **Queue Manager**: Creates task scheduling and coordination system
7. **Orphaned Task Cleanup**: Handles recovery from previous interrupted executions

**Execution Modes**

**Job Mode**: One-time processing of specific time ranges

- Requires start\_time and end\_time parameters
- Supports resume functionality for interrupted jobs
- Creates tasks for the specified time window

**Cronjob Mode**: Continuous periodic processing

- Automatically creates tasks based on current time
- Handles failed task retries with exponential backoff
- Manages orphaned task detection and cleanup

**Error Handling and Recovery**

- **Signal Handling**: Graceful shutdown on SIGTERM/SIGINT with current task completion
- **Task State Management**: Tracks task lifecycle (pending → running → completed/failed)
- **Retry Logic**: Exponential backoff for failed tasks with configurable parameters
- **Orphaned Task Recovery**: Automatic detection and cleanup of abandoned tasks
- **Batch Processing**: Configurable batch sizes with shutdown checks between batches

Management Utilities
~~~~~~~~~~~~~~~~~~~~

**QueueManager (queue\_manager.py)**

- Task scheduling and workflow management for distributed processing
- Manages processing queues, task priorities, and resource allocation
- Handles task dependencies and parallel execution coordination
- Provides monitoring, logging, and debugging capabilities for workflow execution
- Implements fault tolerance and task retry mechanisms

**generate\_schema\_from\_config.py**

- Automated schema generation from YAML configuration files
- Creates PostgreSQL table definitions based on Column specifications
- Handles schema versioning and migration management
- Validates generated schemas against database constraints and best practices
- Provides schema comparison and diff capabilities for configuration changes

Class Relationships
-------------------

The transformed EFD system architecture consists of several interconnected layers that work together to process telemetry data from raw EFD streams into structured database records.

**System Architecture Overview**

The system follows a layered architecture with clear separation of concerns:

1. **Application Layer**: Main entry point that orchestrates the entire workflow (transform\_efd.py)
2. **Configuration Layer**: Pydantic models that define and validate YAML configurations
3. **Data Access Layer**: DAOs that abstract database operations and external service interactions
4. **Transformation Layer**: Core processing engine that orchestrates data flow and transformations
5. **Management Layer**: Task scheduling and workflow coordination
6. **Integration Layer**: CLI interfaces and external service connections

**Detailed Class Relationships**

.. mermaid::

   classDiagram
      class Transform {
          -butler_dao: ButlerDao
          -efd: InfluxDbDao
          -config: Dict
          -commit_every: int
          +process_interval()
          +_compute_column_value()
          +_map_topics()
          +_store_results()
      }

      class Summary {
          -_raw_dataframe: DataFrame
          -_data_array: ndarray
          +mean()
          +stddev()
          +max()
          +min()
          +apply()
      }

      class ConfigModel {
          +version: str
          +columns: List[Column]
      }

      class Column {
          +name: str
          +function: str
          +tables: List[str]
          +topics: List[Topic]
          +function_args: Dict
      }

      class Topic {
          +name: str
          +fields: List[Field]
      }

      class Field {
          +name: str
      }

      class InfluxDbDao {
          -url: str
          -database_name: str
          +select_time_series()
          +select_packed_time_series()
      }

      class ButlerDao {
          -butler: Butler
          +exposures_by_period()
          +visits_by_period()
      }

      class DBBase {
          -engine: Engine
          -db_uri: str
          +get_db_engine()
          +execute_upsert()
          +fetch_all_dict()
      }

      class ExposureEfdDao {
          -tbl: Table
          +upsert()
          +get_by_exposure_id()
          +count()
      }

      class VisitEfdDao {
          -tbl: Table
          +upsert()
          +get_by_visit_id()
          +count()
      }

      class TransformdDao {
          -tbl: Table
          +task_started()
          +task_completed()
          +task_failed()
          +select_next()
          +bulk_insert()
          +select_by_id()
          +count()
          +fail_orphaned_tasks()
      }

      class QueueManager {
          -dao: TransformdDao
          -instrument: str
          +create_tasks()
          +get_next_task()
          +mark_task_completed()
      }

      class TransformEfd {
          +main()
          +build_argparser()
          +get_logger()
          +read_config()
          +_process_task()
          +process_tasks()
          +handle_job()
          +handle_cronjob()
      }

      %% Core transformation relationships
      Transform --> ButlerDao : "creates and uses"
      Transform --> InfluxDbDao : "queries EFD data"
      Transform --> Summary : "instantiates for computations"
      Transform --> ConfigModel : "validates configuration"

      %% Configuration model relationships
      ConfigModel --> Column : "contains list of"
      Column --> Topic : "references list of"
      Topic --> Field : "contains list of"

      %% Data access inheritance
      ExposureEfdDao --> DBBase : "inherits from"
      VisitEfdDao --> DBBase : "inherits from"
      TransformdDao --> DBBase : "inherits from"

      %% Application orchestration relationships
      TransformEfd --> Transform : "initializes and coordinates"
      TransformEfd --> QueueManager : "initializes and manages"
      TransformEfd --> Butler : "creates Butler instance"
      TransformEfd --> InfluxDbDao : "creates EFD connection"
      TransformEfd --> ConfigModel : "validates configuration"

      %% Queue management relationships
      QueueManager --> TransformdDao : "manages via"
      QueueManager --> Transform : "coordinates execution"

      %% Database operations
      Transform --> ExposureEfdDao : "stores results via"
      Transform --> VisitEfdDao : "stores results via"

The system consists of the following key classes and their relationships:

**Core Classes**

- **Transform**: Main processing engine with dependencies on ButlerDao, InfluxDbDao, Summary, and ConfigModel
- **Summary**: Statistical processing framework with methods for mean, stddev, max, min, rms\_from\_polynomial\_fit, most\_recent\_value, apply
- **ConfigModel**: Pydantic model containing version and list of Column objects
- **Column**: Configuration object with name, function, tables, topics, and function\_args
- **Topic**: Configuration object with name and list of Field objects
- **Field**: Simple configuration object with name attribute

**Data Access Classes**

- **DBBase**: Abstract base class providing database engine management, connection handling, and common operations
- **InfluxDbDao**: Inherits from DBBase, handles InfluxDB connections and time-series queries
- **ButlerDao**: Inherits from DBBase, manages Butler repository access for exposure/visit metadata
- **ExposureEfdDao**: Inherits from DBBase, handles exposure\_efd table operations
- **VisitEfdDao**: Inherits from DBBase, handles visit1\_efd table operations
- **TransformdDao**: Inherits from DBBase, manages task scheduling metadata

**Management Classes**

- **QueueManager**: Task scheduling and workflow coordination using TransformdDao
- **TransformEfd**: Main application entry point that orchestrates all components

**Key Relationships**

1. **Transform** creates and uses **ButlerDao** for metadata access
2. **Transform** queries **InfluxDbDao** for EFD telemetry data
3. **Transform** instantiates **Summary** objects for statistical computations
4. **Transform** validates **ConfigModel** for configuration-driven processing
5. **ConfigModel** contains lists of **Column** objects
6. **Column** objects reference lists of **Topic** objects
7. **Topic** objects contain lists of **Field** objects
8. All specialized DAOs inherit from **DBBase** for consistent database operations
9. **TransformEfd** initializes and coordinates **Transform** and **QueueManager**
10. **TransformEfd** creates **Butler** instances and **InfluxDbDao** connections
11. **QueueManager** manages tasks via **TransformdDao**
12. **Transform** stores results via **ExposureEfdDao** and **VisitEfdDao**

**Key Relationship Patterns**

**1. Composition and Dependency Injection**

- Transform class receives all its dependencies (Butler, InfluxDbDao, config) through constructor injection
- This enables flexible testing and configuration without tight coupling

**2. Configuration-Driven Architecture**

- ConfigModel validates YAML configurations and provides structured access to Column, Topic, and Field definitions
- Transform class uses configuration to drive all processing logic without hardcoded transformations

**3. Data Access Object Pattern**

- All DAOs inherit from DBBase, providing consistent database operations
- Specialized DAOs (ExposureEfdDao, VisitEfdDao, TransformdDao) handle specific table operations
- Transform class uses DAOs for all data persistence operations

**4. Strategy Pattern for Transformations**

- Summary class provides pluggable transformation functions (mean, stddev, etc.)
- Transform class dynamically instantiates Summary objects and calls transformation methods based on configuration

**5. Template Method Pattern**

- Transform.process\_interval() defines the high-level processing algorithm
- Specific processing steps (\_map\_topics, \_compute\_column\_value, etc.) can be overridden for custom behavior

**6. Observer Pattern via Logging**

- All classes use structured logging for monitoring and debugging
- @handle\_processing\_errors decorator provides consistent error handling across Transform methods

**Data Flow Relationships**

1. **Application Flow**: CLI arguments → TransformEfd initialization → Component coordination
2. **Configuration Flow**: YAML files → ConfigModel validation → Transform initialization
3. **Metadata Flow**: Butler → ButlerDao → Transform for exposure/visit information
4. **Telemetry Flow**: InfluxDB → InfluxDbDao → Transform for EFD data retrieval
5. **Transformation Flow**: EFD data → Summary → Transform for statistical processing
6. **Storage Flow**: Transform → DAOs → PostgreSQL for result persistence
7. **Scheduling Flow**: QueueManager → TransformdDao → Transform for task coordination

**Integration Points for Extensions**

- **New Data Sources**: Add new DAO classes inheriting from DBBase
- **New Transformations**: Add methods to Summary class
- **New Output Formats**: Extend Transform.\_store\_results() method
- **Custom Processing**: Override Transform.\_compute\_column\_value() method
- **Alternative Scheduling**: Replace QueueManager with custom task coordination

Service Operation Flow
----------------------

The transformed EFD service runs in two ways:

1. **Direct Python**: Run ``transform_efd.py`` with command line arguments
2. **Docker Container**: Run in Kubernetes cluster

Both methods use the same code. The diagram shows the processing flow:

.. mermaid::

   flowchart TD
      Start([Service Start]) --> ExecutionMode{Execution Method?}

      ExecutionMode -->|Direct Python| ParseCLI[Parse CLI Arguments<br/>- Config file<br/>- Instrument<br/>- Time range<br/>- Database connections]
      ExecutionMode -->|Containerized| LoadEnv[Load Environment Variables<br/>- CONFIG_FILE<br/>- INSTRUMENT<br/>- BUTLER_REPO<br/>- CONSDB_URL<br/>- EFD<br/>- TIMEDELTA]

      ParseCLI --> ValidateConfig[Validate Configuration<br/>- Load YAML config<br/>- Validate with Pydantic<br/>- Check schema compatibility]
      LoadEnv --> ValidateConfig

      ValidateConfig --> InitLogging[Initialize Logging<br/>- Setup structured logging<br/>- Configure file/console output<br/>- Set log levels]
      InitLogging --> InitComponents[Initialize Core Components]

      subgraph InitComponents[Component Initialization]
        InitButler[Initialize ButlerDAO<br/>- Connect to Butler repo<br/>- Setup metadata access]
        InitEFD[Initialize InfluxDbDAO<br/>- Connect to EFD InfluxDB<br/>- Setup authentication<br/>- Configure query limits]
        InitTransform[Initialize Transform<br/>- Load configuration<br/>- Setup processing pipeline<br/>- Configure commit settings]
        InitQueue[Initialize QueueManager<br/>- Connect to task database<br/>- Setup task scheduling<br/>- Check for orphaned tasks]
      end

      InitComponents --> ModeDecision{Execution Mode?}

      ModeDecision -->|Job Mode| CreateJobTasks[Create Job Tasks<br/>- Parse start/end times<br/>- Generate time intervals<br/>- Create task records]
      ModeDecision -->|Cronjob Mode| GetCronTasks[Get Cronjob Tasks<br/>- Check for pending tasks<br/>- Handle failed retries<br/>- Create new intervals]

      CreateJobTasks --> ProcessTasks[Core Processing Loop]
      GetCronTasks --> ProcessTasks

      subgraph ProcessTasks[Core Processing Loop]
        GetTask[Get Next Task<br/>- Query task queue<br/>- Select pending/idle task<br/>- Update status to 'running']

        GetTask --> TaskExists{Task Available?}
        TaskExists -->|No| WaitForTask[Wait for New Tasks<br/>- Sleep interval<br/>- Check for new tasks]
        WaitForTask --> GetTask

        TaskExists -->|Yes| QueryButler[Query Butler for Metadata<br/>- Get exposures in time range<br/>- Get visits in time range<br/>- Extract timespan boundaries]

        QueryButler --> HasData{Data Found?}
        HasData -->|No| LogEmpty[Log Empty Result<br/>- Update task status<br/>- Mark as completed]
        LogEmpty --> GetTask

        HasData -->|Yes| MapTopics[Map & Optimize Topics<br/>- Group columns by topic<br/>- Minimize EFD queries<br/>- Setup server aggregation]

        MapTopics --> QueryEFD[Query EFD for Telemetry<br/>- Execute time series queries<br/>- Handle packed series<br/>- Apply time offsets]

        QueryEFD --> ProcessColumns[Process Each Column<br/>- Filter to exposure/visit bounds<br/>- Apply statistical functions<br/>- Compute metric values]

        ProcessColumns --> StoreResults[Store Results<br/>- Upsert to exposure_efd<br/>- Upsert to visit1_efd<br/>- Handle unpivoted tables]

        StoreResults --> UpdateTask[Update Task Status<br/>- Mark task completed<br/>- Record processing counts<br/>- Log success metrics]

        UpdateTask --> ErrorCheck{Processing Error?}
        ErrorCheck -->|Yes| HandleError[Handle Processing Error<br/>- Log error details<br/>- Mark task failed<br/>- Increment retry count]
        ErrorCheck -->|No| GetTask
        HandleError --> GetTask
      end

      ProcessTasks --> ShutdownCheck{Shutdown Signal?}
      ShutdownCheck -->|No| ProcessTasks
      ShutdownCheck -->|Yes| GracefulShutdown[Graceful Shutdown<br/>- Complete current task<br/>- Update orphaned tasks<br/>- Close connections]

      GracefulShutdown --> FinalSummary[Final Processing Summary<br/>- Log total statistics<br/>- Report completion status<br/>- Cleanup resources]

**Processing Steps:**

1. **Start**
   - Parse arguments or load environment variables
   - Load YAML config file
   - Initialize logging and components

2. **Task Management**
   - **Job Mode**: Create tasks for specific time range
   - **Cronjob Mode**: Create tasks continuously
   - Clean up orphaned tasks

3. **Process Data**
   - Get task from queue
   - Query Butler for exposures/visits
   - Query EFD for telemetry data
   - Apply transformations
   - Store results in database

4. **Error Handling**
   - Log errors
   - Retry failed tasks
   - Handle shutdown signals

5. **Finish**
   - Log statistics
   - Clean up resources

Key Processing Methods
----------------------

Transform.process\_interval()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Main method that processes data for a time range:

1. Query Butler for exposures and visits
2. Group columns by topic to reduce queries
3. Process each topic and apply transformations
4. Store results in database
5. Update task status

Transform.\_map\_topics()
~~~~~~~~~~~~~~~~~~~~~~~~~

Groups similar EFD queries to reduce database calls:

- Groups columns by topic, packed\_series, start\_offset, and aggregation settings
- Reduces queries from hundreds to 10-50 per processing run
- Enables server-side aggregation when configured

Transform.\_compute\_column\_value()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Applies statistical functions to time-series data:

1. Filter data to exposure/visit time boundaries
2. Handle missing data and NaN values
3. Apply statistical functions (mean, stddev, max, min, etc.)
4. Return computed values

Transform.\_query\_efd\_values()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Queries InfluxDB for telemetry data:

- Handles regular and packed time series
- Groups fields into batches (max 100 per query)
- Applies time offsets
- Manages connections and handles errors

Summary.apply()
~~~~~~~~~~~~~~~

Calls the correct statistical method:

1. Check for empty datasets
2. Call the requested method (mean, stddev, etc.)
3. Handle errors
4. Return None for invalid operations

QueueManager.create\_tasks()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Creates processing tasks for time intervals:

- Creates tasks in 5-minute chunks (default)
- Checks for existing tasks to avoid duplicates
- Sets initial status to 'pending'
- Links tasks to Butler repositories

Task status: pending → running → completed/failed → retry (if failed)

Execution Methods
-----------------

Direct Python Execution
~~~~~~~~~~~~~~~~~~~~~~~

For development and testing:

.. code-block:: bash

   python transform_efd.py \
     -c config_latiss.yaml \
     -i latiss \
     -r s3://rubin-summit-users/butler.yaml \
     -d postgresql://user:pass@host:port/db \
     -E "efd_latiss" \
     -m job \
     -s 2024-01-01T00:00:00 \
     -e 2024-01-01T01:00:00 \
     -t 5 \
     -w 1 \
     -l /path/to/logfile.log \
     -R

Required arguments:

- ``-c, --config``: YAML config file path
- ``-i, --instrument``: Instrument name (converted to lowercase)
- ``-r, --repo``: Butler repository path (default: s3://rubin-summit-users/butler.yaml)
- ``-d, --db``: Database connection string
- ``-E, --efd``: EFD connection string
- ``-m, --mode``: Execution mode (job or cronjob)

Optional arguments:

- ``-s, --start``: Start time in ISO format (required for job mode)
- ``-e, --end``: End time in ISO format (required for job mode)
- ``-t, --timedelta``: Processing interval in minutes (default: 5)
- ``-w, --timewindow``: Overlap window in minutes (default: 1)
- ``-l, --logfile``: Log file path (optional, logs to console if not specified)
- ``-R, --resume``: Resume pending tasks (flag, no value required)

Docker Container Execution
~~~~~~~~~~~~~~~~~~~~~~~~~~

For execution in a Kubernetes cluster please see the `Operator Guide <../operator-guide/transformed-efd.html>`_.

Secrets and Credentials Management
----------------------------------

The transformed EFD service integrates with the default vault system for secure management of secrets, passwords, and connection credentials. This ensures that sensitive information is not exposed in configuration files or command-line arguments.

- **Database Credentials**: PostgreSQL connection strings and authentication tokens are retrieved from the vault system
- **EFD Authentication**: InfluxDB credentials and API keys are managed securely through the vault
- **Butler Repository Access**: Butler repository authentication credentials are handled via vault integration
- **Default Passwords**: System default passwords and service account credentials are centrally managed


Data Transformation Functions
-----------------------------

Available in Summary class:

- mean(): Arithmetic mean ignoring NaN values
- stddev(): Standard deviation with configurable degrees of freedom
- max()/min(): Maximum/minimum values
- rms\_from\_polynomial\_fit(): RMS after polynomial detrending
- most\_recent\_value(): Most recent scalar value

Extension Patterns
------------------

Adding New Transformation Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Add method to Summary class in summary.py:

.. code-block:: python

   def median(self) -> float:
       """Calculate the median, ignoring NaN values."""
       values = self._get_numeric_values()
       if len(values) == 0:
           return np.nan
       return np.nanmedian(values)

2. Add comprehensive tests in tests/transformed\_efd/test\_summary.py
3. Update documentation with usage examples

Extending Configuration Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Add field to appropriate Pydantic model in config\_model.py
2. Update validation logic if needed
3. Modify schema generation in generate\_schema\_from\_config.py
4. Update transformation logic to handle new option

Adding New Data Sources
~~~~~~~~~~~~~~~~~~~~~~~

1. Create new DAO class inheriting from DBBase
2. Implement data retrieval methods with proper error handling
3. Integrate with transformation pipeline in transform.py
4. Add tests for new data source integration

Error Handling Strategy
-----------------------

- Decorator-based: @handle\_processing\_errors decorator for consistent error logging
- Graceful Degradation: Continue processing when individual transformations fail
- Comprehensive Logging: Detailed error context for debugging
- Validation First: Pydantic models validate configurations before processing


Common Development Scenarios
----------------------------

This section provides complete end-to-end examples for typical development tasks.

Scenario 1: Adding a New Statistical Function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal**: Add a median calculation function to the Summary class.

**Complete workflow:**

1. **Add the method to Summary class:**

.. code-block:: python

   # In summary.py
   def median(self) -> float:
       """Calculate the median, ignoring NaN values."""
       values = self._get_numeric_values()
       if len(values) == 0:
           return np.nan
       return np.nanmedian(values)

2. **Add comprehensive tests:**

.. code-block:: python

   # In tests/transformed_efd/test_summary.py
   def test_median(summary_instance):
       """Test median calculation with valid data."""
       assert summary_instance.median() == 3.0

3. **Use in configuration:**

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

Scenario 2: Adding Support for a New Instrument
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal**: Add support for a new instrument called "NewCam".

**Complete workflow:**

1. **Create configuration file:**

.. code-block:: bash

   cp python/lsst/consdb/transformed_efd/config/config_latiss.yaml \
      python/lsst/consdb/transformed_efd/config/config_newcam.yaml

2. **Edit configuration for NewCam:**

.. code-block:: yaml

   # In config_newcam.yaml
   version: "1.0.0"
   columns:
     - name: newcam_dome_temperature_mean
       tables: ["exposure_efd", "visit1_efd"]
       function: mean
       datatype: float
       ivoa: {"unit": "deg_C", "ucd": "phys.temperature;stat.mean"}
       description: Mean dome temperature for NewCam.
       packed_series: false
       topics:
         - name: lsst.sal.ESS.temperature
           fields:
             - name: domeAirTemperature

3. **Generate schema:**

.. code-block:: bash

   python ./python/lsst/consdb/transformed_efd/generate_schema_from_config.py --instrument newcam

4. **Create Alembic migration:**

.. code-block:: bash

   alembic -n efd_newcam revision --autogenerate -m "Add NewCam instrument support"

5. **Test the configuration:**

.. code-block:: bash

   python -m pytest tests/transformed_efd/test_config_model.py -v

Scenario 3: Adding a New Data Source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal**: Add support for querying a new external API for additional telemetry data.

**Complete workflow:**

1. **Create new DAO class:**

.. code-block:: python

   # In dao/new_api.py
   from .base import DBBase

   class NewApiDao(DBBase):
       def __init__(self, api_url: str, api_key: str):
           self.api_url = api_url
           self.api_key = api_key

       def get_telemetry_data(self, start_time: str, end_time: str):
           # Implementation for API calls
           pass

2. **Integrate with Transform class:**

.. code-block:: python

   # In transform.py, add to __init__
   self.new_api = NewApiDao(api_url, api_key)

   # Add method to query new data source
   def _query_new_api_data(self, start_time, end_time):
       return self.new_api.get_telemetry_data(start_time, end_time)

3. **Add tests:**

.. code-block:: python

   # In tests/transformed_efd/test_new_api.py
   def test_new_api_dao():
       dao = NewApiDao("http://api.example.com", "test-key")
       data = dao.get_telemetry_data("2023-01-01", "2023-01-02")
       assert data is not None

Scenario 4: Modifying Data Processing Logic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal**: Add custom preprocessing for specific telemetry topics.

**Complete workflow:**

1. **Override processing method:**

.. code-block:: python

   # In transform.py, extend the Transform class
   def _preprocess_telemetry_data(self, data, topic_name):
       if topic_name == "lsst.sal.ESS.temperature":
           # Apply temperature-specific preprocessing
           data = self._apply_temperature_corrections(data)
       return data

2. **Integrate into processing pipeline:**

.. code-block:: python

   # In _process_topic method
   def _process_topic(self, topic_config, start_time, end_time):
       # Get raw data
       raw_data = self._query_efd_values(topic_config, start_time, end_time)

       # Apply preprocessing
       processed_data = self._preprocess_telemetry_data(raw_data, topic_config.name)

       # Continue with normal processing
       return self._compute_column_values(processed_data, topic_config)

3. **Add configuration support:**

.. code-block:: yaml

   # In config file, add preprocessing options
   topics:
     - name: lsst.sal.ESS.temperature
       fields:
         - name: domeAirTemperature
       preprocessing:
         apply_temperature_correction: true

Scenario 5: Working with Scheduler Tables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal**: Monitor and manage processing tasks in the scheduler tables.

**Complete workflow:**

1. **Query task status:**

.. code-block:: python

   # In your monitoring script
   from lsst.consdb.transformed_efd.dao.transformd import TransformdDao

   dao = TransformdDao(db_uri, instrument="latiss", schema="efd_scheduler")

   # Get recent tasks
   recent_tasks = dao.select_recent(limit=10)
   for task in recent_tasks:
       print(f"Task {task['id']}: {task['status']} - {task['start_time']} to {task['end_time']}")

2. **Monitor task processing:**

.. code-block:: python

   # Check task metrics
   total_tasks = dao.count()
   failed_tasks = dao.select_queued(status="failed")
   running_tasks = dao.select_queued(status="running")
   stale_tasks = dao.select_queued(status="stale")

   print(f"Total tasks: {total_tasks}")
   print(f"Failed tasks: {len(failed_tasks)}")
   print(f"Running tasks: {len(running_tasks)}")
   print(f"Stale tasks: {len(stale_tasks)}")

3. **Handle orphaned tasks:**

.. code-block:: python

   # Clean up orphaned tasks
   orphaned_count = dao.fail_orphaned_tasks()
   print(f"Marked {orphaned_count} tasks as orphaned")

4. **Create custom task management:**

.. code-block:: python

   # Custom task retry logic
   def retry_failed_tasks(dao, max_retries=3):
       failed_tasks = dao.select_queued(status="failed")
       for task in failed_tasks:
           if task['retries'] < max_retries:
               dao.update(task['id'], {
                   'status': 'pending',
                   'retries': task['retries'] + 1,
                   'error': None
               })
               print(f"Retrying task {task['id']}")

   # Clean up stale tasks
   def cleanup_stale_tasks(dao, days_old=30):
       from datetime import datetime, timedelta
       cutoff_date = datetime.now() - timedelta(days=days_old)
       stale_tasks = dao.select_queued(status="stale")
       for task in stale_tasks:
           if task['created_at'] < cutoff_date:
               dao.delete(task['id'])
               print(f"Deleted stale task {task['id']}")

Code Organization
-----------------

::

    python/lsst/consdb/transformed_efd/
    ├── __init__.py          # Module documentation and exports
    ├── config/              # Instrument configuration YAML files
    ├── config_model.py      # Pydantic validation models
    ├── dao/                 # Data access objects
    │   ├── __init__.py
    │   ├── base.py          # DBBase foundation class
    │   ├── butler.py        # Butler metadata access
    │   ├── influxdb.py      # EFD data querying
    │   ├── exposure_efd.py  # Output table operations
    │   ├── visit_efd.py
    │   └── transformd.py    # Task scheduling
    ├── generate_schema_from_config.py  # Schema generation
    ├── queue_manager.py     # Task scheduling
    ├── schemas/             # Generated database schemas
    ├── summary.py           # Statistical processing
    ├── transform.py         # Main transformation logic
    └── transform_efd.py     # CLI entry point
