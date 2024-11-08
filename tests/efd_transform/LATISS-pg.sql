
CREATE TABLE cdb_latiss.exposure_efd (
	exposure_id BIGINT,
	created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	instrument CHAR(20),
	at_mount_jitter_azimuth FLOAT,
	at_mount_jitter_elevation FLOAT,
	at_mount_jitter_nasmyth FLOAT,
	at_salindex201_sonic_temperature_mean FLOAT,
	at_salindex201_sonic_temperature_stddev FLOAT,
	at_salindex201_sonic_temperature_stddev_mean FLOAT,
	at_salindex201_sonic_temperature_stddev_stddev FLOAT,
	at_salindex205_sonic_temperature_mean FLOAT,
	at_salindex205_sonic_temperature_stddev FLOAT,
	at_salindex205_sonic_temperature_stddev_mean FLOAT,
	at_salindex205_sonic_temperature_stddev_stddev FLOAT,
	at_salindex201_wind_speed_x_mean FLOAT,
	at_salindex201_wind_speed_0_stddev FLOAT,
	at_salindex201_wind_speed_0_min FLOAT,
	at_salindex201_wind_speed_0_max FLOAT,
	at_salindex201_wind_speed_1_mean FLOAT,
	at_salindex201_wind_speed_1_stddev FLOAT,
	at_salindex201_wind_speed_1_min FLOAT,
	at_salindex201_wind_speed_1_max FLOAT,
	at_salindex201_wind_speed_2_mean FLOAT,
	at_salindex201_wind_speed_2_stddev FLOAT,
	at_salindex201_wind_speed_2_min FLOAT,
	at_salindex201_wind_speed_2_max FLOAT,
	at_salindex201_wind_speed_speedstddev_0_mean FLOAT,
	at_salindex201_wind_speed_speedstddev_0_stddev FLOAT,
	at_salindex201_wind_speed_speedstddev_0_min FLOAT,
	at_salindex201_wind_speed_speedstddev_0_max FLOAT,
	at_salindex201_wind_speed_speedstddev_1_mean FLOAT,
	at_salindex201_wind_speed_speedstddev_1_stddev FLOAT,
	at_salindex201_wind_speed_speedstddev_1_min FLOAT,
	at_salindex201_wind_speed_speedstddev_1_max FLOAT,
	at_salindex201_wind_speed_speedstddev_2_mean FLOAT,
	at_salindex201_wind_speed_speedstddev_2_stddev FLOAT,
	at_salindex201_wind_speed_speedstddev_2_min FLOAT,
	at_salindex201_wind_speed_speedstddev_2_max FLOAT,
	at_salindex201_wind_speed_magnitude_mean FLOAT,
	at_salindex201_wind_speed_magnitude_stddev FLOAT,
	at_salindex201_wind_speed_magnitude_min FLOAT,
	at_salindex201_wind_speed_magnitude_max FLOAT,
	at_salindex201_wind_speed_maxmagnitude_mean FLOAT,
	at_salindex201_wind_speed_maxmagnitude_stddev FLOAT,
	at_salindex201_wind_speed_maxmagnitude_min FLOAT,
	at_salindex201_wind_speed_maxmagnitude_max FLOAT,
	at_salindex204_wind_speed_0_mean FLOAT,
	at_salindex204_wind_speed_0_stddev FLOAT,
	at_salindex204_wind_speed_0_min FLOAT,
	at_salindex204_wind_speed_0_max FLOAT,
	at_salindex204_wind_speed_1_mean FLOAT,
	at_salindex204_wind_speed_1_stddev FLOAT,
	at_salindex204_wind_speed_1_min FLOAT,
	at_salindex204_wind_speed_1_max FLOAT,
	at_salindex204_wind_speed_2_mean FLOAT,
	at_salindex204_wind_speed_2_stddev FLOAT,
	at_salindex204_wind_speed_2_min FLOAT,
	at_salindex204_wind_speed_2_max FLOAT,
	at_salindex204_wind_speed_speedstddev_0_mean FLOAT,
	at_salindex204_wind_speed_speedstddev_0_stddev FLOAT,
	at_salindex204_wind_speed_speedstddev_0_min FLOAT,
	at_salindex204_wind_speed_speedstddev_0_max FLOAT,
	at_salindex204_wind_speed_speedstddev_1_mean FLOAT,
	at_salindex204_wind_speed_speedstddev_1_stddev FLOAT,
	at_salindex204_wind_speed_speedstddev_1_min FLOAT,
	at_salindex204_wind_speed_speedstddev_1_max FLOAT,
	at_salindex204_wind_speed_speedstddev_2_mean FLOAT,
	at_salindex204_wind_speed_speedstddev_2_stddev FLOAT,
	at_salindex204_wind_speed_speedstddev_2_min FLOAT,
	at_salindex204_wind_speed_speedstddev_2_max FLOAT,
	at_salindex204_wind_speed_magnitude_mean FLOAT,
	at_salindex204_wind_speed_magnitude_stddev FLOAT,
	at_salindex204_wind_speed_magnitude_min FLOAT,
	at_salindex204_wind_speed_magnitude_max FLOAT,
	at_salindex204_wind_speed_maxmagnitude_mean FLOAT,
	at_salindex204_wind_speed_maxmagnitude_stddev FLOAT,
	at_salindex204_wind_speed_maxmagnitude_min FLOAT,
	at_salindex204_wind_speed_maxmagnitude_max FLOAT,
	at_salindex205_wind_speed_0_mean FLOAT,
	at_salindex205_wind_speed_0_stddev FLOAT,
	at_salindex205_wind_speed_0_min FLOAT,
	at_salindex205_wind_speed_0_max FLOAT,
	at_salindex205_wind_speed_1_mean FLOAT,
	at_salindex205_wind_speed_1_stddev FLOAT,
	at_salindex205_wind_speed_1_min FLOAT,
	at_salindex205_wind_speed_1_max FLOAT,
	at_salindex205_wind_speed_2_mean FLOAT,
	at_salindex205_wind_speed_2_stddev FLOAT,
	at_salindex205_wind_speed_2_min FLOAT,
	at_salindex205_wind_speed_2_max FLOAT,
	at_salindex205_wind_speed_speedstddev_0_mean FLOAT,
	at_salindex205_wind_speed_speedstddev_0_stddev FLOAT,
	at_salindex205_wind_speed_speedstddev_0_min FLOAT,
	at_salindex205_wind_speed_speedstddev_0_max FLOAT,
	at_salindex205_wind_speed_speedstddev_1_mean FLOAT,
	at_salindex205_wind_speed_speedstddev_1_stddev FLOAT,
	at_salindex205_wind_speed_speedstddev_1_min FLOAT,
	at_salindex205_wind_speed_speedstddev_1_max FLOAT,
	at_salindex205_wind_speed_speedstddev_2_mean FLOAT,
	at_salindex205_wind_speed_speedstddev_2_stddev FLOAT,
	at_salindex205_wind_speed_speedstddev_2_min FLOAT,
	at_salindex205_wind_speed_speedstddev_2_max FLOAT,
	at_salindex205_wind_speed_magnitude_mean FLOAT,
	at_salindex205_wind_speed_magnitude_stddev FLOAT,
	at_salindex205_wind_speed_magnitude_min FLOAT,
	at_salindex205_wind_speed_magnitude_max FLOAT,
	at_salindex205_wind_speed_maxmagnitude_mean FLOAT,
	at_salindex205_wind_speed_maxmagnitude_stddev FLOAT,
	at_salindex205_wind_speed_maxmagnitude_min FLOAT,
	at_salindex205_wind_speed_maxmagnitude_max FLOAT,
	at_salindex201_airflow_speed_mean FLOAT,
	at_salindex201_airflow_speed_stddev FLOAT,
	at_salindex201_airflow_speed_min FLOAT,
	at_salindex201_airflow_speed_max FLOAT,
	at_salindex201_airflow_speedstddev_mean FLOAT,
	at_salindex201_airflow_speedstddev_stddev FLOAT,
	at_salindex201_airflow_speedstddev_min FLOAT,
	at_salindex201_airflow_speedstddev_max FLOAT,
	at_salindex201_airflow_direction_mean FLOAT,
	at_salindex201_airflow_direction_stddev FLOAT,
	at_salindex201_airflow_direction_min FLOAT,
	at_salindex201_airflow_direction_max FLOAT,
	at_salindex204_airflow_speed_mean FLOAT,
	at_salindex204_airflow_speed_stddev FLOAT,
	at_salindex204_airflow_speed_min FLOAT,
	at_salindex204_airflow_speed_max FLOAT,
	at_salindex204_airflow_speedstddev_mean FLOAT,
	at_salindex204_airflow_speedstddev_stddev FLOAT,
	at_salindex204_airflow_speedstddev_min FLOAT,
	at_salindex204_airflow_speedstddev_max FLOAT,
	at_salindex204_airflow_direction_mean FLOAT,
	at_salindex204_airflow_direction_stddev FLOAT,
	at_salindex204_airflow_direction_min FLOAT,
	at_salindex204_airflow_direction_max FLOAT,
	at_salindex205_airflow_speed_mean FLOAT,
	at_salindex205_airflow_speed_stddev FLOAT,
	at_salindex205_airflow_speed_min FLOAT,
	at_salindex205_airflow_speed_max FLOAT,
	at_salindex205_airflow_speedstddev_mean FLOAT,
	at_salindex205_airflow_speedstddev_stddev FLOAT,
	at_salindex205_airflow_speedstddev_min FLOAT,
	at_salindex205_airflow_speedstddev_max FLOAT,
	at_salindex205_airflow_direction_mean FLOAT,
	at_salindex205_airflow_direction_stddev FLOAT,
	at_salindex205_airflow_direction_min FLOAT,
	at_salindex205_airflow_direction_max FLOAT,
	at_salindex201_temperatureitem_0_mean FLOAT,
	at_salindex201_temperatureitem_0_stddev FLOAT,
	at_salindex201_temperatureitem_0_min FLOAT,
	at_salindex201_temperatureitem_0_max FLOAT,
	at_salindex201_temperatureitem_1_mean FLOAT,
	at_salindex201_temperatureitem_1_stddev FLOAT,
	at_salindex201_temperatureitem_1_min FLOAT,
	at_salindex201_temperatureitem_1_max FLOAT,
	at_salindex201_temperatureitem_2_mean FLOAT,
	at_salindex201_temperatureitem_2_stddev FLOAT,
	at_salindex201_temperatureitem_2_min FLOAT,
	at_salindex201_temperatureitem_2_max FLOAT,
	at_salindex201_temperatureitem_3_mean FLOAT,
	at_salindex201_temperatureitem_3_stddev FLOAT,
	at_salindex201_temperatureitem_3_min FLOAT,
	at_salindex201_temperatureitem_3_max FLOAT,
	at_salindex201_temperatureitem_4_mean FLOAT,
	at_salindex201_temperatureitem_4_stddev FLOAT,
	at_salindex201_temperatureitem_4_min FLOAT,
	at_salindex201_temperatureitem_4_max FLOAT,
	at_salindex201_temperatureitem_5_mean FLOAT,
	at_salindex201_temperatureitem_5_stddev FLOAT,
	at_salindex201_temperatureitem_5_min FLOAT,
	at_salindex201_temperatureitem_5_max FLOAT,
	at_salindex201_temperatureitem_6_mean FLOAT,
	at_salindex201_temperatureitem_6_stddev FLOAT,
	at_salindex201_temperatureitem_6_min FLOAT,
	at_salindex201_temperatureitem_6_max FLOAT,
	at_salindex201_temperatureitem_7_mean FLOAT,
	at_salindex201_temperatureitem_7_stddev FLOAT,
	at_salindex201_temperatureitem_7_min FLOAT,
	at_salindex201_temperatureitem_7_max FLOAT,
	at_salindex301_temperatureitem_0_mean FLOAT,
	at_salindex301_temperatureitem_0_stddev FLOAT,
	at_salindex301_temperatureitem_0_min FLOAT,
	at_salindex301_temperatureitem_0_max FLOAT,
	at_salindex301_temperatureitem_1_mean FLOAT,
	at_salindex301_temperatureitem_1_stddev FLOAT,
	at_salindex301_temperatureitem_1_min FLOAT,
	at_salindex301_temperatureitem_1_max FLOAT,
	at_salindex301_temperatureitem_2_mean FLOAT,
	at_salindex301_temperatureitem_2_stddev FLOAT,
	at_salindex301_temperatureitem_2_min FLOAT,
	at_salindex301_temperatureitem_2_max FLOAT,
	at_salindex301_temperatureitem_3_mean FLOAT,
	at_salindex301_temperatureitem_3_stddev FLOAT,
	at_salindex301_temperatureitem_3_min FLOAT,
	at_salindex301_temperatureitem_3_max FLOAT,
	at_salindex301_temperatureitem_4_mean FLOAT,
	at_salindex301_temperatureitem_4_stddev FLOAT,
	at_salindex301_temperatureitem_4_min FLOAT,
	at_salindex301_temperatureitem_4_max FLOAT,
	at_salindex301_temperatureitem_5_mean FLOAT,
	at_salindex301_temperatureitem_5_stddev FLOAT,
	at_salindex301_temperatureitem_5_min FLOAT,
	at_salindex301_temperatureitem_5_max FLOAT,
	at_salindex301_temperatureitem_6_mean FLOAT,
	at_salindex301_temperatureitem_6_stddev FLOAT,
	at_salindex301_temperatureitem_6_min FLOAT,
	at_salindex301_temperatureitem_6_max FLOAT,
	at_salindex301_temperatureitem_7_mean FLOAT,
	at_salindex301_temperatureitem_7_stddev FLOAT,
	at_salindex301_temperatureitem_7_min FLOAT,
	at_salindex301_temperatureitem_7_max FLOAT,
	at_azimuth_calculated_angle FLOAT,
	at_elevation_calculated_angle FLOAT,
	at_dimm_fwhm_mean FLOAT,
	at_azimuth_mean FLOAT,
	at_elevation_mean FLOAT,
	at_hexapod_reported_position_x_mean FLOAT,
	at_hexapod_reported_position_x_max FLOAT,
	at_hexapod_reported_position_x_min FLOAT,
	at_hexapod_reported_position_y_mean FLOAT,
	at_hexapod_reported_position_y_max FLOAT,
	at_hexapod_reported_position_y_min FLOAT,
	at_hexapod_reported_position_z_mean FLOAT,
	at_hexapod_reported_position_z_max FLOAT,
	at_hexapod_reported_position_z_min FLOAT,
	at_hexapod_reported_position_u_mean FLOAT,
	at_hexapod_reported_position_u_max FLOAT,
	at_hexapod_reported_position_u_min FLOAT,
	at_hexapod_reported_position_v_mean FLOAT,
	at_hexapod_reported_position_v_max FLOAT,
	at_hexapod_reported_position_v_min FLOAT,
	at_hexapod_reported_position_w_mean FLOAT,
	at_hexapod_reported_position_w_max FLOAT,
	at_hexapod_reported_position_w_min FLOAT,
	at_salindex202_acceleration_x_mean FLOAT,
	at_salindex202_acceleration_x_stddev FLOAT,
	at_salindex202_acceleration_x_min FLOAT,
	at_salindex202_acceleration_x_max FLOAT,
	at_salindey202_acceleration_y_mean FLOAT,
	at_salindex202_acceleration_y_stddev FLOAT,
	at_salindex202_acceleration_y_min FLOAT,
	at_salindex202_acceleration_y_max FLOAT,
	at_salindez202_acceleration_z_mean FLOAT,
	at_salindex202_acceleration_z_stddev FLOAT,
	at_salindex202_acceleration_z_min FLOAT,
	at_salindex202_acceleration_z_max FLOAT,
	at_salindex201_dewpoint_mean FLOAT,
	at_salindex201_relative_humidity_mean FLOAT,
	at_salindex201_pressure_item_0_mean FLOAT,
	at_salindex201_pressure_item_1_mean FLOAT,
	at_salindex301_pressure_item_0_mean FLOAT,
	at_salindex301_pressure_item_1_mean FLOAT,
	at_pointing_mount_position_ra_mean FLOAT,
	at_pointing_mount_position_ra_stddev FLOAT,
	at_pointing_mount_position_dec_mean FLOAT,
	at_pointing_mount_position_dec_stddev FLOAT,
	at_pointing_mount_position_sky_angle_mean FLOAT,
	at_pointing_mount_position_sky_angle_stddev FLOAT,
	PRIMARY KEY (exposure_id, instrument),
	CONSTRAINT un_exposure_id_instrument UNIQUE (exposure_id, instrument)
)

