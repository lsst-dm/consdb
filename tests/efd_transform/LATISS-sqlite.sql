
CREATE TABLE main.exposure_efd (
	exposure_id BIGINT,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	instrument CHAR(20),
	PRIMARY KEY (exposure_id, instrument),
	CONSTRAINT un_exposure_id_instrument UNIQUE (exposure_id, instrument)
)

;

CREATE TABLE main.exposure_efd_unpivoted (
	exposure_id INTEGER NOT NULL,
	property CHAR(255) DEFAULT 'default_property' NOT NULL,
	field CHAR(255) DEFAULT 'default_field' NOT NULL,
	value DOUBLE,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (exposure_id, property, field),
	CONSTRAINT un_exposure_property_field UNIQUE (exposure_id, property, field)
)

;

CREATE TABLE main.visit1_efd (
	visit_id BIGINT,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	instrument CHAR(20),
	PRIMARY KEY (visit_id, instrument),
	CONSTRAINT un_visit_id_instrument UNIQUE (visit_id, instrument)
)

;

CREATE TABLE main.visit1_efd_unpivoted (
	visit_id INTEGER NOT NULL,
	property CHAR(255) DEFAULT 'default_property' NOT NULL,
	field CHAR(255) DEFAULT 'default_field' NOT NULL,
	value DOUBLE,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (visit_id, property, field),
	CONSTRAINT un_visit_property_field UNIQUE (visit_id, property, field)
)

;

CREATE TABLE main.transformed_efd_scheduler (
	id INTEGER NOT NULL,
	start_time TIMESTAMP,
	end_time TIMESTAMP,
	timewindow INTEGER,
	status CHAR(20) DEFAULT 'pending',
	process_start_time TIMESTAMP,
	process_end_time TIMESTAMP,
	process_exec_time INTEGER DEFAULT 0,
	exposures INTEGER DEFAULT 0,
	visits1 INTEGER DEFAULT 0,
	retries INTEGER DEFAULT 0,
	error TEXT,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id),
	CONSTRAINT un_id UNIQUE (id)
)

;
