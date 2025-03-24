# This file is part of consdb.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