;
COMMENT ON TABLE cdb_latiss.exposure_efd IS 'Transformed EFD topics by exposure.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.exposure_id IS 'Exposure unique ID.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.created_at IS 'Timestamp when the record was created, default is the current timestamp';
COMMENT ON COLUMN cdb_latiss.exposure_efd.instrument IS 'Instrument name.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_mount_jitter_azimuth IS 'RMS after 4th order polynomial fit of azimuth axis position computed from the axis encoders at 100 Hz beginning at the specified time. The range is the hard stop limits (L3), approximately -280 to 280.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_mount_jitter_elevation IS 'RMS after 4th order polynomial fit of elevation axis position computed from the axis encoders at 100 Hz beginning at the specified time.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_mount_jitter_nasmyth IS 'RMS after 4th order polynomial fit of Nasmyth 1 axis position computed from the axis encoders, or nan if this axis is not in use. The range is the software limits (L1), approximately -175 to 175.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_sonic_temperature_mean IS 'Median sonic temperature (air temperature measured sonically). Sonic temperature has poor absolute accuracy (it can be off by several degrees) but good time resolution.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_sonic_temperature_stddev IS 'Median sonic temperature (air temperature measured sonically). Sonic temperature has poor absolute accuracy (it can be off by several degrees) but good time resolution.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_sonic_temperature_stddev_mean IS 'Standard devation of sonic temperature (air temperature measured sonically) estimated from quartiles.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_sonic_temperature_stddev_stddev IS 'Standard devation of sonic temperature (air temperature measured sonically) estimated from quartiles.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_sonic_temperature_mean IS 'Median sonic temperature (air temperature measured sonically). Sonic temperature has poor absolute accuracy (it can be off by several degrees) but good time resolution.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_sonic_temperature_stddev IS 'Median sonic temperature (air temperature measured sonically). Sonic temperature has poor absolute accuracy (it can be off by several degrees) but good time resolution.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_sonic_temperature_stddev_mean IS 'Standard devation of sonic temperature (air temperature measured sonically) estimated from quartiles.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_sonic_temperature_stddev_stddev IS 'Standard devation of sonic temperature (air temperature measured sonically) estimated from quartiles.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_wind_speed_x_mean IS 'Median wind speed (x, y, z) in AuxTel-ESS04 along axis 0 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_wind_speed_0_stddev IS 'Median wind speed (x, y, z) in AuxTel-ESS04 along axis 0 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_wind_speed_0_min IS 'Median wind speed (x, y, z) in AuxTel-ESS04 along axis 0 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_wind_speed_0_max IS 'Median wind speed (x, y, z) in AuxTel-ESS04 along axis 0 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_wind_speed_1_mean IS 'Median wind speed (x, y, z) in AuxTel-ESS04 along axis 1 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_wind_speed_1_stddev IS 'Median wind speed (x, y, z) in AuxTel-ESS04 along axis 1 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_wind_speed_1_min IS 'Median wind speed (x, y, z) in AuxTel-ESS04 along axis 1 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_wind_speed_1_max IS 'Median wind speed (x, y, z) in AuxTel-ESS04 along axis 1 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_wind_speed_2_mean IS 'Median wind speed (x, y, z) in AuxTel-ESS04 along axis 2 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_wind_speed_2_stddev IS 'Median wind speed (x, y, z) in AuxTel-ESS04 along axis 2 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_wind_speed_2_min IS 'Median wind speed (x, y, z) in AuxTel-ESS04 along axis 2 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_wind_speed_2_max IS 'Median wind speed (x, y, z) in AuxTel-ESS04 along axis 2 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_wind_speed_speedstddev_0_mean IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-ESS04 along axis 0 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_wind_speed_speedstddev_0_stddev IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-ESS04 along axis 0 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_wind_speed_speedstddev_0_min IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-ESS04 along axis 0 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_wind_speed_speedstddev_0_max IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-ESS04 along axis 0 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_wind_speed_speedstddev_1_mean IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-ESS04 along axis 1 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_wind_speed_speedstddev_1_stddev IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-ESS04 along axis 1 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_wind_speed_speedstddev_1_min IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-ESS04 along axis 1 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_wind_speed_speedstddev_1_max IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-ESS04 along axis 1 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_wind_speed_speedstddev_2_mean IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-ESS04 along axis 2 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_wind_speed_speedstddev_2_stddev IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-ESS04 along axis 2 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_wind_speed_speedstddev_2_min IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-ESS04 along axis 2 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_wind_speed_speedstddev_2_max IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-ESS04 along axis 2 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_wind_speed_magnitude_mean IS 'Median wind speed magnitude in AuxTel-ESS04 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_wind_speed_magnitude_stddev IS 'Median wind speed magnitude in AuxTel-ESS04 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_wind_speed_magnitude_min IS 'Median wind speed magnitude in AuxTel-ESS04 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_wind_speed_magnitude_max IS 'Median wind speed magnitude in AuxTel-ESS04 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_wind_speed_maxmagnitude_mean IS 'Maximum wind speed magnitude in AuxTel-ESS04 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_wind_speed_maxmagnitude_stddev IS 'Maximum wind speed magnitude in AuxTel-ESS04 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_wind_speed_maxmagnitude_min IS 'Maximum wind speed magnitude in AuxTel-ESS04 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_wind_speed_maxmagnitude_max IS 'Maximum wind speed magnitude in AuxTel-ESS04 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_wind_speed_0_mean IS 'Median wind speed (x, y, z) along axis 0 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_wind_speed_0_stddev IS 'Median wind speed (x, y, z) along axis 0 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_wind_speed_0_min IS 'Median wind speed (x, y, z) along axis 0 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_wind_speed_0_max IS 'Median wind speed (x, y, z) along axis 0 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_wind_speed_1_mean IS 'Median wind speed (x, y, z) along axis 1 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_wind_speed_1_stddev IS 'Median wind speed (x, y, z) along axis 1 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_wind_speed_1_min IS 'Median wind speed (x, y, z) along axis 1 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_wind_speed_1_max IS 'Median wind speed (x, y, z) along axis 1 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_wind_speed_2_mean IS 'Median wind speed (x, y, z) along axis 2 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_wind_speed_2_stddev IS 'Median wind speed (x, y, z) along axis 2 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_wind_speed_2_min IS 'Median wind speed (x, y, z) along axis 2 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_wind_speed_2_max IS 'Median wind speed (x, y, z) along axis 2 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_wind_speed_speedstddev_0_mean IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles along axis 0 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_wind_speed_speedstddev_0_stddev IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles along axis 0 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_wind_speed_speedstddev_0_min IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles along axis 0 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_wind_speed_speedstddev_0_max IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles along axis 0 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_wind_speed_speedstddev_1_mean IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles along axis 1 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_wind_speed_speedstddev_1_stddev IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles along axis 1 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_wind_speed_speedstddev_1_min IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles along axis 1 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_wind_speed_speedstddev_1_max IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles along axis 1 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_wind_speed_speedstddev_2_mean IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles along axis 2 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_wind_speed_speedstddev_2_stddev IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles along axis 2 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_wind_speed_speedstddev_2_min IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles along axis 2 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_wind_speed_speedstddev_2_max IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles along axis 2 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_wind_speed_magnitude_mean IS 'Median wind speed magnitude (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_wind_speed_magnitude_stddev IS 'Median wind speed magnitude (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_wind_speed_magnitude_min IS 'Median wind speed magnitude (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_wind_speed_magnitude_max IS 'Median wind speed magnitude (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_wind_speed_maxmagnitude_mean IS 'Maximum wind speed magnitude (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_wind_speed_maxmagnitude_stddev IS 'Maximum wind speed magnitude (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_wind_speed_maxmagnitude_min IS 'Maximum wind speed magnitude (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_wind_speed_maxmagnitude_max IS 'Maximum wind speed magnitude (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_wind_speed_0_mean IS 'Median wind speed (x, y, z) in AuxTel-GillLabJack01 along axis 0 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_wind_speed_0_stddev IS 'Median wind speed (x, y, z) in AuxTel-GillLabJack01 along axis 0 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_wind_speed_0_min IS 'Median wind speed (x, y, z) in AuxTel-GillLabJack01 along axis 0 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_wind_speed_0_max IS 'Median wind speed (x, y, z) in AuxTel-GillLabJack01 along axis 0 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_wind_speed_1_mean IS 'Median wind speed (x, y, z) in AuxTel-GillLabJack01 along axis 1 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_wind_speed_1_stddev IS 'Median wind speed (x, y, z) in AuxTel-GillLabJack01 along axis 1 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_wind_speed_1_min IS 'Median wind speed (x, y, z) in AuxTel-GillLabJack01 along axis 1 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_wind_speed_1_max IS 'Median wind speed (x, y, z) in AuxTel-GillLabJack01 along axis 1 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_wind_speed_2_mean IS 'Median wind speed (x, y, z) in AuxTel-GillLabJack01 along axis 2 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_wind_speed_2_stddev IS 'Median wind speed (x, y, z) in AuxTel-GillLabJack01 along axis 2 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_wind_speed_2_min IS 'Median wind speed (x, y, z) in AuxTel-GillLabJack01 along axis 2 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_wind_speed_2_max IS 'Median wind speed (x, y, z) in AuxTel-GillLabJack01 along axis 2 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_wind_speed_speedstddev_0_mean IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-GillLabJack01 along axis 0 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_wind_speed_speedstddev_0_stddev IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-GillLabJack01 along axis 0 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_wind_speed_speedstddev_0_min IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-GillLabJack01 along axis 0 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_wind_speed_speedstddev_0_max IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-GillLabJack01 along axis 0 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_wind_speed_speedstddev_1_mean IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-GillLabJack01 along axis 1 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_wind_speed_speedstddev_1_stddev IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-GillLabJack01 along axis 1 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_wind_speed_speedstddev_1_min IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-GillLabJack01 along axis 1 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_wind_speed_speedstddev_1_max IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-GillLabJack01 along axis 1 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_wind_speed_speedstddev_2_mean IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-GillLabJack01 along axis 2 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_wind_speed_speedstddev_2_stddev IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-GillLabJack01 along axis 2 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_wind_speed_speedstddev_2_min IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-GillLabJack01 along axis 2 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_wind_speed_speedstddev_2_max IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-GillLabJack01 along axis 2 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_wind_speed_magnitude_mean IS 'Median wind speed magnitude in AuxTel-GillLabJack01 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_wind_speed_magnitude_stddev IS 'Median wind speed magnitude in AuxTel-GillLabJack01 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_wind_speed_magnitude_min IS 'Median wind speed magnitude in AuxTel-GillLabJack01 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_wind_speed_magnitude_max IS 'Median wind speed magnitude in AuxTel-GillLabJack01 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_wind_speed_maxmagnitude_mean IS 'Maximum wind speed magnitude in AuxTel-GillLabJack01 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_wind_speed_maxmagnitude_stddev IS 'Maximum wind speed magnitude in AuxTel-GillLabJack01 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_wind_speed_maxmagnitude_min IS 'Maximum wind speed magnitude in AuxTel-GillLabJack01 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_wind_speed_maxmagnitude_max IS 'Maximum wind speed magnitude in AuxTel-GillLabJack01 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_airflow_speed_mean IS 'Median (mean for some sensors) wind speed in [] (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_airflow_speed_stddev IS 'Median (mean for some sensors) wind speed in [] (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_airflow_speed_min IS 'Median (mean for some sensors) wind speed in [] (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_airflow_speed_max IS 'Median (mean for some sensors) wind speed in [] (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_airflow_speedstddev_mean IS 'Standard deviation of wind speed estimated from quartiles in [] (salIndex 201). Not available for all sensor types.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_airflow_speedstddev_stddev IS 'Standard deviation of wind speed estimated from quartiles in [] (salIndex 201). Not available for all sensor types.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_airflow_speedstddev_min IS 'Standard deviation of wind speed estimated from quartiles in [] (salIndex 201). Not available for all sensor types.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_airflow_speedstddev_max IS 'Standard deviation of wind speed estimated from quartiles in [] (salIndex 201). Not available for all sensor types.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_airflow_direction_mean IS 'Median (mean for some sensors) wind speed in [] (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_airflow_direction_stddev IS 'Median (mean for some sensors) wind speed in [] (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_airflow_direction_min IS 'Median (mean for some sensors) wind speed in [] (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_airflow_direction_max IS 'Median (mean for some sensors) wind speed in [] (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_airflow_speed_mean IS 'Median (mean for some sensors) wind speed in AuxTel-Windsonic (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_airflow_speed_stddev IS 'Median (mean for some sensors) wind speed in AuxTel-Windsonic (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_airflow_speed_min IS 'Median (mean for some sensors) wind speed in AuxTel-Windsonic (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_airflow_speed_max IS 'Median (mean for some sensors) wind speed in AuxTel-Windsonic (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_airflow_speedstddev_mean IS 'Standard deviation of wind speed estimated from quartiles in AuxTel-Windsonic (salIndex 204). Not available for all sensor types.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_airflow_speedstddev_stddev IS 'Standard deviation of wind speed estimated from quartiles in AuxTel-Windsonic (salIndex 204). Not available for all sensor types.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_airflow_speedstddev_min IS 'Standard deviation of wind speed estimated from quartiles in AuxTel-Windsonic (salIndex 204). Not available for all sensor types.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_airflow_speedstddev_max IS 'Standard deviation of wind speed estimated from quartiles in AuxTel-Windsonic (salIndex 204). Not available for all sensor types.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_airflow_direction_mean IS 'Median (mean for some sensors) wind speed in AuxTel-Windsonic (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_airflow_direction_stddev IS 'Median (mean for some sensors) wind speed in AuxTel-Windsonic (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_airflow_direction_min IS 'Median (mean for some sensors) wind speed in AuxTel-Windsonic (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex204_airflow_direction_max IS 'Median (mean for some sensors) wind speed in AuxTel-Windsonic (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_airflow_speed_mean IS 'Median (mean for some sensors) wind speed in [] (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_airflow_speed_stddev IS 'Median (mean for some sensors) wind speed in [] (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_airflow_speed_min IS 'Median (mean for some sensors) wind speed in [] (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_airflow_speed_max IS 'Median (mean for some sensors) wind speed in [] (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_airflow_speedstddev_mean IS 'Standard deviation of wind speed estimated from quartiles in [] (salIndex 205). Not available for all sensor types.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_airflow_speedstddev_stddev IS 'Standard deviation of wind speed estimated from quartiles in [] (salIndex 205). Not available for all sensor types.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_airflow_speedstddev_min IS 'Standard deviation of wind speed estimated from quartiles in [] (salIndex 205). Not available for all sensor types.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_airflow_speedstddev_max IS 'Standard deviation of wind speed estimated from quartiles in [] (salIndex 205). Not available for all sensor types.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_airflow_direction_mean IS 'Median (mean for some sensors) wind speed in [] (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_airflow_direction_stddev IS 'Median (mean for some sensors) wind speed in [] (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_airflow_direction_min IS 'Median (mean for some sensors) wind speed in [] (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex205_airflow_direction_max IS 'Median (mean for some sensors) wind speed in [] (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_temperatureitem_0_mean IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 0';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_temperatureitem_0_stddev IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 0';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_temperatureitem_0_min IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 0';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_temperatureitem_0_max IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 0';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_temperatureitem_1_mean IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 1';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_temperatureitem_1_stddev IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 1';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_temperatureitem_1_min IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 1';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_temperatureitem_1_max IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 1';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_temperatureitem_2_mean IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 2';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_temperatureitem_2_stddev IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 2';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_temperatureitem_2_min IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 2';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_temperatureitem_2_max IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 2';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_temperatureitem_3_mean IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 3';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_temperatureitem_3_stddev IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 3';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_temperatureitem_3_min IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 3';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_temperatureitem_3_max IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 3';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_temperatureitem_4_mean IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 4';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_temperatureitem_4_stddev IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 4';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_temperatureitem_4_min IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 4';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_temperatureitem_4_max IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 4';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_temperatureitem_5_mean IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 5';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_temperatureitem_5_stddev IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 5';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_temperatureitem_5_min IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 5';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_temperatureitem_5_max IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 5';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_temperatureitem_6_mean IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 6';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_temperatureitem_6_stddev IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 6';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_temperatureitem_6_min IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 6';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_temperatureitem_6_max IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 6';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_temperatureitem_7_mean IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 7';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_temperatureitem_7_stddev IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 7';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_temperatureitem_7_min IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 7';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_temperatureitem_7_max IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 7';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_temperatureitem_0_mean IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 0';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_temperatureitem_0_stddev IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 0';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_temperatureitem_0_min IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 0';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_temperatureitem_0_max IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 0';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_temperatureitem_1_mean IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 1';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_temperatureitem_1_stddev IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 1';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_temperatureitem_1_min IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 1';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_temperatureitem_1_max IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 1';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_temperatureitem_2_mean IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 2';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_temperatureitem_2_stddev IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 2';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_temperatureitem_2_min IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 2';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_temperatureitem_2_max IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 2';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_temperatureitem_3_mean IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 3';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_temperatureitem_3_stddev IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 3';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_temperatureitem_3_min IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 3';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_temperatureitem_3_max IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 3';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_temperatureitem_4_mean IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 4';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_temperatureitem_4_stddev IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 4';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_temperatureitem_4_min IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 4';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_temperatureitem_4_max IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 4';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_temperatureitem_5_mean IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 5';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_temperatureitem_5_stddev IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 5';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_temperatureitem_5_min IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 5';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_temperatureitem_5_max IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 5';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_temperatureitem_6_mean IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 6';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_temperatureitem_6_stddev IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 6';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_temperatureitem_6_min IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 6';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_temperatureitem_6_max IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 6';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_temperatureitem_7_mean IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 7';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_temperatureitem_7_stddev IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 7';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_temperatureitem_7_min IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 7';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_temperatureitem_7_max IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 7';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_azimuth_calculated_angle IS 'Azimuth axis position computed from the axis encoders at 100 Hz beginning at the specified time. The range is the hard stop limits (L3),  approximately -280 to 280.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_elevation_calculated_angle IS 'Elevation axis position computed from the axis encoders at 100 Hz beginning at the specified time.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_dimm_fwhm_mean IS 'Combined full width half maximum';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_azimuth_mean IS 'Elevation axis position computed from the axis encoders at 100 Hz beginning at the specified time.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_elevation_mean IS 'Azimuth axis position computed from the axis encoders at 100 Hz beginning at the specified time. The range is the hard stop limits (L3), approximately -280 to 280.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_hexapod_reported_position_x_mean IS 'Auxiliary telescope hexapod reported position in x';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_hexapod_reported_position_x_max IS 'Auxiliary telescope hexapod reported position in x';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_hexapod_reported_position_x_min IS 'Auxiliary telescope hexapod reported position in x';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_hexapod_reported_position_y_mean IS 'Auxiliary telescope hexapod reported position in y';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_hexapod_reported_position_y_max IS 'Auxiliary telescope hexapod reported position in y';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_hexapod_reported_position_y_min IS 'Auxiliary telescope hexapod reported position in y';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_hexapod_reported_position_z_mean IS 'Auxiliary telescope hexapod reported position in z';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_hexapod_reported_position_z_max IS 'Auxiliary telescope hexapod reported position in z';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_hexapod_reported_position_z_min IS 'Auxiliary telescope hexapod reported position in z';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_hexapod_reported_position_u_mean IS 'Auxiliary telescope hexapod reported position in u';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_hexapod_reported_position_u_max IS 'Auxiliary telescope hexapod reported position in u';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_hexapod_reported_position_u_min IS 'Auxiliary telescope hexapod reported position in u';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_hexapod_reported_position_v_mean IS 'Auxiliary telescope hexapod reported position in v';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_hexapod_reported_position_v_max IS 'Auxiliary telescope hexapod reported position in v';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_hexapod_reported_position_v_min IS 'Auxiliary telescope hexapod reported position in v';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_hexapod_reported_position_w_mean IS 'Auxiliary telescope hexapod reported position in w';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_hexapod_reported_position_w_max IS 'Auxiliary telescope hexapod reported position in w';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_hexapod_reported_position_w_min IS 'Auxiliary telescope hexapod reported position in w';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex202_acceleration_x_mean IS 'Acceleration in x direction in AccelAuxTel-M2, AuxTel-Truss, AuxTel-M1';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex202_acceleration_x_stddev IS 'Acceleration in x direction in AccelAuxTel-M2, AuxTel-Truss, AuxTel-M1';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex202_acceleration_x_min IS 'Acceleration in x direction in AccelAuxTel-M2, AuxTel-Truss, AuxTel-M1';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex202_acceleration_x_max IS 'Acceleration in x direction in AccelAuxTel-M2, AuxTel-Truss, AuxTel-M1';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindey202_acceleration_y_mean IS 'Acceleration in y direction in AccelAuxTel-M2, AuxTel-Truss, AuxTel-M1';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex202_acceleration_y_stddev IS 'Acceleration in y direction in AccelAuxTel-M2, AuxTel-Truss, AuxTel-M1';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex202_acceleration_y_min IS 'Acceleration in y direction in AccelAuxTel-M2, AuxTel-Truss, AuxTel-M1';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex202_acceleration_y_max IS 'Acceleration in y direction in AccelAuxTel-M2, AuxTel-Truss, AuxTel-M1';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindez202_acceleration_z_mean IS 'Acceleration in z direction in AccelAuxTel-M2, AuxTel-Truss, AuxTel-M1';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex202_acceleration_z_stddev IS 'Acceleration in z direction in AccelAuxTel-M2, AuxTel-Truss, AuxTel-M1';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex202_acceleration_z_min IS 'Acceleration in z direction in AccelAuxTel-M2, AuxTel-Truss, AuxTel-M1';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex202_acceleration_z_max IS 'Acceleration in z direction in AccelAuxTel-M2, AuxTel-Truss, AuxTel-M1';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_dewpoint_mean IS 'Dew point in AuxTel-ESS02';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_relative_humidity_mean IS 'Relative humidity in AuxTel-ESS02';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_pressure_item_0_mean IS 'Atmosferic pressure item 0 in AuxTel-ESS02';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex201_pressure_item_1_mean IS 'Atmosferic pressure item 1 in AuxTel-ESS02';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_pressure_item_0_mean IS 'Atmosferic pressure item 0 in weather tower atmospheric pressure';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_salindex301_pressure_item_1_mean IS 'Atmosferic pressure item 1 in weather tower atmospheric pressure';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_pointing_mount_position_ra_mean IS 'RA calculated from the azimuthCalculatedAngle and elevationCalculatedAngle.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_pointing_mount_position_ra_stddev IS 'RA calculated from the azimuthCalculatedAngle and elevationCalculatedAngle.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_pointing_mount_position_dec_mean IS 'Dec calculated from the azimuthCalculatedAngle and elevationCalculatedAngle.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_pointing_mount_position_dec_stddev IS 'Dec calculated from the azimuthCalculatedAngle and elevationCalculatedAngle.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_pointing_mount_position_sky_angle_mean IS 'Calculated sky angle.';
COMMENT ON COLUMN cdb_latiss.exposure_efd.at_pointing_mount_position_sky_angle_stddev IS 'Calculated sky angle.';
COMMENT ON CONSTRAINT un_exposure_id_instrument ON cdb_latiss.exposure_efd IS 'Ensure exposure_id is unique.';

CREATE TABLE cdb_latiss.visit1_efd (
	visit_id BIGINT,
	created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	instrument CHAR(20),
	at_salindex201_sonic_temperature_mean FLOAT,
	at_salindex201_sonic_temperature_stddev FLOAT,
	at_salindex201_sonic_temperature_stddev_mean FLOAT,
	at_salindex201_sonic_temperature_stddev_stddev FLOAT,
	at_salindex205_sonic_temperature_mean FLOAT,
	at_salindex205_sonic_temperature_stddev FLOAT,
	at_salindex205_sonic_temperature_stddev_mean FLOAT,
	at_salindex205_sonic_temperature_stddev_stddev FLOAT,
	at_salindex201_wind_speed_x_mean FLOAT,
	at_salindex201_wind_speed_0_stddev FLOAT,
	at_salindex201_wind_speed_0_min FLOAT,
	at_salindex201_wind_speed_0_max FLOAT,
	at_salindex201_wind_speed_1_mean FLOAT,
	at_salindex201_wind_speed_1_stddev FLOAT,
	at_salindex201_wind_speed_1_min FLOAT,
	at_salindex201_wind_speed_1_max FLOAT,
	at_salindex201_wind_speed_2_mean FLOAT,
	at_salindex201_wind_speed_2_stddev FLOAT,
	at_salindex201_wind_speed_2_min FLOAT,
	at_salindex201_wind_speed_2_max FLOAT,
	at_salindex201_wind_speed_speedstddev_0_mean FLOAT,
	at_salindex201_wind_speed_speedstddev_0_stddev FLOAT,
	at_salindex201_wind_speed_speedstddev_0_min FLOAT,
	at_salindex201_wind_speed_speedstddev_0_max FLOAT,
	at_salindex201_wind_speed_speedstddev_1_mean FLOAT,
	at_salindex201_wind_speed_speedstddev_1_stddev FLOAT,
	at_salindex201_wind_speed_speedstddev_1_min FLOAT,
	at_salindex201_wind_speed_speedstddev_1_max FLOAT,
	at_salindex201_wind_speed_speedstddev_2_mean FLOAT,
	at_salindex201_wind_speed_speedstddev_2_stddev FLOAT,
	at_salindex201_wind_speed_speedstddev_2_min FLOAT,
	at_salindex201_wind_speed_speedstddev_2_max FLOAT,
	at_salindex201_wind_speed_magnitude_mean FLOAT,
	at_salindex201_wind_speed_magnitude_stddev FLOAT,
	at_salindex201_wind_speed_magnitude_min FLOAT,
	at_salindex201_wind_speed_magnitude_max FLOAT,
	at_salindex201_wind_speed_maxmagnitude_mean FLOAT,
	at_salindex201_wind_speed_maxmagnitude_stddev FLOAT,
	at_salindex201_wind_speed_maxmagnitude_min FLOAT,
	at_salindex201_wind_speed_maxmagnitude_max FLOAT,
	at_salindex204_wind_speed_0_mean FLOAT,
	at_salindex204_wind_speed_0_stddev FLOAT,
	at_salindex204_wind_speed_0_min FLOAT,
	at_salindex204_wind_speed_0_max FLOAT,
	at_salindex204_wind_speed_1_mean FLOAT,
	at_salindex204_wind_speed_1_stddev FLOAT,
	at_salindex204_wind_speed_1_min FLOAT,
	at_salindex204_wind_speed_1_max FLOAT,
	at_salindex204_wind_speed_2_mean FLOAT,
	at_salindex204_wind_speed_2_stddev FLOAT,
	at_salindex204_wind_speed_2_min FLOAT,
	at_salindex204_wind_speed_2_max FLOAT,
	at_salindex204_wind_speed_speedstddev_0_mean FLOAT,
	at_salindex204_wind_speed_speedstddev_0_stddev FLOAT,
	at_salindex204_wind_speed_speedstddev_0_min FLOAT,
	at_salindex204_wind_speed_speedstddev_0_max FLOAT,
	at_salindex204_wind_speed_speedstddev_1_mean FLOAT,
	at_salindex204_wind_speed_speedstddev_1_stddev FLOAT,
	at_salindex204_wind_speed_speedstddev_1_min FLOAT,
	at_salindex204_wind_speed_speedstddev_1_max FLOAT,
	at_salindex204_wind_speed_speedstddev_2_mean FLOAT,
	at_salindex204_wind_speed_speedstddev_2_stddev FLOAT,
	at_salindex204_wind_speed_speedstddev_2_min FLOAT,
	at_salindex204_wind_speed_speedstddev_2_max FLOAT,
	at_salindex204_wind_speed_magnitude_mean FLOAT,
	at_salindex204_wind_speed_magnitude_stddev FLOAT,
	at_salindex204_wind_speed_magnitude_min FLOAT,
	at_salindex204_wind_speed_magnitude_max FLOAT,
	at_salindex204_wind_speed_maxmagnitude_mean FLOAT,
	at_salindex204_wind_speed_maxmagnitude_stddev FLOAT,
	at_salindex204_wind_speed_maxmagnitude_min FLOAT,
	at_salindex204_wind_speed_maxmagnitude_max FLOAT,
	at_salindex205_wind_speed_0_mean FLOAT,
	at_salindex205_wind_speed_0_stddev FLOAT,
	at_salindex205_wind_speed_0_min FLOAT,
	at_salindex205_wind_speed_0_max FLOAT,
	at_salindex205_wind_speed_1_mean FLOAT,
	at_salindex205_wind_speed_1_stddev FLOAT,
	at_salindex205_wind_speed_1_min FLOAT,
	at_salindex205_wind_speed_1_max FLOAT,
	at_salindex205_wind_speed_2_mean FLOAT,
	at_salindex205_wind_speed_2_stddev FLOAT,
	at_salindex205_wind_speed_2_min FLOAT,
	at_salindex205_wind_speed_2_max FLOAT,
	at_salindex205_wind_speed_speedstddev_0_mean FLOAT,
	at_salindex205_wind_speed_speedstddev_0_stddev FLOAT,
	at_salindex205_wind_speed_speedstddev_0_min FLOAT,
	at_salindex205_wind_speed_speedstddev_0_max FLOAT,
	at_salindex205_wind_speed_speedstddev_1_mean FLOAT,
	at_salindex205_wind_speed_speedstddev_1_stddev FLOAT,
	at_salindex205_wind_speed_speedstddev_1_min FLOAT,
	at_salindex205_wind_speed_speedstddev_1_max FLOAT,
	at_salindex205_wind_speed_speedstddev_2_mean FLOAT,
	at_salindex205_wind_speed_speedstddev_2_stddev FLOAT,
	at_salindex205_wind_speed_speedstddev_2_min FLOAT,
	at_salindex205_wind_speed_speedstddev_2_max FLOAT,
	at_salindex205_wind_speed_magnitude_mean FLOAT,
	at_salindex205_wind_speed_magnitude_stddev FLOAT,
	at_salindex205_wind_speed_magnitude_min FLOAT,
	at_salindex205_wind_speed_magnitude_max FLOAT,
	at_salindex205_wind_speed_maxmagnitude_mean FLOAT,
	at_salindex205_wind_speed_maxmagnitude_stddev FLOAT,
	at_salindex205_wind_speed_maxmagnitude_min FLOAT,
	at_salindex205_wind_speed_maxmagnitude_max FLOAT,
	at_salindex201_airflow_speed_mean FLOAT,
	at_salindex201_airflow_speed_stddev FLOAT,
	at_salindex201_airflow_speed_min FLOAT,
	at_salindex201_airflow_speed_max FLOAT,
	at_salindex201_airflow_speedstddev_mean FLOAT,
	at_salindex201_airflow_speedstddev_stddev FLOAT,
	at_salindex201_airflow_speedstddev_min FLOAT,
	at_salindex201_airflow_speedstddev_max FLOAT,
	at_salindex201_airflow_direction_mean FLOAT,
	at_salindex201_airflow_direction_stddev FLOAT,
	at_salindex201_airflow_direction_min FLOAT,
	at_salindex201_airflow_direction_max FLOAT,
	at_salindex204_airflow_speed_mean FLOAT,
	at_salindex204_airflow_speed_stddev FLOAT,
	at_salindex204_airflow_speed_min FLOAT,
	at_salindex204_airflow_speed_max FLOAT,
	at_salindex204_airflow_speedstddev_mean FLOAT,
	at_salindex204_airflow_speedstddev_stddev FLOAT,
	at_salindex204_airflow_speedstddev_min FLOAT,
	at_salindex204_airflow_speedstddev_max FLOAT,
	at_salindex204_airflow_direction_mean FLOAT,
	at_salindex204_airflow_direction_stddev FLOAT,
	at_salindex204_airflow_direction_min FLOAT,
	at_salindex204_airflow_direction_max FLOAT,
	at_salindex205_airflow_speed_mean FLOAT,
	at_salindex205_airflow_speed_stddev FLOAT,
	at_salindex205_airflow_speed_min FLOAT,
	at_salindex205_airflow_speed_max FLOAT,
	at_salindex205_airflow_speedstddev_mean FLOAT,
	at_salindex205_airflow_speedstddev_stddev FLOAT,
	at_salindex205_airflow_speedstddev_min FLOAT,
	at_salindex205_airflow_speedstddev_max FLOAT,
	at_salindex205_airflow_direction_mean FLOAT,
	at_salindex205_airflow_direction_stddev FLOAT,
	at_salindex205_airflow_direction_min FLOAT,
	at_salindex205_airflow_direction_max FLOAT,
	at_salindex201_temperatureitem_0_mean FLOAT,
	at_salindex201_temperatureitem_0_stddev FLOAT,
	at_salindex201_temperatureitem_0_min FLOAT,
	at_salindex201_temperatureitem_0_max FLOAT,
	at_salindex201_temperatureitem_1_mean FLOAT,
	at_salindex201_temperatureitem_1_stddev FLOAT,
	at_salindex201_temperatureitem_1_min FLOAT,
	at_salindex201_temperatureitem_1_max FLOAT,
	at_salindex201_temperatureitem_2_mean FLOAT,
	at_salindex201_temperatureitem_2_stddev FLOAT,
	at_salindex201_temperatureitem_2_min FLOAT,
	at_salindex201_temperatureitem_2_max FLOAT,
	at_salindex201_temperatureitem_3_mean FLOAT,
	at_salindex201_temperatureitem_3_stddev FLOAT,
	at_salindex201_temperatureitem_3_min FLOAT,
	at_salindex201_temperatureitem_3_max FLOAT,
	at_salindex201_temperatureitem_4_mean FLOAT,
	at_salindex201_temperatureitem_4_stddev FLOAT,
	at_salindex201_temperatureitem_4_min FLOAT,
	at_salindex201_temperatureitem_4_max FLOAT,
	at_salindex201_temperatureitem_5_mean FLOAT,
	at_salindex201_temperatureitem_5_stddev FLOAT,
	at_salindex201_temperatureitem_5_min FLOAT,
	at_salindex201_temperatureitem_5_max FLOAT,
	at_salindex201_temperatureitem_6_mean FLOAT,
	at_salindex201_temperatureitem_6_stddev FLOAT,
	at_salindex201_temperatureitem_6_min FLOAT,
	at_salindex201_temperatureitem_6_max FLOAT,
	at_salindex201_temperatureitem_7_mean FLOAT,
	at_salindex201_temperatureitem_7_stddev FLOAT,
	at_salindex201_temperatureitem_7_min FLOAT,
	at_salindex201_temperatureitem_7_max FLOAT,
	at_salindex301_temperatureitem_0_mean FLOAT,
	at_salindex301_temperatureitem_0_stddev FLOAT,
	at_salindex301_temperatureitem_0_min FLOAT,
	at_salindex301_temperatureitem_0_max FLOAT,
	at_salindex301_temperatureitem_1_mean FLOAT,
	at_salindex301_temperatureitem_1_stddev FLOAT,
	at_salindex301_temperatureitem_1_min FLOAT,
	at_salindex301_temperatureitem_1_max FLOAT,
	at_salindex301_temperatureitem_2_mean FLOAT,
	at_salindex301_temperatureitem_2_stddev FLOAT,
	at_salindex301_temperatureitem_2_min FLOAT,
	at_salindex301_temperatureitem_2_max FLOAT,
	at_salindex301_temperatureitem_3_mean FLOAT,
	at_salindex301_temperatureitem_3_stddev FLOAT,
	at_salindex301_temperatureitem_3_min FLOAT,
	at_salindex301_temperatureitem_3_max FLOAT,
	at_salindex301_temperatureitem_4_mean FLOAT,
	at_salindex301_temperatureitem_4_stddev FLOAT,
	at_salindex301_temperatureitem_4_min FLOAT,
	at_salindex301_temperatureitem_4_max FLOAT,
	at_salindex301_temperatureitem_5_mean FLOAT,
	at_salindex301_temperatureitem_5_stddev FLOAT,
	at_salindex301_temperatureitem_5_min FLOAT,
	at_salindex301_temperatureitem_5_max FLOAT,
	at_salindex301_temperatureitem_6_mean FLOAT,
	at_salindex301_temperatureitem_6_stddev FLOAT,
	at_salindex301_temperatureitem_6_min FLOAT,
	at_salindex301_temperatureitem_6_max FLOAT,
	at_salindex301_temperatureitem_7_mean FLOAT,
	at_salindex301_temperatureitem_7_stddev FLOAT,
	at_salindex301_temperatureitem_7_min FLOAT,
	at_salindex301_temperatureitem_7_max FLOAT,
	at_azimuth_calculated_angle FLOAT,
	at_elevation_calculated_angle FLOAT,
	at_dimm_fwhm_mean FLOAT,
	at_azimuth_mean FLOAT,
	at_elevation_mean FLOAT,
	at_hexapod_reported_position_x_mean FLOAT,
	at_hexapod_reported_position_x_max FLOAT,
	at_hexapod_reported_position_x_min FLOAT,
	at_hexapod_reported_position_y_mean FLOAT,
	at_hexapod_reported_position_y_max FLOAT,
	at_hexapod_reported_position_y_min FLOAT,
	at_hexapod_reported_position_z_mean FLOAT,
	at_hexapod_reported_position_z_max FLOAT,
	at_hexapod_reported_position_z_min FLOAT,
	at_hexapod_reported_position_u_mean FLOAT,
	at_hexapod_reported_position_u_max FLOAT,
	at_hexapod_reported_position_u_min FLOAT,
	at_hexapod_reported_position_v_mean FLOAT,
	at_hexapod_reported_position_v_max FLOAT,
	at_hexapod_reported_position_v_min FLOAT,
	at_hexapod_reported_position_w_mean FLOAT,
	at_hexapod_reported_position_w_max FLOAT,
	at_hexapod_reported_position_w_min FLOAT,
	at_salindex202_acceleration_x_mean FLOAT,
	at_salindex202_acceleration_x_stddev FLOAT,
	at_salindex202_acceleration_x_min FLOAT,
	at_salindex202_acceleration_x_max FLOAT,
	at_salindey202_acceleration_y_mean FLOAT,
	at_salindex202_acceleration_y_stddev FLOAT,
	at_salindex202_acceleration_y_min FLOAT,
	at_salindex202_acceleration_y_max FLOAT,
	at_salindez202_acceleration_z_mean FLOAT,
	at_salindex202_acceleration_z_stddev FLOAT,
	at_salindex202_acceleration_z_min FLOAT,
	at_salindex202_acceleration_z_max FLOAT,
	at_salindex201_dewpoint_mean FLOAT,
	at_salindex201_relative_humidity_mean FLOAT,
	at_salindex201_pressure_item_0_mean FLOAT,
	at_salindex201_pressure_item_1_mean FLOAT,
	at_salindex301_pressure_item_0_mean FLOAT,
	at_salindex301_pressure_item_1_mean FLOAT,
	at_pointing_mount_position_ra_mean FLOAT,
	at_pointing_mount_position_ra_stddev FLOAT,
	at_pointing_mount_position_dec_mean FLOAT,
	at_pointing_mount_position_dec_stddev FLOAT,
	at_pointing_mount_position_sky_angle_mean FLOAT,
	at_pointing_mount_position_sky_angle_stddev FLOAT,
	PRIMARY KEY (visit_id, instrument),
	CONSTRAINT un_visit_id_instrument UNIQUE (visit_id, instrument)
)

;
COMMENT ON TABLE cdb_latiss.visit1_efd IS 'Transformed EFD topics by visit.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.visit_id IS 'Visit unique ID.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.created_at IS 'Timestamp when the record was created, default is the current timestamp';
COMMENT ON COLUMN cdb_latiss.visit1_efd.instrument IS 'Instrument name.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_sonic_temperature_mean IS 'Median sonic temperature (air temperature measured sonically). Sonic temperature has poor absolute accuracy (it can be off by several degrees) but good time resolution.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_sonic_temperature_stddev IS 'Median sonic temperature (air temperature measured sonically). Sonic temperature has poor absolute accuracy (it can be off by several degrees) but good time resolution.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_sonic_temperature_stddev_mean IS 'Standard devation of sonic temperature (air temperature measured sonically) estimated from quartiles.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_sonic_temperature_stddev_stddev IS 'Standard devation of sonic temperature (air temperature measured sonically) estimated from quartiles.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_sonic_temperature_mean IS 'Median sonic temperature (air temperature measured sonically). Sonic temperature has poor absolute accuracy (it can be off by several degrees) but good time resolution.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_sonic_temperature_stddev IS 'Median sonic temperature (air temperature measured sonically). Sonic temperature has poor absolute accuracy (it can be off by several degrees) but good time resolution.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_sonic_temperature_stddev_mean IS 'Standard devation of sonic temperature (air temperature measured sonically) estimated from quartiles.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_sonic_temperature_stddev_stddev IS 'Standard devation of sonic temperature (air temperature measured sonically) estimated from quartiles.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_wind_speed_x_mean IS 'Median wind speed (x, y, z) in AuxTel-ESS04 along axis 0 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_wind_speed_0_stddev IS 'Median wind speed (x, y, z) in AuxTel-ESS04 along axis 0 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_wind_speed_0_min IS 'Median wind speed (x, y, z) in AuxTel-ESS04 along axis 0 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_wind_speed_0_max IS 'Median wind speed (x, y, z) in AuxTel-ESS04 along axis 0 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_wind_speed_1_mean IS 'Median wind speed (x, y, z) in AuxTel-ESS04 along axis 1 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_wind_speed_1_stddev IS 'Median wind speed (x, y, z) in AuxTel-ESS04 along axis 1 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_wind_speed_1_min IS 'Median wind speed (x, y, z) in AuxTel-ESS04 along axis 1 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_wind_speed_1_max IS 'Median wind speed (x, y, z) in AuxTel-ESS04 along axis 1 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_wind_speed_2_mean IS 'Median wind speed (x, y, z) in AuxTel-ESS04 along axis 2 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_wind_speed_2_stddev IS 'Median wind speed (x, y, z) in AuxTel-ESS04 along axis 2 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_wind_speed_2_min IS 'Median wind speed (x, y, z) in AuxTel-ESS04 along axis 2 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_wind_speed_2_max IS 'Median wind speed (x, y, z) in AuxTel-ESS04 along axis 2 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_wind_speed_speedstddev_0_mean IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-ESS04 along axis 0 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_wind_speed_speedstddev_0_stddev IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-ESS04 along axis 0 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_wind_speed_speedstddev_0_min IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-ESS04 along axis 0 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_wind_speed_speedstddev_0_max IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-ESS04 along axis 0 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_wind_speed_speedstddev_1_mean IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-ESS04 along axis 1 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_wind_speed_speedstddev_1_stddev IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-ESS04 along axis 1 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_wind_speed_speedstddev_1_min IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-ESS04 along axis 1 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_wind_speed_speedstddev_1_max IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-ESS04 along axis 1 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_wind_speed_speedstddev_2_mean IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-ESS04 along axis 2 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_wind_speed_speedstddev_2_stddev IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-ESS04 along axis 2 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_wind_speed_speedstddev_2_min IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-ESS04 along axis 2 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_wind_speed_speedstddev_2_max IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-ESS04 along axis 2 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_wind_speed_magnitude_mean IS 'Median wind speed magnitude in AuxTel-ESS04 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_wind_speed_magnitude_stddev IS 'Median wind speed magnitude in AuxTel-ESS04 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_wind_speed_magnitude_min IS 'Median wind speed magnitude in AuxTel-ESS04 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_wind_speed_magnitude_max IS 'Median wind speed magnitude in AuxTel-ESS04 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_wind_speed_maxmagnitude_mean IS 'Maximum wind speed magnitude in AuxTel-ESS04 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_wind_speed_maxmagnitude_stddev IS 'Maximum wind speed magnitude in AuxTel-ESS04 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_wind_speed_maxmagnitude_min IS 'Maximum wind speed magnitude in AuxTel-ESS04 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_wind_speed_maxmagnitude_max IS 'Maximum wind speed magnitude in AuxTel-ESS04 (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_wind_speed_0_mean IS 'Median wind speed (x, y, z) along axis 0 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_wind_speed_0_stddev IS 'Median wind speed (x, y, z) along axis 0 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_wind_speed_0_min IS 'Median wind speed (x, y, z) along axis 0 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_wind_speed_0_max IS 'Median wind speed (x, y, z) along axis 0 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_wind_speed_1_mean IS 'Median wind speed (x, y, z) along axis 1 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_wind_speed_1_stddev IS 'Median wind speed (x, y, z) along axis 1 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_wind_speed_1_min IS 'Median wind speed (x, y, z) along axis 1 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_wind_speed_1_max IS 'Median wind speed (x, y, z) along axis 1 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_wind_speed_2_mean IS 'Median wind speed (x, y, z) along axis 2 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_wind_speed_2_stddev IS 'Median wind speed (x, y, z) along axis 2 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_wind_speed_2_min IS 'Median wind speed (x, y, z) along axis 2 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_wind_speed_2_max IS 'Median wind speed (x, y, z) along axis 2 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_wind_speed_speedstddev_0_mean IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles along axis 0 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_wind_speed_speedstddev_0_stddev IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles along axis 0 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_wind_speed_speedstddev_0_min IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles along axis 0 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_wind_speed_speedstddev_0_max IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles along axis 0 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_wind_speed_speedstddev_1_mean IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles along axis 1 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_wind_speed_speedstddev_1_stddev IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles along axis 1 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_wind_speed_speedstddev_1_min IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles along axis 1 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_wind_speed_speedstddev_1_max IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles along axis 1 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_wind_speed_speedstddev_2_mean IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles along axis 2 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_wind_speed_speedstddev_2_stddev IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles along axis 2 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_wind_speed_speedstddev_2_min IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles along axis 2 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_wind_speed_speedstddev_2_max IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles along axis 2 (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_wind_speed_magnitude_mean IS 'Median wind speed magnitude (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_wind_speed_magnitude_stddev IS 'Median wind speed magnitude (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_wind_speed_magnitude_min IS 'Median wind speed magnitude (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_wind_speed_magnitude_max IS 'Median wind speed magnitude (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_wind_speed_maxmagnitude_mean IS 'Maximum wind speed magnitude (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_wind_speed_maxmagnitude_stddev IS 'Maximum wind speed magnitude (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_wind_speed_maxmagnitude_min IS 'Maximum wind speed magnitude (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_wind_speed_maxmagnitude_max IS 'Maximum wind speed magnitude (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_wind_speed_0_mean IS 'Median wind speed (x, y, z) in AuxTel-GillLabJack01 along axis 0 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_wind_speed_0_stddev IS 'Median wind speed (x, y, z) in AuxTel-GillLabJack01 along axis 0 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_wind_speed_0_min IS 'Median wind speed (x, y, z) in AuxTel-GillLabJack01 along axis 0 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_wind_speed_0_max IS 'Median wind speed (x, y, z) in AuxTel-GillLabJack01 along axis 0 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_wind_speed_1_mean IS 'Median wind speed (x, y, z) in AuxTel-GillLabJack01 along axis 1 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_wind_speed_1_stddev IS 'Median wind speed (x, y, z) in AuxTel-GillLabJack01 along axis 1 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_wind_speed_1_min IS 'Median wind speed (x, y, z) in AuxTel-GillLabJack01 along axis 1 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_wind_speed_1_max IS 'Median wind speed (x, y, z) in AuxTel-GillLabJack01 along axis 1 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_wind_speed_2_mean IS 'Median wind speed (x, y, z) in AuxTel-GillLabJack01 along axis 2 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_wind_speed_2_stddev IS 'Median wind speed (x, y, z) in AuxTel-GillLabJack01 along axis 2 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_wind_speed_2_min IS 'Median wind speed (x, y, z) in AuxTel-GillLabJack01 along axis 2 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_wind_speed_2_max IS 'Median wind speed (x, y, z) in AuxTel-GillLabJack01 along axis 2 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_wind_speed_speedstddev_0_mean IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-GillLabJack01 along axis 0 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_wind_speed_speedstddev_0_stddev IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-GillLabJack01 along axis 0 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_wind_speed_speedstddev_0_min IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-GillLabJack01 along axis 0 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_wind_speed_speedstddev_0_max IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-GillLabJack01 along axis 0 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_wind_speed_speedstddev_1_mean IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-GillLabJack01 along axis 1 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_wind_speed_speedstddev_1_stddev IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-GillLabJack01 along axis 1 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_wind_speed_speedstddev_1_min IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-GillLabJack01 along axis 1 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_wind_speed_speedstddev_1_max IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-GillLabJack01 along axis 1 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_wind_speed_speedstddev_2_mean IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-GillLabJack01 along axis 2 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_wind_speed_speedstddev_2_stddev IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-GillLabJack01 along axis 2 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_wind_speed_speedstddev_2_min IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-GillLabJack01 along axis 2 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_wind_speed_speedstddev_2_max IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in AuxTel-GillLabJack01 along axis 2 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_wind_speed_magnitude_mean IS 'Median wind speed magnitude in AuxTel-GillLabJack01 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_wind_speed_magnitude_stddev IS 'Median wind speed magnitude in AuxTel-GillLabJack01 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_wind_speed_magnitude_min IS 'Median wind speed magnitude in AuxTel-GillLabJack01 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_wind_speed_magnitude_max IS 'Median wind speed magnitude in AuxTel-GillLabJack01 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_wind_speed_maxmagnitude_mean IS 'Maximum wind speed magnitude in AuxTel-GillLabJack01 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_wind_speed_maxmagnitude_stddev IS 'Maximum wind speed magnitude in AuxTel-GillLabJack01 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_wind_speed_maxmagnitude_min IS 'Maximum wind speed magnitude in AuxTel-GillLabJack01 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_wind_speed_maxmagnitude_max IS 'Maximum wind speed magnitude in AuxTel-GillLabJack01 (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_airflow_speed_mean IS 'Median (mean for some sensors) wind speed in [] (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_airflow_speed_stddev IS 'Median (mean for some sensors) wind speed in [] (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_airflow_speed_min IS 'Median (mean for some sensors) wind speed in [] (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_airflow_speed_max IS 'Median (mean for some sensors) wind speed in [] (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_airflow_speedstddev_mean IS 'Standard deviation of wind speed estimated from quartiles in [] (salIndex 201). Not available for all sensor types.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_airflow_speedstddev_stddev IS 'Standard deviation of wind speed estimated from quartiles in [] (salIndex 201). Not available for all sensor types.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_airflow_speedstddev_min IS 'Standard deviation of wind speed estimated from quartiles in [] (salIndex 201). Not available for all sensor types.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_airflow_speedstddev_max IS 'Standard deviation of wind speed estimated from quartiles in [] (salIndex 201). Not available for all sensor types.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_airflow_direction_mean IS 'Median (mean for some sensors) wind speed in [] (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_airflow_direction_stddev IS 'Median (mean for some sensors) wind speed in [] (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_airflow_direction_min IS 'Median (mean for some sensors) wind speed in [] (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_airflow_direction_max IS 'Median (mean for some sensors) wind speed in [] (salIndex 201)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_airflow_speed_mean IS 'Median (mean for some sensors) wind speed in AuxTel-Windsonic (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_airflow_speed_stddev IS 'Median (mean for some sensors) wind speed in AuxTel-Windsonic (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_airflow_speed_min IS 'Median (mean for some sensors) wind speed in AuxTel-Windsonic (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_airflow_speed_max IS 'Median (mean for some sensors) wind speed in AuxTel-Windsonic (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_airflow_speedstddev_mean IS 'Standard deviation of wind speed estimated from quartiles in AuxTel-Windsonic (salIndex 204). Not available for all sensor types.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_airflow_speedstddev_stddev IS 'Standard deviation of wind speed estimated from quartiles in AuxTel-Windsonic (salIndex 204). Not available for all sensor types.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_airflow_speedstddev_min IS 'Standard deviation of wind speed estimated from quartiles in AuxTel-Windsonic (salIndex 204). Not available for all sensor types.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_airflow_speedstddev_max IS 'Standard deviation of wind speed estimated from quartiles in AuxTel-Windsonic (salIndex 204). Not available for all sensor types.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_airflow_direction_mean IS 'Median (mean for some sensors) wind speed in AuxTel-Windsonic (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_airflow_direction_stddev IS 'Median (mean for some sensors) wind speed in AuxTel-Windsonic (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_airflow_direction_min IS 'Median (mean for some sensors) wind speed in AuxTel-Windsonic (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex204_airflow_direction_max IS 'Median (mean for some sensors) wind speed in AuxTel-Windsonic (salIndex 204)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_airflow_speed_mean IS 'Median (mean for some sensors) wind speed in [] (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_airflow_speed_stddev IS 'Median (mean for some sensors) wind speed in [] (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_airflow_speed_min IS 'Median (mean for some sensors) wind speed in [] (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_airflow_speed_max IS 'Median (mean for some sensors) wind speed in [] (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_airflow_speedstddev_mean IS 'Standard deviation of wind speed estimated from quartiles in [] (salIndex 205). Not available for all sensor types.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_airflow_speedstddev_stddev IS 'Standard deviation of wind speed estimated from quartiles in [] (salIndex 205). Not available for all sensor types.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_airflow_speedstddev_min IS 'Standard deviation of wind speed estimated from quartiles in [] (salIndex 205). Not available for all sensor types.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_airflow_speedstddev_max IS 'Standard deviation of wind speed estimated from quartiles in [] (salIndex 205). Not available for all sensor types.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_airflow_direction_mean IS 'Median (mean for some sensors) wind speed in [] (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_airflow_direction_stddev IS 'Median (mean for some sensors) wind speed in [] (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_airflow_direction_min IS 'Median (mean for some sensors) wind speed in [] (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex205_airflow_direction_max IS 'Median (mean for some sensors) wind speed in [] (salIndex 205)';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_temperatureitem_0_mean IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 0';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_temperatureitem_0_stddev IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 0';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_temperatureitem_0_min IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 0';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_temperatureitem_0_max IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 0';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_temperatureitem_1_mean IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 1';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_temperatureitem_1_stddev IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 1';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_temperatureitem_1_min IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 1';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_temperatureitem_1_max IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 1';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_temperatureitem_2_mean IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 2';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_temperatureitem_2_stddev IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 2';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_temperatureitem_2_min IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 2';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_temperatureitem_2_max IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 2';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_temperatureitem_3_mean IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 3';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_temperatureitem_3_stddev IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 3';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_temperatureitem_3_min IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 3';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_temperatureitem_3_max IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 3';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_temperatureitem_4_mean IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 4';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_temperatureitem_4_stddev IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 4';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_temperatureitem_4_min IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 4';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_temperatureitem_4_max IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 4';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_temperatureitem_5_mean IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 5';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_temperatureitem_5_stddev IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 5';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_temperatureitem_5_min IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 5';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_temperatureitem_5_max IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 5';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_temperatureitem_6_mean IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 6';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_temperatureitem_6_stddev IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 6';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_temperatureitem_6_min IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 6';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_temperatureitem_6_max IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 6';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_temperatureitem_7_mean IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 7';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_temperatureitem_7_stddev IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 7';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_temperatureitem_7_min IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 7';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_temperatureitem_7_max IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 7';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_temperatureitem_0_mean IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 0';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_temperatureitem_0_stddev IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 0';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_temperatureitem_0_min IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 0';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_temperatureitem_0_max IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 0';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_temperatureitem_1_mean IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 1';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_temperatureitem_1_stddev IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 1';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_temperatureitem_1_min IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 1';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_temperatureitem_1_max IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 1';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_temperatureitem_2_mean IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 2';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_temperatureitem_2_stddev IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 2';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_temperatureitem_2_min IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 2';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_temperatureitem_2_max IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 2';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_temperatureitem_3_mean IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 3';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_temperatureitem_3_stddev IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 3';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_temperatureitem_3_min IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 3';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_temperatureitem_3_max IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 3';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_temperatureitem_4_mean IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 4';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_temperatureitem_4_stddev IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 4';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_temperatureitem_4_min IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 4';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_temperatureitem_4_max IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 4';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_temperatureitem_5_mean IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 5';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_temperatureitem_5_stddev IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 5';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_temperatureitem_5_min IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 5';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_temperatureitem_5_max IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 5';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_temperatureitem_6_mean IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 6';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_temperatureitem_6_stddev IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 6';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_temperatureitem_6_min IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 6';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_temperatureitem_6_max IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 6';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_temperatureitem_7_mean IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 7';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_temperatureitem_7_stddev IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 7';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_temperatureitem_7_min IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 7';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_temperatureitem_7_max IS 'AuxTel-ESS01, AuxTel-ESS02, AuxTel-ESS03 temperature item 7';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_azimuth_calculated_angle IS 'Azimuth axis position computed from the axis encoders at 100 Hz beginning at the specified time. The range is the hard stop limits (L3),  approximately -280 to 280.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_elevation_calculated_angle IS 'Elevation axis position computed from the axis encoders at 100 Hz beginning at the specified time.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_dimm_fwhm_mean IS 'Combined full width half maximum';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_azimuth_mean IS 'Elevation axis position computed from the axis encoders at 100 Hz beginning at the specified time.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_elevation_mean IS 'Azimuth axis position computed from the axis encoders at 100 Hz beginning at the specified time. The range is the hard stop limits (L3), approximately -280 to 280.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_hexapod_reported_position_x_mean IS 'Auxiliary telescope hexapod reported position in x';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_hexapod_reported_position_x_max IS 'Auxiliary telescope hexapod reported position in x';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_hexapod_reported_position_x_min IS 'Auxiliary telescope hexapod reported position in x';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_hexapod_reported_position_y_mean IS 'Auxiliary telescope hexapod reported position in y';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_hexapod_reported_position_y_max IS 'Auxiliary telescope hexapod reported position in y';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_hexapod_reported_position_y_min IS 'Auxiliary telescope hexapod reported position in y';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_hexapod_reported_position_z_mean IS 'Auxiliary telescope hexapod reported position in z';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_hexapod_reported_position_z_max IS 'Auxiliary telescope hexapod reported position in z';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_hexapod_reported_position_z_min IS 'Auxiliary telescope hexapod reported position in z';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_hexapod_reported_position_u_mean IS 'Auxiliary telescope hexapod reported position in u';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_hexapod_reported_position_u_max IS 'Auxiliary telescope hexapod reported position in u';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_hexapod_reported_position_u_min IS 'Auxiliary telescope hexapod reported position in u';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_hexapod_reported_position_v_mean IS 'Auxiliary telescope hexapod reported position in v';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_hexapod_reported_position_v_max IS 'Auxiliary telescope hexapod reported position in v';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_hexapod_reported_position_v_min IS 'Auxiliary telescope hexapod reported position in v';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_hexapod_reported_position_w_mean IS 'Auxiliary telescope hexapod reported position in w';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_hexapod_reported_position_w_max IS 'Auxiliary telescope hexapod reported position in w';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_hexapod_reported_position_w_min IS 'Auxiliary telescope hexapod reported position in w';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex202_acceleration_x_mean IS 'Acceleration in x direction in AccelAuxTel-M2, AuxTel-Truss, AuxTel-M1';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex202_acceleration_x_stddev IS 'Acceleration in x direction in AccelAuxTel-M2, AuxTel-Truss, AuxTel-M1';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex202_acceleration_x_min IS 'Acceleration in x direction in AccelAuxTel-M2, AuxTel-Truss, AuxTel-M1';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex202_acceleration_x_max IS 'Acceleration in x direction in AccelAuxTel-M2, AuxTel-Truss, AuxTel-M1';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindey202_acceleration_y_mean IS 'Acceleration in y direction in AccelAuxTel-M2, AuxTel-Truss, AuxTel-M1';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex202_acceleration_y_stddev IS 'Acceleration in y direction in AccelAuxTel-M2, AuxTel-Truss, AuxTel-M1';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex202_acceleration_y_min IS 'Acceleration in y direction in AccelAuxTel-M2, AuxTel-Truss, AuxTel-M1';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex202_acceleration_y_max IS 'Acceleration in y direction in AccelAuxTel-M2, AuxTel-Truss, AuxTel-M1';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindez202_acceleration_z_mean IS 'Acceleration in z direction in AccelAuxTel-M2, AuxTel-Truss, AuxTel-M1';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex202_acceleration_z_stddev IS 'Acceleration in z direction in AccelAuxTel-M2, AuxTel-Truss, AuxTel-M1';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex202_acceleration_z_min IS 'Acceleration in z direction in AccelAuxTel-M2, AuxTel-Truss, AuxTel-M1';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex202_acceleration_z_max IS 'Acceleration in z direction in AccelAuxTel-M2, AuxTel-Truss, AuxTel-M1';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_dewpoint_mean IS 'Dew point in AuxTel-ESS02';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_relative_humidity_mean IS 'Relative humidity in AuxTel-ESS02';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_pressure_item_0_mean IS 'Atmosferic pressure item 0 in AuxTel-ESS02';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex201_pressure_item_1_mean IS 'Atmosferic pressure item 1 in AuxTel-ESS02';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_pressure_item_0_mean IS 'Atmosferic pressure item 0 in weather tower atmospheric pressure';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_salindex301_pressure_item_1_mean IS 'Atmosferic pressure item 1 in weather tower atmospheric pressure';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_pointing_mount_position_ra_mean IS 'RA calculated from the azimuthCalculatedAngle and elevationCalculatedAngle.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_pointing_mount_position_ra_stddev IS 'RA calculated from the azimuthCalculatedAngle and elevationCalculatedAngle.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_pointing_mount_position_dec_mean IS 'Dec calculated from the azimuthCalculatedAngle and elevationCalculatedAngle.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_pointing_mount_position_dec_stddev IS 'Dec calculated from the azimuthCalculatedAngle and elevationCalculatedAngle.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_pointing_mount_position_sky_angle_mean IS 'Calculated sky angle.';
COMMENT ON COLUMN cdb_latiss.visit1_efd.at_pointing_mount_position_sky_angle_stddev IS 'Calculated sky angle.';
COMMENT ON CONSTRAINT un_visit_id_instrument ON cdb_latiss.visit1_efd IS 'Ensure visit_id is unique.';

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
