
CREATE TABLE cdb_latiss.exposure_efd (
	exposure_id BIGINT, 
	created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP, 
	instrument CHAR(20), 
	PRIMARY KEY (exposure_id, instrument), 
	CONSTRAINT un_exposure_id_instrument UNIQUE (exposure_id, instrument)
)

;
COMMENT ON TABLE cdb_latiss.exposure_efd IS 'Transformed EFD topics by exposure.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.exposure_id IS 'Exposure unique ID.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.created_at IS 'Timestamp when the record was created, default is the current timestamp';
COMMENT ON COLUMN cdb_latiss.exposure_efd.instrument IS 'Instrument name.';
COMMENT ON CONSTRAINT un_exposure_id_instrument ON cdb_latiss.exposure_efd IS 'Ensure exposure_id is unique.';

CREATE TABLE cdb_latiss.exposure_efd_unpivoted (
	exposure_id INTEGER NOT NULL, 
	property CHAR(255) NOT NULL, 
	field CHAR(255) NOT NULL, 
	value DOUBLE PRECISION, 
	created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (exposure_id, property, field), 
	CONSTRAINT un_exposure_property_field UNIQUE (exposure_id, property, field)
)

;
COMMENT ON TABLE cdb_latiss.exposure_efd_unpivoted IS 'Unpivoted EFD exposure data.';
COMMENT ON COLUMN cdb_latiss.exposure_efd_unpivoted.exposure_id IS 'Unique identifier for the exposure';
COMMENT ON COLUMN cdb_latiss.exposure_efd_unpivoted.property IS 'Property name for the unpivoted data';
COMMENT ON COLUMN cdb_latiss.exposure_efd_unpivoted.field IS 'Field name for the unpivoted data';
COMMENT ON COLUMN cdb_latiss.exposure_efd_unpivoted.value IS 'Value corresponding to the parameter';
COMMENT ON COLUMN cdb_latiss.exposure_efd_unpivoted.created_at IS 'Timestamp when the record was created, default is the current timestamp';
COMMENT ON CONSTRAINT un_exposure_property_field ON cdb_latiss.exposure_efd_unpivoted IS 'Ensure the combination of exposure_id, property, and field is unique.';

CREATE TABLE cdb_latiss.visit1_efd (
	visit_id BIGINT, 
	created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP, 
	instrument CHAR(20), 
	PRIMARY KEY (visit_id, instrument), 
	CONSTRAINT un_visit_id_instrument UNIQUE (visit_id, instrument)
)

;
COMMENT ON TABLE cdb_latiss.visit1_efd IS 'Transformed EFD topics by visit.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.visit_id IS 'Visit unique ID.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.created_at IS 'Timestamp when the record was created, default is the current timestamp';
COMMENT ON COLUMN cdb_latiss.visit1_efd.instrument IS 'Instrument name.';
COMMENT ON CONSTRAINT un_visit_id_instrument ON cdb_latiss.visit1_efd IS 'Ensure visit_id is unique.';

CREATE TABLE cdb_latiss.visit1_efd_unpivoted (
	visit_id INTEGER NOT NULL, 
	property CHAR(255) NOT NULL, 
	field CHAR(255) NOT NULL, 
	value DOUBLE PRECISION, 
	created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (visit_id, property, field), 
	CONSTRAINT un_visit_property_field UNIQUE (visit_id, property, field)
)

;
COMMENT ON TABLE cdb_latiss.visit1_efd_unpivoted IS 'Unpivoted EFD visit data.';
COMMENT ON COLUMN cdb_latiss.visit1_efd_unpivoted.visit_id IS 'Unique identifier for the visit';
COMMENT ON COLUMN cdb_latiss.visit1_efd_unpivoted.property IS 'Property name for the unpivoted data';
COMMENT ON COLUMN cdb_latiss.visit1_efd_unpivoted.field IS 'Field name for the unpivoted data';
COMMENT ON COLUMN cdb_latiss.visit1_efd_unpivoted.value IS 'Value corresponding to the parameter';
COMMENT ON COLUMN cdb_latiss.visit1_efd_unpivoted.created_at IS 'Timestamp when the record was created, default is the current timestamp';
COMMENT ON CONSTRAINT un_visit_property_field ON cdb_latiss.visit1_efd_unpivoted IS 'Ensure the combination of visit_id, property, and field is unique.';

CREATE TABLE cdb_latiss.transformed_efd_scheduler (
	id SERIAL NOT NULL, 
	start_time TIMESTAMP WITHOUT TIME ZONE, 
	end_time TIMESTAMP WITHOUT TIME ZONE, 
	timewindow INTEGER, 
	status CHAR(20) DEFAULT 'pending', 
	process_start_time TIMESTAMP WITHOUT TIME ZONE, 
	process_end_time TIMESTAMP WITHOUT TIME ZONE, 
	process_exec_time INTEGER DEFAULT 0, 
	exposures INTEGER DEFAULT 0, 
	visits1 INTEGER DEFAULT 0, 
	retries INTEGER DEFAULT 0, 
	error TEXT, 
	created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (id), 
	CONSTRAINT un_id UNIQUE (id)
)

;
COMMENT ON TABLE cdb_latiss.transformed_efd_scheduler IS 'Transformed EFD scheduler.';
COMMENT ON COLUMN cdb_latiss.transformed_efd_scheduler.id IS 'Unique ID, auto-incremented';
COMMENT ON COLUMN cdb_latiss.transformed_efd_scheduler.start_time IS 'Start time of the transformation interval, must be provided';
COMMENT ON COLUMN cdb_latiss.transformed_efd_scheduler.end_time IS 'End time of the transformation interval, must be provided';
COMMENT ON COLUMN cdb_latiss.transformed_efd_scheduler.timewindow IS 'Time window used to expand start and end times by, in minutes';
COMMENT ON COLUMN cdb_latiss.transformed_efd_scheduler.status IS 'Status of the process, default is ''pending''';
COMMENT ON COLUMN cdb_latiss.transformed_efd_scheduler.process_start_time IS 'Timestamp when the process started';
COMMENT ON COLUMN cdb_latiss.transformed_efd_scheduler.process_end_time IS 'Timestamp when the process ended';
COMMENT ON COLUMN cdb_latiss.transformed_efd_scheduler.process_exec_time IS 'Execution time of the process in seconds, default is 0';
COMMENT ON COLUMN cdb_latiss.transformed_efd_scheduler.exposures IS 'Number of exposures processed, default is 0';
COMMENT ON COLUMN cdb_latiss.transformed_efd_scheduler.visits1 IS 'Number of visits recorded, default is 0';
COMMENT ON COLUMN cdb_latiss.transformed_efd_scheduler.retries IS 'Number of retries attempted, default is 0';
COMMENT ON COLUMN cdb_latiss.transformed_efd_scheduler.error IS 'Error message, if any';
COMMENT ON COLUMN cdb_latiss.transformed_efd_scheduler.created_at IS 'Timestamp when the record was created, default is the current timestamp';
COMMENT ON CONSTRAINT un_id ON cdb_latiss.transformed_efd_scheduler IS 'Ensure id is unique.';
