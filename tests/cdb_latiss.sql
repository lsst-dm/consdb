
CREATE TABLE main.exposure (
	exposure_id BIGINT NOT NULL, 
	exposure_name VARCHAR(20) NOT NULL, 
	controller VARCHAR(1) NOT NULL, 
	day_obs BIGINT NOT NULL, 
	seq_num BIGINT NOT NULL, 
	physical_filter TEXT, 
	band TEXT, 
	s_ra DOUBLE, 
	s_dec DOUBLE, 
	sky_rotation DOUBLE, 
	azimuth_start DOUBLE, 
	azimuth_end DOUBLE, 
	azimuth DOUBLE, 
	altitude_start DOUBLE, 
	altitude_end DOUBLE, 
	altitude DOUBLE, 
	zenith_distance_start DOUBLE, 
	zenith_distance_end DOUBLE, 
	zenith_distance DOUBLE, 
	airmass DOUBLE, 
	exp_midpt TIMESTAMP, 
	exp_midpt_mjd DOUBLE, 
	obs_start TIMESTAMP, 
	obs_start_mjd DOUBLE, 
	obs_end TIMESTAMP, 
	obs_end_mjd DOUBLE, 
	exp_time DOUBLE, 
	shut_time DOUBLE, 
	dark_time DOUBLE, 
	group_id TEXT, 
	cur_index INTEGER, 
	max_index INTEGER, 
	img_type TEXT, 
	emulated BOOLEAN, 
	science_program TEXT, 
	observation_reason TEXT, 
	target_name TEXT, 
	shutter_open_begin TIMESTAMP, 
	shutter_open_end TIMESTAMP, 
	shutter_close_begin TIMESTAMP, 
	shutter_close_end TIMESTAMP, 
	air_temp FLOAT, 
	pressure FLOAT, 
	humidity FLOAT, 
	wind_speed FLOAT, 
	wind_dir FLOAT, 
	dimm_seeing FLOAT, 
	shut_lower FLOAT, 
	shut_upper FLOAT, 
	focus_z FLOAT, 
	dome_azimuth FLOAT, 
	simulated BOOLEAN, 
	PRIMARY KEY (day_obs, seq_num), 
	CONSTRAINT un_exposure_id UNIQUE (exposure_id)
)

;

CREATE TABLE main.exposure_flexdata_schema (
	"key" TEXT NOT NULL, 
	dtype TEXT NOT NULL, 
	doc TEXT NOT NULL, 
	unit TEXT, 
	ucd TEXT, 
	PRIMARY KEY ("key")
)

;

CREATE TABLE main.exposure_flexdata (
	obs_id BIGINT NOT NULL, 
	"key" TEXT NOT NULL, 
	value TEXT, 
	PRIMARY KEY (obs_id, "key"), 
	CONSTRAINT fk_obs_id FOREIGN KEY(obs_id) REFERENCES exposure (exposure_id), 
	CONSTRAINT fk_key FOREIGN KEY("key") REFERENCES exposure_flexdata_schema ("key")
)

;
