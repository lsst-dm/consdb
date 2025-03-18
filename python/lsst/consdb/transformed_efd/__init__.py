"""Provides a structured framework for processing and transforming data from the (EFD).

Overview:
---------
This module offers tools for accessing, transforming, and managing EFD data, supporting
workflows and integration with the LSST ecosystem. It includes capabilities for
data retrieval, transformation pipelines, configuration management, and schema
generation.

Components:
-----------
- **Data Access**: The `dao` subpackage provides Data Access Objects (DAOs) to interact
  with specific database tables such as `exposure_efd` and `visit_efd`.
- **Data Transformation**: Includes utilities for applying structured transformations
  to EFD data, including summarization and restructuring.
- **Configuration Handling**: Supports loading and validating instrument configurations
  through YAML files for flexible setup and operation.
- **Schema Generation**: Automates the creation of database schemas based on predefined
  instrument configurations.
- **Queue Management**: Implements tools for task scheduling and queue-based workflows.

Submodules:
-----------
- `dao`: Contains DAOs for database interactions.
- `config_model`: Defines models for validating YAML configurations.
- `generate_schema`: Includes schema generation utilities.
- `summary`: Provides tools for summarizing EFD data.
- `transform`: Manages transformation pipelines.
- `transform_efd`: Contains specialized transformation methods.
- `queue_manager`: Handles task queue management.

Configuration Files:
--------------------
The module uses YAML files for instrument-specific configurations:
- `config_latiss.yaml`: Configuration for LATISS.
- `config_lsstcomcam.yaml`: Configuration for LSSTComCam.
- `config_lsstcomcamsim.yaml`: Configuration for LSSTComCamSim.

"""
