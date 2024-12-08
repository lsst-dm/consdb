
CREATE TABLE cdb_lsstcomcamsim.exposure_efd (
	exposure_id BIGINT, 
	created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP, 
	instrument CHAR(20), 
	mt_azimuth_encoder_absolute_position_0_rms_jitter FLOAT, 
	mt_azimuth_encoder_absolute_position_1_rms_jitter FLOAT, 
	mt_azimuth_encoder_absolute_position_2_rms_jitter FLOAT, 
	mt_azimuth_encoder_absolute_position_3_rms_jitter FLOAT, 
	mt_elevation_encoder_absolute_position_0_rms_jitter FLOAT, 
	mt_elevation_encoder_absolute_position_1_rms_jitter FLOAT, 
	mt_elevation_encoder_absolute_position_2_rms_jitter FLOAT, 
	mt_elevation_encoder_absolute_position_3_rms_jitter FLOAT, 
	mt_salindex110_sonic_temperature_mean FLOAT, 
	mt_salindex110_sonic_temperature_stddev FLOAT, 
	at_salindex110_sonic_temperature_stddev_mean FLOAT, 
	at_salindex110_sonic_temperature_stddev_stddev FLOAT, 
	mt_salindex110_wind_speed_0_mean FLOAT, 
	mt_salindex110_wind_speed_0_stddev FLOAT, 
	mt_salindex110_wind_speed_0_min FLOAT, 
	mt_salindex110_wind_speed_0_max FLOAT, 
	mt_salindex110_wind_speed_1_mean FLOAT, 
	mt_salindex110_wind_speed_1_stddev FLOAT, 
	mt_salindex110_wind_speed_1_min FLOAT, 
	mt_salindex110_wind_speed_1_max FLOAT, 
	mt_salindex110_wind_speed_2_mean FLOAT, 
	mt_salindex110_wind_speed_2_stddev FLOAT, 
	mt_salindex110_wind_speed_2_min FLOAT, 
	mt_salindex110_wind_speed_2_max FLOAT, 
	mt_salindex110_wind_speed_speedstddev_0_mean FLOAT, 
	mt_salindex110_wind_speed_speedstddev_0_stddev FLOAT, 
	mt_salindex110_wind_speed_speedstddev_0_min FLOAT, 
	mt_salindex110_wind_speed_speedstddev_0_max FLOAT, 
	mt_salindex110_wind_speed_speedstddev_1_mean FLOAT, 
	mt_salindex110_wind_speed_speedstddev_1_stddev FLOAT, 
	mt_salindex110_wind_speed_speedstddev_1_min FLOAT, 
	mt_salindex110_wind_speed_speedstddev_1_max FLOAT, 
	mt_salindex110_wind_speed_speedstddev_2_mean FLOAT, 
	mt_salindex110_wind_speed_speedstddev_2_stddev FLOAT, 
	mt_salindex110_wind_speed_speedstddev_2_min FLOAT, 
	mt_salindex110_wind_speed_speedstddev_2_max FLOAT, 
	mt_salindex110_wind_speed_magnitude_mean FLOAT, 
	mt_salindex110_wind_speed_magnitude_stddev FLOAT, 
	mt_salindex110_wind_speed_magnitude_min FLOAT, 
	mt_salindex110_wind_speed_magnitude_max FLOAT, 
	mt_salindex110_wind_speed_maxmagnitude_mean FLOAT, 
	mt_salindex110_wind_speed_maxmagnitude_stddev FLOAT, 
	mt_salindex110_wind_speed_maxmagnitude_min FLOAT, 
	mt_salindex110_wind_speed_maxmagnitude_max FLOAT, 
	mt_salindex301_airflow_speed_mean FLOAT, 
	mt_salindex301_airflow_speed_stddev FLOAT, 
	mt_salindex301_airflow_speed_min FLOAT, 
	mt_salindex301_airflow_speed_max FLOAT, 
	mt_salindex301_airflow_speedstddev_mean FLOAT, 
	mt_salindex301_airflow_speedstddev_stddev FLOAT, 
	mt_salindex301_airflow_speedstddev_min FLOAT, 
	mt_salindex301_airflow_speedstddev_max FLOAT, 
	mt_salindex301_airflow_direction_mean FLOAT, 
	mt_salindex301_airflow_direction_stddev FLOAT, 
	mt_salindex301_airflow_direction_min FLOAT, 
	mt_salindex301_airflow_direction_max FLOAT, 
	mt_salindex1_temperature_0_mean FLOAT, 
	mt_salindex1_temperature_0_stddev FLOAT, 
	mt_salindex1_temperature_0_min FLOAT, 
	mt_salindex1_temperature_1_mean FLOAT, 
	mt_salindex1_temperature_0_max FLOAT, 
	mt_salindex1_temperature_1_stddev FLOAT, 
	mt_salindex1_temperature_1_min FLOAT, 
	mt_salindex1_temperature_1_max FLOAT, 
	mt_salindex1_temperature_2_mean FLOAT, 
	mt_salindex1_temperature_2_stddev FLOAT, 
	mt_salindex1_temperature_2_min FLOAT, 
	mt_salindex1_temperature_2_max FLOAT, 
	mt_salindex1_temperature_3_mean FLOAT, 
	mt_salindex1_temperature_3_stddev FLOAT, 
	mt_salindex1_temperature_3_min FLOAT, 
	mt_salindex1_temperature_3_max FLOAT, 
	mt_salindex1_temperature_4_mean FLOAT, 
	mt_salindex1_temperature_4_stddev FLOAT, 
	mt_salindex1_temperature_4_min FLOAT, 
	mt_salindex1_temperature_4_max FLOAT, 
	mt_salindex1_temperature_5_mean FLOAT, 
	mt_salindex1_temperature_5_stddev FLOAT, 
	mt_salindex1_temperature_5_min FLOAT, 
	mt_salindex1_temperature_5_max FLOAT, 
	mt_salindex1_temperature_6_mean FLOAT, 
	mt_salindex1_temperature_6_stddev FLOAT, 
	mt_salindex1_temperature_6_min FLOAT, 
	mt_salindex1_temperature_6_max FLOAT, 
	mt_salindex1_temperature_7_mean FLOAT, 
	mt_salindex1_temperature_7_stddev FLOAT, 
	mt_salindex1_temperature_7_min FLOAT, 
	mt_salindex1_temperature_7_max FLOAT, 
	mt_salindex101_temperature_0_mean FLOAT, 
	mt_salindex101_temperature_0_stddev FLOAT, 
	mt_salindex101_temperature_0_min FLOAT, 
	mt_salindex101_temperature_1_mean FLOAT, 
	mt_salindex101_temperature_0_max FLOAT, 
	mt_salindex101_temperature_1_stddev FLOAT, 
	mt_salindex101_temperature_1_min FLOAT, 
	mt_salindex101_temperature_1_max FLOAT, 
	mt_salindex101_temperature_2_mean FLOAT, 
	mt_salindex101_temperature_2_stddev FLOAT, 
	mt_salindex101_temperature_2_min FLOAT, 
	mt_salindex101_temperature_2_max FLOAT, 
	mt_salindex101_temperature_3_mean FLOAT, 
	mt_salindex101_temperature_3_stddev FLOAT, 
	mt_salindex101_temperature_3_min FLOAT, 
	mt_salindex101_temperature_3_max FLOAT, 
	mt_salindex101_temperature_4_mean FLOAT, 
	mt_salindex101_temperature_4_stddev FLOAT, 
	mt_salindex101_temperature_4_min FLOAT, 
	mt_salindex101_temperature_4_max FLOAT, 
	mt_salindex101_temperature_5_mean FLOAT, 
	mt_salindex101_temperature_5_stddev FLOAT, 
	mt_salindex101_temperature_5_min FLOAT, 
	mt_salindex101_temperature_5_max FLOAT, 
	mt_salindex101_temperature_6_mean FLOAT, 
	mt_salindex101_temperature_6_stddev FLOAT, 
	mt_salindex101_temperature_6_min FLOAT, 
	mt_salindex101_temperature_6_max FLOAT, 
	mt_salindex101_temperature_7_mean FLOAT, 
	mt_salindex101_temperature_7_stddev FLOAT, 
	mt_salindex101_temperature_7_min FLOAT, 
	mt_salindex101_temperature_7_max FLOAT, 
	mt_salindex102_temperature_0_mean FLOAT, 
	mt_salindex102_temperature_0_stddev FLOAT, 
	mt_salindex102_temperature_0_min FLOAT, 
	mt_salindex102_temperature_1_mean FLOAT, 
	mt_salindex102_temperature_0_max FLOAT, 
	mt_salindex102_temperature_1_stddev FLOAT, 
	mt_salindex102_temperature_1_min FLOAT, 
	mt_salindex102_temperature_1_max FLOAT, 
	mt_salindex102_temperature_2_mean FLOAT, 
	mt_salindex102_temperature_2_stddev FLOAT, 
	mt_salindex102_temperature_2_min FLOAT, 
	mt_salindex102_temperature_2_max FLOAT, 
	mt_salindex102_temperature_3_mean FLOAT, 
	mt_salindex102_temperature_3_stddev FLOAT, 
	mt_salindex102_temperature_3_min FLOAT, 
	mt_salindex102_temperature_3_max FLOAT, 
	mt_salindex102_temperature_4_mean FLOAT, 
	mt_salindex102_temperature_4_stddev FLOAT, 
	mt_salindex102_temperature_4_min FLOAT, 
	mt_salindex102_temperature_4_max FLOAT, 
	mt_salindex102_temperature_5_mean FLOAT, 
	mt_salindex102_temperature_5_stddev FLOAT, 
	mt_salindex102_temperature_5_min FLOAT, 
	mt_salindex102_temperature_5_max FLOAT, 
	mt_salindex102_temperature_6_mean FLOAT, 
	mt_salindex102_temperature_6_stddev FLOAT, 
	mt_salindex102_temperature_6_min FLOAT, 
	mt_salindex102_temperature_6_max FLOAT, 
	mt_salindex102_temperature_7_mean FLOAT, 
	mt_salindex102_temperature_7_stddev FLOAT, 
	mt_salindex102_temperature_7_min FLOAT, 
	mt_salindex102_temperature_7_max FLOAT, 
	mt_salindex103_temperature_0_mean FLOAT, 
	mt_salindex103_temperature_0_stddev FLOAT, 
	mt_salindex103_temperature_0_min FLOAT, 
	mt_salindex103_temperature_1_mean FLOAT, 
	mt_salindex103_temperature_0_max FLOAT, 
	mt_salindex103_temperature_1_stddev FLOAT, 
	mt_salindex103_temperature_1_min FLOAT, 
	mt_salindex103_temperature_1_max FLOAT, 
	mt_salindex103_temperature_2_mean FLOAT, 
	mt_salindex103_temperature_2_stddev FLOAT, 
	mt_salindex103_temperature_2_min FLOAT, 
	mt_salindex103_temperature_2_max FLOAT, 
	mt_salindex103_temperature_3_mean FLOAT, 
	mt_salindex103_temperature_3_stddev FLOAT, 
	mt_salindex103_temperature_3_min FLOAT, 
	mt_salindex103_temperature_3_max FLOAT, 
	mt_salindex103_temperature_4_mean FLOAT, 
	mt_salindex103_temperature_4_stddev FLOAT, 
	mt_salindex103_temperature_4_min FLOAT, 
	mt_salindex103_temperature_4_max FLOAT, 
	mt_salindex103_temperature_5_mean FLOAT, 
	mt_salindex103_temperature_5_stddev FLOAT, 
	mt_salindex103_temperature_5_min FLOAT, 
	mt_salindex103_temperature_5_max FLOAT, 
	mt_salindex103_temperature_6_mean FLOAT, 
	mt_salindex103_temperature_6_stddev FLOAT, 
	mt_salindex103_temperature_6_min FLOAT, 
	mt_salindex103_temperature_6_max FLOAT, 
	mt_salindex103_temperature_7_mean FLOAT, 
	mt_salindex103_temperature_7_stddev FLOAT, 
	mt_salindex103_temperature_7_min FLOAT, 
	mt_salindex103_temperature_7_max FLOAT, 
	mt_salindex106_temperature_0_mean FLOAT, 
	mt_salindex106_temperature_0_stddev FLOAT, 
	mt_salindex106_temperature_0_min FLOAT, 
	mt_salindex106_temperature_1_mean FLOAT, 
	mt_salindex106_temperature_0_max FLOAT, 
	mt_salindex106_temperature_1_stddev FLOAT, 
	mt_salindex106_temperature_1_min FLOAT, 
	mt_salindex106_temperature_1_max FLOAT, 
	mt_salindex106_temperature_2_mean FLOAT, 
	mt_salindex106_temperature_2_stddev FLOAT, 
	mt_salindex106_temperature_2_min FLOAT, 
	mt_salindex106_temperature_2_max FLOAT, 
	mt_salindex106_temperature_3_mean FLOAT, 
	mt_salindex106_temperature_3_stddev FLOAT, 
	mt_salindex106_temperature_3_min FLOAT, 
	mt_salindex106_temperature_3_max FLOAT, 
	mt_salindex106_temperature_4_mean FLOAT, 
	mt_salindex106_temperature_4_stddev FLOAT, 
	mt_salindex106_temperature_4_min FLOAT, 
	mt_salindex106_temperature_4_max FLOAT, 
	mt_salindex106_temperature_5_mean FLOAT, 
	mt_salindex106_temperature_5_stddev FLOAT, 
	mt_salindex106_temperature_5_min FLOAT, 
	mt_salindex106_temperature_5_max FLOAT, 
	mt_salindex106_temperature_6_mean FLOAT, 
	mt_salindex106_temperature_6_stddev FLOAT, 
	mt_salindex106_temperature_6_min FLOAT, 
	mt_salindex106_temperature_6_max FLOAT, 
	mt_salindex106_temperature_7_mean FLOAT, 
	mt_salindex106_temperature_7_stddev FLOAT, 
	mt_salindex106_temperature_7_min FLOAT, 
	mt_salindex106_temperature_7_max FLOAT, 
	mt_salindex107_temperature_0_mean FLOAT, 
	mt_salindex107_temperature_0_stddev FLOAT, 
	mt_salindex107_temperature_0_min FLOAT, 
	mt_salindex107_temperature_1_mean FLOAT, 
	mt_salindex107_temperature_0_max FLOAT, 
	mt_salindex107_temperature_1_stddev FLOAT, 
	mt_salindex107_temperature_1_min FLOAT, 
	mt_salindex107_temperature_1_max FLOAT, 
	mt_salindex107_temperature_2_mean FLOAT, 
	mt_salindex107_temperature_2_stddev FLOAT, 
	mt_salindex107_temperature_2_min FLOAT, 
	mt_salindex107_temperature_2_max FLOAT, 
	mt_salindex107_temperature_3_mean FLOAT, 
	mt_salindex107_temperature_3_stddev FLOAT, 
	mt_salindex107_temperature_3_min FLOAT, 
	mt_salindex107_temperature_3_max FLOAT, 
	mt_salindex107_temperature_4_mean FLOAT, 
	mt_salindex107_temperature_4_stddev FLOAT, 
	mt_salindex107_temperature_4_min FLOAT, 
	mt_salindex107_temperature_4_max FLOAT, 
	mt_salindex107_temperature_5_mean FLOAT, 
	mt_salindex107_temperature_5_stddev FLOAT, 
	mt_salindex107_temperature_5_min FLOAT, 
	mt_salindex107_temperature_5_max FLOAT, 
	mt_salindex107_temperature_6_mean FLOAT, 
	mt_salindex107_temperature_6_stddev FLOAT, 
	mt_salindex107_temperature_6_min FLOAT, 
	mt_salindex107_temperature_6_max FLOAT, 
	mt_salindex107_temperature_7_mean FLOAT, 
	mt_salindex107_temperature_7_stddev FLOAT, 
	mt_salindex107_temperature_7_min FLOAT, 
	mt_salindex107_temperature_7_max FLOAT, 
	mt_salindex108_temperature_0_mean FLOAT, 
	mt_salindex108_temperature_0_stddev FLOAT, 
	mt_salindex108_temperature_0_min FLOAT, 
	mt_salindex108_temperature_1_mean FLOAT, 
	mt_salindex108_temperature_0_max FLOAT, 
	mt_salindex108_temperature_1_stddev FLOAT, 
	mt_salindex108_temperature_1_min FLOAT, 
	mt_salindex108_temperature_1_max FLOAT, 
	mt_salindex108_temperature_2_mean FLOAT, 
	mt_salindex108_temperature_2_stddev FLOAT, 
	mt_salindex108_temperature_2_min FLOAT, 
	mt_salindex108_temperature_2_max FLOAT, 
	mt_salindex108_temperature_3_mean FLOAT, 
	mt_salindex108_temperature_3_stddev FLOAT, 
	mt_salindex108_temperature_3_min FLOAT, 
	mt_salindex108_temperature_3_max FLOAT, 
	mt_salindex108_temperature_4_mean FLOAT, 
	mt_salindex108_temperature_4_stddev FLOAT, 
	mt_salindex108_temperature_4_min FLOAT, 
	mt_salindex108_temperature_4_max FLOAT, 
	mt_salindex108_temperature_5_mean FLOAT, 
	mt_salindex108_temperature_5_stddev FLOAT, 
	mt_salindex108_temperature_5_min FLOAT, 
	mt_salindex108_temperature_5_max FLOAT, 
	mt_salindex108_temperature_6_mean FLOAT, 
	mt_salindex108_temperature_6_stddev FLOAT, 
	mt_salindex108_temperature_6_min FLOAT, 
	mt_salindex108_temperature_6_max FLOAT, 
	mt_salindex108_temperature_7_mean FLOAT, 
	mt_salindex108_temperature_7_stddev FLOAT, 
	mt_salindex108_temperature_7_min FLOAT, 
	mt_salindex108_temperature_7_max FLOAT, 
	mt_salindex301_temperature_0_mean FLOAT, 
	mt_salindex301_temperature_0_stddev FLOAT, 
	mt_salindex301_temperature_0_min FLOAT, 
	mt_salindex301_temperature_1_mean FLOAT, 
	mt_salindex301_temperature_0_max FLOAT, 
	mt_salindex301_temperature_1_stddev FLOAT, 
	mt_salindex301_temperature_1_min FLOAT, 
	mt_salindex301_temperature_1_max FLOAT, 
	mt_salindex301_temperature_2_mean FLOAT, 
	mt_salindex301_temperature_2_stddev FLOAT, 
	mt_salindex301_temperature_2_min FLOAT, 
	mt_salindex301_temperature_2_max FLOAT, 
	mt_salindex301_temperature_3_mean FLOAT, 
	mt_salindex301_temperature_3_stddev FLOAT, 
	mt_salindex301_temperature_3_min FLOAT, 
	mt_salindex301_temperature_3_max FLOAT, 
	mt_salindex301_temperature_4_mean FLOAT, 
	mt_salindex301_temperature_4_stddev FLOAT, 
	mt_salindex301_temperature_4_min FLOAT, 
	mt_salindex301_temperature_4_max FLOAT, 
	mt_salindex301_temperature_5_mean FLOAT, 
	mt_salindex301_temperature_5_stddev FLOAT, 
	mt_salindex301_temperature_5_min FLOAT, 
	mt_salindex301_temperature_5_max FLOAT, 
	mt_salindex301_temperature_6_mean FLOAT, 
	mt_salindex301_temperature_6_stddev FLOAT, 
	mt_salindex301_temperature_6_min FLOAT, 
	mt_salindex301_temperature_6_max FLOAT, 
	mt_salindex301_temperature_7_mean FLOAT, 
	mt_salindex301_temperature_7_stddev FLOAT, 
	mt_salindex301_temperature_7_min FLOAT, 
	mt_salindex301_temperature_7_max FLOAT, 
	mt_dimm_fwhm_mean FLOAT, 
	mt_azimuth_encoder_absolute_position_0_mean FLOAT, 
	mt_azimuth_encoder_absolute_position_1_mean FLOAT, 
	mt_azimuth_encoder_absolute_position_2_mean FLOAT, 
	mt_azimuth_encoder_absolute_position_3_mean FLOAT, 
	mt_elevation_encoder_absolute_position_0_mean FLOAT, 
	mt_elevation_encoder_absolute_position_1_mean FLOAT, 
	mt_elevation_encoder_absolute_position_2_mean FLOAT, 
	mt_elevation_encoder_absolute_position_3_mean FLOAT, 
	mt_hexapod_uncompensated_position_u_mean FLOAT, 
	mt_hexapod_uncompensated_position_u_max FLOAT, 
	mt_hexapod_uncompensated_position_u_min FLOAT, 
	mt_hexapod_uncompensated_position_v_mean FLOAT, 
	mt_hexapod_uncompensated_position_v_max FLOAT, 
	mt_hexapod_uncompensated_position_v_min FLOAT, 
	mt_hexapod_uncompensated_position_w_mean FLOAT, 
	mt_hexapod_uncompensated_position_w_max FLOAT, 
	mt_hexapod_uncompensated_position_w_min FLOAT, 
	mt_hexapod_uncompensated_position_x_mean FLOAT, 
	mt_hexapod_uncompensated_position_x_max FLOAT, 
	mt_hexapod_uncompensated_position_x_min FLOAT, 
	mt_hexapod_uncompensated_position_y_mean FLOAT, 
	mt_hexapod_uncompensated_position_y_max FLOAT, 
	mt_hexapod_uncompensated_position_y_min FLOAT, 
	mt_hexapod_uncompensated_position_z_mean FLOAT, 
	mt_hexapod_uncompensated_position_z_max FLOAT, 
	mt_hexapod_uncompensated_position_z_min FLOAT, 
	mt_salindex111_dewpoint_mean FLOAT, 
	mt_salindex112_dewpoint_mean FLOAT, 
	mt_salindex113_dewpoint_mean FLOAT, 
	mt_salindex111_relativehumidity_mean FLOAT, 
	mt_salindex112_relativehumidity_mean FLOAT, 
	mt_salindex113_relativehumidity_mean FLOAT, 
	mt_salindex113_pressure_0_mean FLOAT, 
	mt_salindex113_pressure_1_mean FLOAT, 
	mt_salindex301_pressure_0_mean FLOAT, 
	mt_salindex301_pressure_1_mean FLOAT, 
	mt_pointing_mount_position_ra_mean FLOAT, 
	mt_pointing_mount_position_ra_stddev FLOAT, 
	mt_pointing_mount_position_dec_mean FLOAT, 
	mt_pointing_mount_position_dec_stddev FLOAT, 
	mt_pointing_mount_position_sky_angle_mean FLOAT, 
	mt_pointing_mount_position_sky_angle_stddev FLOAT, 
	mt_pointing_mount_position_rotator_mean FLOAT, 
	mt_pointing_mount_position_rotator_stddev FLOAT, 
	camera_hexapod_aos_corrections_u FLOAT, 
	camera_hexapod_aos_corrections_v FLOAT, 
	camera_hexapod_aos_corrections_w FLOAT, 
	camera_hexapod_aos_corrections_x FLOAT, 
	camera_hexapod_aos_corrections_y FLOAT, 
	camera_hexapod_aos_corrections_z FLOAT, 
	m2_hexapod_aos_corrections_u FLOAT, 
	m2_hexapod_aos_corrections_v FLOAT, 
	m2_hexapod_aos_corrections_w FLOAT, 
	m2_hexapod_aos_corrections_x FLOAT, 
	m2_hexapod_aos_corrections_y FLOAT, 
	m2_hexapod_aos_corrections_z FLOAT, 
	m2_stress FLOAT, 
	m1m3_stress FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_0_mean" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_0_stddev" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_0_max" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_0_min" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_1_mean" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_1_stddev" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_1_max" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_1_min" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_2_mean" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_2_stddev" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_2_max" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_2_min" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_3_mean" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_3_stddev" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_3_max" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_3_min" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_4_mean" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_4_stddev" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_4_max" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_4_min" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_5_mean" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_5_stddev" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_5_max" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_5_min" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_6_mean" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_6_stddev" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_6_max" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_6_min" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_7_mean" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_7_stddev" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_7_max" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_7_min" FLOAT, 
	"mt_salIndex104_m1m3_angular_acceleration_x_mean" FLOAT, 
	"mt_salIndex104_m1m3_angular_acceleration_x_stddev" FLOAT, 
	"mt_salIndex104_m1m3_angular_acceleration_x_max" FLOAT, 
	"mt_salIndex104_m1m3_angular_acceleration_x_min" FLOAT, 
	"mt_salIndex104_m1m3_angular_acceleration_y_mean" FLOAT, 
	"mt_salIndex104_m1m3_angular_acceleration_y_stddev" FLOAT, 
	"mt_salIndex104_m1m3_angular_acceleration_y_max" FLOAT, 
	"mt_salIndex104_m1m3_angular_acceleration_y_min" FLOAT, 
	"mt_salIndex104_m1m3_angular_acceleration_z_mean" FLOAT, 
	"mt_salIndex104_m1m3_angular_acceleration_z_stddev" FLOAT, 
	"mt_salIndex104_m1m3_angular_acceleration_z_max" FLOAT, 
	"mt_salIndex104_m1m3_angular_acceleration_z_min" FLOAT, 
	PRIMARY KEY (exposure_id, instrument), 
	CONSTRAINT un_exposure_id_instrument UNIQUE (exposure_id, instrument)
)

;
COMMENT ON TABLE cdb_lsstcomcamsim.exposure_efd IS 'Transformed EFD topics by exposure.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.exposure_id IS 'Exposure unique ID.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.created_at IS 'Timestamp when the record was created, default is the current timestamp';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.instrument IS 'Instrument name.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_azimuth_encoder_absolute_position_0_rms_jitter IS 'RMS after 4th order polynomial fit of Azimuth absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_azimuth_encoder_absolute_position_1_rms_jitter IS 'RMS after 4th order polynomial fit of Azimuth absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_azimuth_encoder_absolute_position_2_rms_jitter IS 'RMS after 4th order polynomial fit of Azimuth absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_azimuth_encoder_absolute_position_3_rms_jitter IS 'RMS after 4th order polynomial fit of Azimuth absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_elevation_encoder_absolute_position_0_rms_jitter IS 'RMS after 4th order polynomial fit of Elevation absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_elevation_encoder_absolute_position_1_rms_jitter IS 'RMS after 4th order polynomial fit of Elevation absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_elevation_encoder_absolute_position_2_rms_jitter IS 'RMS after 4th order polynomial fit of Elevation absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_elevation_encoder_absolute_position_3_rms_jitter IS 'RMS after 4th order polynomial fit of Elevation absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_sonic_temperature_mean IS 'Median sonic temperature (air temperature measured sonically). Sonic temperature has poor absolute accuracy (it can be off by several degrees) but good time resolution.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_sonic_temperature_stddev IS 'Median sonic temperature (air temperature measured sonically). Sonic temperature has poor absolute accuracy (it can be off by several degrees) but good time resolution.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.at_salindex110_sonic_temperature_stddev_mean IS 'Standard devation of sonic temperature (air temperature measured sonically) estimated from quartiles.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.at_salindex110_sonic_temperature_stddev_stddev IS 'Standard devation of sonic temperature (air temperature measured sonically) estimated from quartiles.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_wind_speed_0_mean IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 0 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_wind_speed_0_stddev IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 0 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_wind_speed_0_min IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 0 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_wind_speed_0_max IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 0 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_wind_speed_1_mean IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 1 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_wind_speed_1_stddev IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 1 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_wind_speed_1_min IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 1 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_wind_speed_1_max IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 1 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_wind_speed_2_mean IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 2 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_wind_speed_2_stddev IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 2 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_wind_speed_2_min IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 2 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_wind_speed_2_max IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 2 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_wind_speed_speedstddev_0_mean IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 0 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_wind_speed_speedstddev_0_stddev IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 0 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_wind_speed_speedstddev_0_min IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 0 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_wind_speed_speedstddev_0_max IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 0 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_wind_speed_speedstddev_1_mean IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 1 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_wind_speed_speedstddev_1_stddev IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 1 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_wind_speed_speedstddev_1_min IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 1 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_wind_speed_speedstddev_1_max IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 1 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_wind_speed_speedstddev_2_mean IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 2 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_wind_speed_speedstddev_2_stddev IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 2 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_wind_speed_speedstddev_2_min IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 2 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_wind_speed_speedstddev_2_max IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 2 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_wind_speed_magnitude_mean IS 'Median wind speed magnitude in TMA-GillLabJack01 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_wind_speed_magnitude_stddev IS 'Median wind speed magnitude in TMA-GillLabJack01 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_wind_speed_magnitude_min IS 'Median wind speed magnitude in TMA-GillLabJack01 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_wind_speed_magnitude_max IS 'Median wind speed magnitude in TMA-GillLabJack01 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_wind_speed_maxmagnitude_mean IS 'Maximum wind speed magnitude in TMA-GillLabJack01 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_wind_speed_maxmagnitude_stddev IS 'Maximum wind speed magnitude in TMA-GillLabJack01 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_wind_speed_maxmagnitude_min IS 'Maximum wind speed magnitude in TMA-GillLabJack01 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex110_wind_speed_maxmagnitude_max IS 'Maximum wind speed magnitude in TMA-GillLabJack01 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_airflow_speed_mean IS 'Median (mean for some sensors) wind speed in XX (salIndex 301)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_airflow_speed_stddev IS 'Median (mean for some sensors) wind speed in XX (salIndex 301)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_airflow_speed_min IS 'Median (mean for some sensors) wind speed in XX (salIndex 301)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_airflow_speed_max IS 'Median (mean for some sensors) wind speed in XX (salIndex 301)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_airflow_speedstddev_mean IS 'Standard deviation of wind speed estimated from quartiles in XX (salIndex 301). Not available for all sensor types.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_airflow_speedstddev_stddev IS 'Standard deviation of wind speed estimated from quartiles in XX (salIndex 301). Not available for all sensor types.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_airflow_speedstddev_min IS 'Standard deviation of wind speed estimated from quartiles in XX (salIndex 301). Not available for all sensor types.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_airflow_speedstddev_max IS 'Standard deviation of wind speed estimated from quartiles in XX (salIndex 301). Not available for all sensor types.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_airflow_direction_mean IS 'Median (mean for some sensors) wind speed in XX (salIndex 301)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_airflow_direction_stddev IS 'Median (mean for some sensors) wind speed in XX (salIndex 301)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_airflow_direction_min IS 'Median (mean for some sensors) wind speed in XX (salIndex 301)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_airflow_direction_max IS 'Median (mean for some sensors) wind speed in XX (salIndex 301)';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex1_temperature_0_mean IS 'MTCameraAssembly-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex1_temperature_0_stddev IS 'MTCameraAssembly-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex1_temperature_0_min IS 'MTCameraAssembly-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex1_temperature_1_mean IS 'MTCameraAssembly-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex1_temperature_0_max IS 'MTCameraAssembly-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex1_temperature_1_stddev IS 'MTCameraAssembly-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex1_temperature_1_min IS 'MTCameraAssembly-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex1_temperature_1_max IS 'MTCameraAssembly-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex1_temperature_2_mean IS 'MTCameraAssembly-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex1_temperature_2_stddev IS 'MTCameraAssembly-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex1_temperature_2_min IS 'MTCameraAssembly-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex1_temperature_2_max IS 'MTCameraAssembly-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex1_temperature_3_mean IS 'MTCameraAssembly-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex1_temperature_3_stddev IS 'MTCameraAssembly-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex1_temperature_3_min IS 'MTCameraAssembly-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex1_temperature_3_max IS 'MTCameraAssembly-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex1_temperature_4_mean IS 'MTCameraAssembly-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex1_temperature_4_stddev IS 'MTCameraAssembly-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex1_temperature_4_min IS 'MTCameraAssembly-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex1_temperature_4_max IS 'MTCameraAssembly-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex1_temperature_5_mean IS 'MTCameraAssembly-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex1_temperature_5_stddev IS 'MTCameraAssembly-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex1_temperature_5_min IS 'MTCameraAssembly-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex1_temperature_5_max IS 'MTCameraAssembly-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex1_temperature_6_mean IS 'MTCameraAssembly-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex1_temperature_6_stddev IS 'MTCameraAssembly-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex1_temperature_6_min IS 'MTCameraAssembly-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex1_temperature_6_max IS 'MTCameraAssembly-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex1_temperature_7_mean IS 'MTCameraAssembly-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex1_temperature_7_stddev IS 'MTCameraAssembly-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex1_temperature_7_min IS 'MTCameraAssembly-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex1_temperature_7_max IS 'MTCameraAssembly-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex101_temperature_0_mean IS 'MTCameraAssembly-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex101_temperature_0_stddev IS 'MTCameraAssembly-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex101_temperature_0_min IS 'MTCameraAssembly-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex101_temperature_1_mean IS 'MTCameraAssembly-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex101_temperature_0_max IS 'MTCameraAssembly-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex101_temperature_1_stddev IS 'MTCameraAssembly-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex101_temperature_1_min IS 'MTCameraAssembly-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex101_temperature_1_max IS 'MTCameraAssembly-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex101_temperature_2_mean IS 'MTCameraAssembly-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex101_temperature_2_stddev IS 'MTCameraAssembly-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex101_temperature_2_min IS 'MTCameraAssembly-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex101_temperature_2_max IS 'MTCameraAssembly-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex101_temperature_3_mean IS 'MTCameraAssembly-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex101_temperature_3_stddev IS 'MTCameraAssembly-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex101_temperature_3_min IS 'MTCameraAssembly-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex101_temperature_3_max IS 'MTCameraAssembly-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex101_temperature_4_mean IS 'MTCameraAssembly-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex101_temperature_4_stddev IS 'MTCameraAssembly-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex101_temperature_4_min IS 'MTCameraAssembly-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex101_temperature_4_max IS 'MTCameraAssembly-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex101_temperature_5_mean IS 'MTCameraAssembly-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex101_temperature_5_stddev IS 'MTCameraAssembly-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex101_temperature_5_min IS 'MTCameraAssembly-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex101_temperature_5_max IS 'MTCameraAssembly-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex101_temperature_6_mean IS 'MTCameraAssembly-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex101_temperature_6_stddev IS 'MTCameraAssembly-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex101_temperature_6_min IS 'MTCameraAssembly-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex101_temperature_6_max IS 'MTCameraAssembly-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex101_temperature_7_mean IS 'MTCameraAssembly-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex101_temperature_7_stddev IS 'MTCameraAssembly-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex101_temperature_7_min IS 'MTCameraAssembly-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex101_temperature_7_max IS 'MTCameraAssembly-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex102_temperature_0_mean IS 'XX temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex102_temperature_0_stddev IS 'XX temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex102_temperature_0_min IS 'XX temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex102_temperature_1_mean IS 'XX temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex102_temperature_0_max IS 'XX temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex102_temperature_1_stddev IS 'XX temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex102_temperature_1_min IS 'XX temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex102_temperature_1_max IS 'XX temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex102_temperature_2_mean IS 'XX temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex102_temperature_2_stddev IS 'XX temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex102_temperature_2_min IS 'XX temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex102_temperature_2_max IS 'XX temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex102_temperature_3_mean IS 'XX temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex102_temperature_3_stddev IS 'XX temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex102_temperature_3_min IS 'XX temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex102_temperature_3_max IS 'XX temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex102_temperature_4_mean IS 'XX temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex102_temperature_4_stddev IS 'XX temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex102_temperature_4_min IS 'XX temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex102_temperature_4_max IS 'XX temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex102_temperature_5_mean IS 'XX temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex102_temperature_5_stddev IS 'XX temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex102_temperature_5_min IS 'XX temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex102_temperature_5_max IS 'XX temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex102_temperature_6_mean IS 'XX temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex102_temperature_6_stddev IS 'XX temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex102_temperature_6_min IS 'XX temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex102_temperature_6_max IS 'XX temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex102_temperature_7_mean IS 'XX temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex102_temperature_7_stddev IS 'XX temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex102_temperature_7_min IS 'XX temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex102_temperature_7_max IS 'XX temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex103_temperature_0_mean IS 'XX temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex103_temperature_0_stddev IS 'XX temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex103_temperature_0_min IS 'XX temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex103_temperature_1_mean IS 'XX temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex103_temperature_0_max IS 'XX temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex103_temperature_1_stddev IS 'XX temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex103_temperature_1_min IS 'XX temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex103_temperature_1_max IS 'XX temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex103_temperature_2_mean IS 'XX temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex103_temperature_2_stddev IS 'XX temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex103_temperature_2_min IS 'XX temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex103_temperature_2_max IS 'XX temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex103_temperature_3_mean IS 'XX temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex103_temperature_3_stddev IS 'XX temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex103_temperature_3_min IS 'XX temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex103_temperature_3_max IS 'XX temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex103_temperature_4_mean IS 'XX temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex103_temperature_4_stddev IS 'XX temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex103_temperature_4_min IS 'XX temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex103_temperature_4_max IS 'XX temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex103_temperature_5_mean IS 'XX temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex103_temperature_5_stddev IS 'XX temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex103_temperature_5_min IS 'XX temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex103_temperature_5_max IS 'XX temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex103_temperature_6_mean IS 'XX temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex103_temperature_6_stddev IS 'XX temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex103_temperature_6_min IS 'XX temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex103_temperature_6_max IS 'XX temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex103_temperature_7_mean IS 'XX temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex103_temperature_7_stddev IS 'XX temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex103_temperature_7_min IS 'XX temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex103_temperature_7_max IS 'XX temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex106_temperature_0_mean IS 'M2-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex106_temperature_0_stddev IS 'M2-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex106_temperature_0_min IS 'M2-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex106_temperature_1_mean IS 'M2-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex106_temperature_0_max IS 'M2-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex106_temperature_1_stddev IS 'M2-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex106_temperature_1_min IS 'M2-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex106_temperature_1_max IS 'M2-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex106_temperature_2_mean IS 'M2-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex106_temperature_2_stddev IS 'M2-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex106_temperature_2_min IS 'M2-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex106_temperature_2_max IS 'M2-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex106_temperature_3_mean IS 'M2-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex106_temperature_3_stddev IS 'M2-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex106_temperature_3_min IS 'M2-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex106_temperature_3_max IS 'M2-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex106_temperature_4_mean IS 'M2-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex106_temperature_4_stddev IS 'M2-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex106_temperature_4_min IS 'M2-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex106_temperature_4_max IS 'M2-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex106_temperature_5_mean IS 'M2-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex106_temperature_5_stddev IS 'M2-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex106_temperature_5_min IS 'M2-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex106_temperature_5_max IS 'M2-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex106_temperature_6_mean IS 'M2-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex106_temperature_6_stddev IS 'M2-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex106_temperature_6_min IS 'M2-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex106_temperature_6_max IS 'M2-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex106_temperature_7_mean IS 'M2-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex106_temperature_7_stddev IS 'M2-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex106_temperature_7_min IS 'M2-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex106_temperature_7_max IS 'M2-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex107_temperature_0_mean IS 'Laser-ESS01, Laser-ESS02 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex107_temperature_0_stddev IS 'Laser-ESS01, Laser-ESS02 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex107_temperature_0_min IS 'Laser-ESS01, Laser-ESS02 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex107_temperature_1_mean IS 'Laser-ESS01, Laser-ESS02 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex107_temperature_0_max IS 'Laser-ESS01, Laser-ESS02 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex107_temperature_1_stddev IS 'Laser-ESS01, Laser-ESS02 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex107_temperature_1_min IS 'Laser-ESS01, Laser-ESS02 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex107_temperature_1_max IS 'Laser-ESS01, Laser-ESS02 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex107_temperature_2_mean IS 'Laser-ESS01, Laser-ESS02 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex107_temperature_2_stddev IS 'Laser-ESS01, Laser-ESS02 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex107_temperature_2_min IS 'Laser-ESS01, Laser-ESS02 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex107_temperature_2_max IS 'Laser-ESS01, Laser-ESS02 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex107_temperature_3_mean IS 'Laser-ESS01, Laser-ESS02 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex107_temperature_3_stddev IS 'Laser-ESS01, Laser-ESS02 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex107_temperature_3_min IS 'Laser-ESS01, Laser-ESS02 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex107_temperature_3_max IS 'Laser-ESS01, Laser-ESS02 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex107_temperature_4_mean IS 'Laser-ESS01, Laser-ESS02 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex107_temperature_4_stddev IS 'Laser-ESS01, Laser-ESS02 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex107_temperature_4_min IS 'Laser-ESS01, Laser-ESS02 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex107_temperature_4_max IS 'Laser-ESS01, Laser-ESS02 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex107_temperature_5_mean IS 'Laser-ESS01, Laser-ESS02 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex107_temperature_5_stddev IS 'Laser-ESS01, Laser-ESS02 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex107_temperature_5_min IS 'Laser-ESS01, Laser-ESS02 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex107_temperature_5_max IS 'Laser-ESS01, Laser-ESS02 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex107_temperature_6_mean IS 'Laser-ESS01, Laser-ESS02 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex107_temperature_6_stddev IS 'Laser-ESS01, Laser-ESS02 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex107_temperature_6_min IS 'Laser-ESS01, Laser-ESS02 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex107_temperature_6_max IS 'Laser-ESS01, Laser-ESS02 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex107_temperature_7_mean IS 'Laser-ESS01, Laser-ESS02 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex107_temperature_7_stddev IS 'Laser-ESS01, Laser-ESS02 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex107_temperature_7_min IS 'Laser-ESS01, Laser-ESS02 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex107_temperature_7_max IS 'Laser-ESS01, Laser-ESS02 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex108_temperature_0_mean IS 'CBP-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex108_temperature_0_stddev IS 'CBP-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex108_temperature_0_min IS 'CBP-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex108_temperature_1_mean IS 'CBP-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex108_temperature_0_max IS 'CBP-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex108_temperature_1_stddev IS 'CBP-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex108_temperature_1_min IS 'CBP-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex108_temperature_1_max IS 'CBP-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex108_temperature_2_mean IS 'CBP-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex108_temperature_2_stddev IS 'CBP-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex108_temperature_2_min IS 'CBP-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex108_temperature_2_max IS 'CBP-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex108_temperature_3_mean IS 'CBP-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex108_temperature_3_stddev IS 'CBP-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex108_temperature_3_min IS 'CBP-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex108_temperature_3_max IS 'CBP-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex108_temperature_4_mean IS 'CBP-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex108_temperature_4_stddev IS 'CBP-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex108_temperature_4_min IS 'CBP-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex108_temperature_4_max IS 'CBP-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex108_temperature_5_mean IS 'CBP-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex108_temperature_5_stddev IS 'CBP-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex108_temperature_5_min IS 'CBP-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex108_temperature_5_max IS 'CBP-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex108_temperature_6_mean IS 'CBP-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex108_temperature_6_stddev IS 'CBP-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex108_temperature_6_min IS 'CBP-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex108_temperature_6_max IS 'CBP-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex108_temperature_7_mean IS 'CBP-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex108_temperature_7_stddev IS 'CBP-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex108_temperature_7_min IS 'CBP-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex108_temperature_7_max IS 'CBP-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_temperature_0_mean IS 'Weather tower air temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_temperature_0_stddev IS 'Weather tower air temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_temperature_0_min IS 'Weather tower air temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_temperature_1_mean IS 'Weather tower air temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_temperature_0_max IS 'Weather tower air temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_temperature_1_stddev IS 'Weather tower air temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_temperature_1_min IS 'Weather tower air temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_temperature_1_max IS 'Weather tower air temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_temperature_2_mean IS 'Weather tower air temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_temperature_2_stddev IS 'Weather tower air temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_temperature_2_min IS 'Weather tower air temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_temperature_2_max IS 'Weather tower air temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_temperature_3_mean IS 'Weather tower air temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_temperature_3_stddev IS 'Weather tower air temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_temperature_3_min IS 'Weather tower air temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_temperature_3_max IS 'Weather tower air temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_temperature_4_mean IS 'Weather tower air temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_temperature_4_stddev IS 'Weather tower air temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_temperature_4_min IS 'Weather tower air temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_temperature_4_max IS 'Weather tower air temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_temperature_5_mean IS 'Weather tower air temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_temperature_5_stddev IS 'Weather tower air temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_temperature_5_min IS 'Weather tower air temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_temperature_5_max IS 'Weather tower air temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_temperature_6_mean IS 'Weather tower air temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_temperature_6_stddev IS 'Weather tower air temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_temperature_6_min IS 'Weather tower air temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_temperature_6_max IS 'Weather tower air temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_temperature_7_mean IS 'Weather tower air temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_temperature_7_stddev IS 'Weather tower air temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_temperature_7_min IS 'Weather tower air temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_temperature_7_max IS 'Weather tower air temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_dimm_fwhm_mean IS 'Combined full width half maximum';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_azimuth_encoder_absolute_position_0_mean IS 'Azimuth absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_azimuth_encoder_absolute_position_1_mean IS 'Azimuth absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_azimuth_encoder_absolute_position_2_mean IS 'Azimuth absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_azimuth_encoder_absolute_position_3_mean IS 'Azimuth absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_elevation_encoder_absolute_position_0_mean IS 'Elevation absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_elevation_encoder_absolute_position_1_mean IS 'Elevation absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_elevation_encoder_absolute_position_2_mean IS 'Elevation absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_elevation_encoder_absolute_position_3_mean IS 'Elevation absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_hexapod_uncompensated_position_u_mean IS 'U angle.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_hexapod_uncompensated_position_u_max IS 'U angle.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_hexapod_uncompensated_position_u_min IS 'U angle.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_hexapod_uncompensated_position_v_mean IS 'V angle.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_hexapod_uncompensated_position_v_max IS 'V angle.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_hexapod_uncompensated_position_v_min IS 'V angle.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_hexapod_uncompensated_position_w_mean IS 'W angle.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_hexapod_uncompensated_position_w_max IS 'W angle.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_hexapod_uncompensated_position_w_min IS 'W angle.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_hexapod_uncompensated_position_x_mean IS 'X position.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_hexapod_uncompensated_position_x_max IS 'X position.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_hexapod_uncompensated_position_x_min IS 'X position.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_hexapod_uncompensated_position_y_mean IS 'Y position.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_hexapod_uncompensated_position_y_max IS 'Y position.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_hexapod_uncompensated_position_y_min IS 'Y position.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_hexapod_uncompensated_position_z_mean IS 'Z position.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_hexapod_uncompensated_position_z_max IS 'Z position.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_hexapod_uncompensated_position_z_min IS 'Z position.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex111_dewpoint_mean IS 'Dew point.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex112_dewpoint_mean IS 'Dew point.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex113_dewpoint_mean IS 'Dew point.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex111_relativehumidity_mean IS 'Relative humidity.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex112_relativehumidity_mean IS 'Relative humidity.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex113_relativehumidity_mean IS 'Relative humidity.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex113_pressure_0_mean IS 'The pressures.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex113_pressure_1_mean IS 'The pressures.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_pressure_0_mean IS 'The pressures.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_salindex301_pressure_1_mean IS 'The pressures.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_pointing_mount_position_ra_mean IS 'RA calculated from the azimuthActualPosition and elevationActualPosition.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_pointing_mount_position_ra_stddev IS 'RA calculated from the azimuthActualPosition and elevationActualPosition.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_pointing_mount_position_dec_mean IS 'Dec calculated from the azimuthActualPosition and elevationActualPosition.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_pointing_mount_position_dec_stddev IS 'Dec calculated from the azimuthActualPosition and elevationActualPosition.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_pointing_mount_position_sky_angle_mean IS 'Calculated sky angle.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_pointing_mount_position_sky_angle_stddev IS 'Calculated sky angle.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_pointing_mount_position_rotator_mean IS 'Rotator axis position reported by rotator component.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.mt_pointing_mount_position_rotator_stddev IS 'Rotator axis position reported by rotator component.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.camera_hexapod_aos_corrections_u IS 'U position offset.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.camera_hexapod_aos_corrections_v IS 'V position offset.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.camera_hexapod_aos_corrections_w IS 'W position offset.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.camera_hexapod_aos_corrections_x IS 'X position offset.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.camera_hexapod_aos_corrections_y IS 'Y position offset.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.camera_hexapod_aos_corrections_z IS 'Z position offset.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.m2_hexapod_aos_corrections_u IS 'U position offset.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.m2_hexapod_aos_corrections_v IS 'V position offset.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.m2_hexapod_aos_corrections_w IS 'W position offset.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.m2_hexapod_aos_corrections_x IS 'X position offset.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.m2_hexapod_aos_corrections_y IS 'Y position offset.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.m2_hexapod_aos_corrections_z IS 'Z position offset.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.m2_stress IS 'Calculate M2 stress computed RSS the stress contribution of each bending mode.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd.m1m3_stress IS 'Calculate M1M3 stress computed RSS the stress contribution of each bending mode.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_accelerometer_0_mean" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_accelerometer_0_stddev" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_accelerometer_0_max" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_accelerometer_0_min" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_accelerometer_1_mean" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_accelerometer_1_stddev" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_accelerometer_1_max" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_accelerometer_1_min" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_accelerometer_2_mean" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_accelerometer_2_stddev" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_accelerometer_2_max" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_accelerometer_2_min" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_accelerometer_3_mean" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_accelerometer_3_stddev" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_accelerometer_3_max" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_accelerometer_3_min" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_accelerometer_4_mean" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_accelerometer_4_stddev" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_accelerometer_4_max" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_accelerometer_4_min" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_accelerometer_5_mean" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_accelerometer_5_stddev" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_accelerometer_5_max" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_accelerometer_5_min" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_accelerometer_6_mean" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_accelerometer_6_stddev" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_accelerometer_6_max" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_accelerometer_6_min" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_accelerometer_7_mean" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_accelerometer_7_stddev" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_accelerometer_7_max" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_accelerometer_7_min" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_angular_acceleration_x_mean" IS 'Accelerometer data angular Acceleration X.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_angular_acceleration_x_stddev" IS 'Accelerometer data angular Acceleration X.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_angular_acceleration_x_max" IS 'Accelerometer data angular Acceleration X.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_angular_acceleration_x_min" IS 'Accelerometer data angular Acceleration X.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_angular_acceleration_y_mean" IS 'Accelerometer data angular Acceleration Y.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_angular_acceleration_y_stddev" IS 'Accelerometer data angular Acceleration Y.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_angular_acceleration_y_max" IS 'Accelerometer data angular Acceleration Y.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_angular_acceleration_y_min" IS 'Accelerometer data angular Acceleration Y.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_angular_acceleration_z_mean" IS 'Accelerometer data angular Acceleration Z.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_angular_acceleration_z_stddev" IS 'Accelerometer data angular Acceleration Z.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_angular_acceleration_z_max" IS 'Accelerometer data angular Acceleration Z.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd."mt_salIndex104_m1m3_angular_acceleration_z_min" IS 'Accelerometer data angular Acceleration Z.';
COMMENT ON CONSTRAINT un_exposure_id_instrument ON cdb_lsstcomcamsim.exposure_efd IS 'Ensure exposure_id is unique.';

CREATE TABLE cdb_lsstcomcamsim.exposure_efd_unpivoted (
	exposure_id INTEGER NOT NULL, 
	topic CHAR(255) NOT NULL, 
	"column" CHAR(255) NOT NULL, 
	value DOUBLE PRECISION, 
	created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (exposure_id, topic, "column"), 
	CONSTRAINT un_exposure_topic_column UNIQUE (exposure_id, topic, "column")
)

;
COMMENT ON TABLE cdb_lsstcomcamsim.exposure_efd_unpivoted IS 'Unpivoted EFD exposure data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd_unpivoted.exposure_id IS 'Unique identifier for the exposure';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd_unpivoted.topic IS 'Topic name for the unpivoted data';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd_unpivoted."column" IS 'Column name for the unpivoted data';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd_unpivoted.value IS 'Value corresponding to the parameter';
COMMENT ON COLUMN cdb_lsstcomcamsim.exposure_efd_unpivoted.created_at IS 'Timestamp when the record was created, default is the current timestamp';
COMMENT ON CONSTRAINT un_exposure_topic_column ON cdb_lsstcomcamsim.exposure_efd_unpivoted IS 'Ensure the combination of exposure_id, topic, and column is unique.';

CREATE TABLE cdb_lsstcomcamsim.visit1_efd (
	visit_id BIGINT, 
	created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP, 
	instrument CHAR(20), 
	mt_salindex110_sonic_temperature_mean FLOAT, 
	mt_salindex110_sonic_temperature_stddev FLOAT, 
	at_salindex110_sonic_temperature_stddev_mean FLOAT, 
	at_salindex110_sonic_temperature_stddev_stddev FLOAT, 
	mt_salindex110_wind_speed_0_mean FLOAT, 
	mt_salindex110_wind_speed_0_stddev FLOAT, 
	mt_salindex110_wind_speed_0_min FLOAT, 
	mt_salindex110_wind_speed_0_max FLOAT, 
	mt_salindex110_wind_speed_1_mean FLOAT, 
	mt_salindex110_wind_speed_1_stddev FLOAT, 
	mt_salindex110_wind_speed_1_min FLOAT, 
	mt_salindex110_wind_speed_1_max FLOAT, 
	mt_salindex110_wind_speed_2_mean FLOAT, 
	mt_salindex110_wind_speed_2_stddev FLOAT, 
	mt_salindex110_wind_speed_2_min FLOAT, 
	mt_salindex110_wind_speed_2_max FLOAT, 
	mt_salindex110_wind_speed_speedstddev_0_mean FLOAT, 
	mt_salindex110_wind_speed_speedstddev_0_stddev FLOAT, 
	mt_salindex110_wind_speed_speedstddev_0_min FLOAT, 
	mt_salindex110_wind_speed_speedstddev_0_max FLOAT, 
	mt_salindex110_wind_speed_speedstddev_1_mean FLOAT, 
	mt_salindex110_wind_speed_speedstddev_1_stddev FLOAT, 
	mt_salindex110_wind_speed_speedstddev_1_min FLOAT, 
	mt_salindex110_wind_speed_speedstddev_1_max FLOAT, 
	mt_salindex110_wind_speed_speedstddev_2_mean FLOAT, 
	mt_salindex110_wind_speed_speedstddev_2_stddev FLOAT, 
	mt_salindex110_wind_speed_speedstddev_2_min FLOAT, 
	mt_salindex110_wind_speed_speedstddev_2_max FLOAT, 
	mt_salindex110_wind_speed_magnitude_mean FLOAT, 
	mt_salindex110_wind_speed_magnitude_stddev FLOAT, 
	mt_salindex110_wind_speed_magnitude_min FLOAT, 
	mt_salindex110_wind_speed_magnitude_max FLOAT, 
	mt_salindex110_wind_speed_maxmagnitude_mean FLOAT, 
	mt_salindex110_wind_speed_maxmagnitude_stddev FLOAT, 
	mt_salindex110_wind_speed_maxmagnitude_min FLOAT, 
	mt_salindex110_wind_speed_maxmagnitude_max FLOAT, 
	mt_salindex301_airflow_speed_mean FLOAT, 
	mt_salindex301_airflow_speed_stddev FLOAT, 
	mt_salindex301_airflow_speed_min FLOAT, 
	mt_salindex301_airflow_speed_max FLOAT, 
	mt_salindex301_airflow_speedstddev_mean FLOAT, 
	mt_salindex301_airflow_speedstddev_stddev FLOAT, 
	mt_salindex301_airflow_speedstddev_min FLOAT, 
	mt_salindex301_airflow_speedstddev_max FLOAT, 
	mt_salindex301_airflow_direction_mean FLOAT, 
	mt_salindex301_airflow_direction_stddev FLOAT, 
	mt_salindex301_airflow_direction_min FLOAT, 
	mt_salindex301_airflow_direction_max FLOAT, 
	mt_salindex1_temperature_0_mean FLOAT, 
	mt_salindex1_temperature_0_stddev FLOAT, 
	mt_salindex1_temperature_0_min FLOAT, 
	mt_salindex1_temperature_1_mean FLOAT, 
	mt_salindex1_temperature_0_max FLOAT, 
	mt_salindex1_temperature_1_stddev FLOAT, 
	mt_salindex1_temperature_1_min FLOAT, 
	mt_salindex1_temperature_1_max FLOAT, 
	mt_salindex1_temperature_2_mean FLOAT, 
	mt_salindex1_temperature_2_stddev FLOAT, 
	mt_salindex1_temperature_2_min FLOAT, 
	mt_salindex1_temperature_2_max FLOAT, 
	mt_salindex1_temperature_3_mean FLOAT, 
	mt_salindex1_temperature_3_stddev FLOAT, 
	mt_salindex1_temperature_3_min FLOAT, 
	mt_salindex1_temperature_3_max FLOAT, 
	mt_salindex1_temperature_4_mean FLOAT, 
	mt_salindex1_temperature_4_stddev FLOAT, 
	mt_salindex1_temperature_4_min FLOAT, 
	mt_salindex1_temperature_4_max FLOAT, 
	mt_salindex1_temperature_5_mean FLOAT, 
	mt_salindex1_temperature_5_stddev FLOAT, 
	mt_salindex1_temperature_5_min FLOAT, 
	mt_salindex1_temperature_5_max FLOAT, 
	mt_salindex1_temperature_6_mean FLOAT, 
	mt_salindex1_temperature_6_stddev FLOAT, 
	mt_salindex1_temperature_6_min FLOAT, 
	mt_salindex1_temperature_6_max FLOAT, 
	mt_salindex1_temperature_7_mean FLOAT, 
	mt_salindex1_temperature_7_stddev FLOAT, 
	mt_salindex1_temperature_7_min FLOAT, 
	mt_salindex1_temperature_7_max FLOAT, 
	mt_salindex101_temperature_0_mean FLOAT, 
	mt_salindex101_temperature_0_stddev FLOAT, 
	mt_salindex101_temperature_0_min FLOAT, 
	mt_salindex101_temperature_1_mean FLOAT, 
	mt_salindex101_temperature_0_max FLOAT, 
	mt_salindex101_temperature_1_stddev FLOAT, 
	mt_salindex101_temperature_1_min FLOAT, 
	mt_salindex101_temperature_1_max FLOAT, 
	mt_salindex101_temperature_2_mean FLOAT, 
	mt_salindex101_temperature_2_stddev FLOAT, 
	mt_salindex101_temperature_2_min FLOAT, 
	mt_salindex101_temperature_2_max FLOAT, 
	mt_salindex101_temperature_3_mean FLOAT, 
	mt_salindex101_temperature_3_stddev FLOAT, 
	mt_salindex101_temperature_3_min FLOAT, 
	mt_salindex101_temperature_3_max FLOAT, 
	mt_salindex101_temperature_4_mean FLOAT, 
	mt_salindex101_temperature_4_stddev FLOAT, 
	mt_salindex101_temperature_4_min FLOAT, 
	mt_salindex101_temperature_4_max FLOAT, 
	mt_salindex101_temperature_5_mean FLOAT, 
	mt_salindex101_temperature_5_stddev FLOAT, 
	mt_salindex101_temperature_5_min FLOAT, 
	mt_salindex101_temperature_5_max FLOAT, 
	mt_salindex101_temperature_6_mean FLOAT, 
	mt_salindex101_temperature_6_stddev FLOAT, 
	mt_salindex101_temperature_6_min FLOAT, 
	mt_salindex101_temperature_6_max FLOAT, 
	mt_salindex101_temperature_7_mean FLOAT, 
	mt_salindex101_temperature_7_stddev FLOAT, 
	mt_salindex101_temperature_7_min FLOAT, 
	mt_salindex101_temperature_7_max FLOAT, 
	mt_salindex102_temperature_0_mean FLOAT, 
	mt_salindex102_temperature_0_stddev FLOAT, 
	mt_salindex102_temperature_0_min FLOAT, 
	mt_salindex102_temperature_1_mean FLOAT, 
	mt_salindex102_temperature_0_max FLOAT, 
	mt_salindex102_temperature_1_stddev FLOAT, 
	mt_salindex102_temperature_1_min FLOAT, 
	mt_salindex102_temperature_1_max FLOAT, 
	mt_salindex102_temperature_2_mean FLOAT, 
	mt_salindex102_temperature_2_stddev FLOAT, 
	mt_salindex102_temperature_2_min FLOAT, 
	mt_salindex102_temperature_2_max FLOAT, 
	mt_salindex102_temperature_3_mean FLOAT, 
	mt_salindex102_temperature_3_stddev FLOAT, 
	mt_salindex102_temperature_3_min FLOAT, 
	mt_salindex102_temperature_3_max FLOAT, 
	mt_salindex102_temperature_4_mean FLOAT, 
	mt_salindex102_temperature_4_stddev FLOAT, 
	mt_salindex102_temperature_4_min FLOAT, 
	mt_salindex102_temperature_4_max FLOAT, 
	mt_salindex102_temperature_5_mean FLOAT, 
	mt_salindex102_temperature_5_stddev FLOAT, 
	mt_salindex102_temperature_5_min FLOAT, 
	mt_salindex102_temperature_5_max FLOAT, 
	mt_salindex102_temperature_6_mean FLOAT, 
	mt_salindex102_temperature_6_stddev FLOAT, 
	mt_salindex102_temperature_6_min FLOAT, 
	mt_salindex102_temperature_6_max FLOAT, 
	mt_salindex102_temperature_7_mean FLOAT, 
	mt_salindex102_temperature_7_stddev FLOAT, 
	mt_salindex102_temperature_7_min FLOAT, 
	mt_salindex102_temperature_7_max FLOAT, 
	mt_salindex103_temperature_0_mean FLOAT, 
	mt_salindex103_temperature_0_stddev FLOAT, 
	mt_salindex103_temperature_0_min FLOAT, 
	mt_salindex103_temperature_1_mean FLOAT, 
	mt_salindex103_temperature_0_max FLOAT, 
	mt_salindex103_temperature_1_stddev FLOAT, 
	mt_salindex103_temperature_1_min FLOAT, 
	mt_salindex103_temperature_1_max FLOAT, 
	mt_salindex103_temperature_2_mean FLOAT, 
	mt_salindex103_temperature_2_stddev FLOAT, 
	mt_salindex103_temperature_2_min FLOAT, 
	mt_salindex103_temperature_2_max FLOAT, 
	mt_salindex103_temperature_3_mean FLOAT, 
	mt_salindex103_temperature_3_stddev FLOAT, 
	mt_salindex103_temperature_3_min FLOAT, 
	mt_salindex103_temperature_3_max FLOAT, 
	mt_salindex103_temperature_4_mean FLOAT, 
	mt_salindex103_temperature_4_stddev FLOAT, 
	mt_salindex103_temperature_4_min FLOAT, 
	mt_salindex103_temperature_4_max FLOAT, 
	mt_salindex103_temperature_5_mean FLOAT, 
	mt_salindex103_temperature_5_stddev FLOAT, 
	mt_salindex103_temperature_5_min FLOAT, 
	mt_salindex103_temperature_5_max FLOAT, 
	mt_salindex103_temperature_6_mean FLOAT, 
	mt_salindex103_temperature_6_stddev FLOAT, 
	mt_salindex103_temperature_6_min FLOAT, 
	mt_salindex103_temperature_6_max FLOAT, 
	mt_salindex103_temperature_7_mean FLOAT, 
	mt_salindex103_temperature_7_stddev FLOAT, 
	mt_salindex103_temperature_7_min FLOAT, 
	mt_salindex103_temperature_7_max FLOAT, 
	mt_salindex106_temperature_0_mean FLOAT, 
	mt_salindex106_temperature_0_stddev FLOAT, 
	mt_salindex106_temperature_0_min FLOAT, 
	mt_salindex106_temperature_1_mean FLOAT, 
	mt_salindex106_temperature_0_max FLOAT, 
	mt_salindex106_temperature_1_stddev FLOAT, 
	mt_salindex106_temperature_1_min FLOAT, 
	mt_salindex106_temperature_1_max FLOAT, 
	mt_salindex106_temperature_2_mean FLOAT, 
	mt_salindex106_temperature_2_stddev FLOAT, 
	mt_salindex106_temperature_2_min FLOAT, 
	mt_salindex106_temperature_2_max FLOAT, 
	mt_salindex106_temperature_3_mean FLOAT, 
	mt_salindex106_temperature_3_stddev FLOAT, 
	mt_salindex106_temperature_3_min FLOAT, 
	mt_salindex106_temperature_3_max FLOAT, 
	mt_salindex106_temperature_4_mean FLOAT, 
	mt_salindex106_temperature_4_stddev FLOAT, 
	mt_salindex106_temperature_4_min FLOAT, 
	mt_salindex106_temperature_4_max FLOAT, 
	mt_salindex106_temperature_5_mean FLOAT, 
	mt_salindex106_temperature_5_stddev FLOAT, 
	mt_salindex106_temperature_5_min FLOAT, 
	mt_salindex106_temperature_5_max FLOAT, 
	mt_salindex106_temperature_6_mean FLOAT, 
	mt_salindex106_temperature_6_stddev FLOAT, 
	mt_salindex106_temperature_6_min FLOAT, 
	mt_salindex106_temperature_6_max FLOAT, 
	mt_salindex106_temperature_7_mean FLOAT, 
	mt_salindex106_temperature_7_stddev FLOAT, 
	mt_salindex106_temperature_7_min FLOAT, 
	mt_salindex106_temperature_7_max FLOAT, 
	mt_salindex107_temperature_0_mean FLOAT, 
	mt_salindex107_temperature_0_stddev FLOAT, 
	mt_salindex107_temperature_0_min FLOAT, 
	mt_salindex107_temperature_1_mean FLOAT, 
	mt_salindex107_temperature_0_max FLOAT, 
	mt_salindex107_temperature_1_stddev FLOAT, 
	mt_salindex107_temperature_1_min FLOAT, 
	mt_salindex107_temperature_1_max FLOAT, 
	mt_salindex107_temperature_2_mean FLOAT, 
	mt_salindex107_temperature_2_stddev FLOAT, 
	mt_salindex107_temperature_2_min FLOAT, 
	mt_salindex107_temperature_2_max FLOAT, 
	mt_salindex107_temperature_3_mean FLOAT, 
	mt_salindex107_temperature_3_stddev FLOAT, 
	mt_salindex107_temperature_3_min FLOAT, 
	mt_salindex107_temperature_3_max FLOAT, 
	mt_salindex107_temperature_4_mean FLOAT, 
	mt_salindex107_temperature_4_stddev FLOAT, 
	mt_salindex107_temperature_4_min FLOAT, 
	mt_salindex107_temperature_4_max FLOAT, 
	mt_salindex107_temperature_5_mean FLOAT, 
	mt_salindex107_temperature_5_stddev FLOAT, 
	mt_salindex107_temperature_5_min FLOAT, 
	mt_salindex107_temperature_5_max FLOAT, 
	mt_salindex107_temperature_6_mean FLOAT, 
	mt_salindex107_temperature_6_stddev FLOAT, 
	mt_salindex107_temperature_6_min FLOAT, 
	mt_salindex107_temperature_6_max FLOAT, 
	mt_salindex107_temperature_7_mean FLOAT, 
	mt_salindex107_temperature_7_stddev FLOAT, 
	mt_salindex107_temperature_7_min FLOAT, 
	mt_salindex107_temperature_7_max FLOAT, 
	mt_salindex108_temperature_0_mean FLOAT, 
	mt_salindex108_temperature_0_stddev FLOAT, 
	mt_salindex108_temperature_0_min FLOAT, 
	mt_salindex108_temperature_1_mean FLOAT, 
	mt_salindex108_temperature_0_max FLOAT, 
	mt_salindex108_temperature_1_stddev FLOAT, 
	mt_salindex108_temperature_1_min FLOAT, 
	mt_salindex108_temperature_1_max FLOAT, 
	mt_salindex108_temperature_2_mean FLOAT, 
	mt_salindex108_temperature_2_stddev FLOAT, 
	mt_salindex108_temperature_2_min FLOAT, 
	mt_salindex108_temperature_2_max FLOAT, 
	mt_salindex108_temperature_3_mean FLOAT, 
	mt_salindex108_temperature_3_stddev FLOAT, 
	mt_salindex108_temperature_3_min FLOAT, 
	mt_salindex108_temperature_3_max FLOAT, 
	mt_salindex108_temperature_4_mean FLOAT, 
	mt_salindex108_temperature_4_stddev FLOAT, 
	mt_salindex108_temperature_4_min FLOAT, 
	mt_salindex108_temperature_4_max FLOAT, 
	mt_salindex108_temperature_5_mean FLOAT, 
	mt_salindex108_temperature_5_stddev FLOAT, 
	mt_salindex108_temperature_5_min FLOAT, 
	mt_salindex108_temperature_5_max FLOAT, 
	mt_salindex108_temperature_6_mean FLOAT, 
	mt_salindex108_temperature_6_stddev FLOAT, 
	mt_salindex108_temperature_6_min FLOAT, 
	mt_salindex108_temperature_6_max FLOAT, 
	mt_salindex108_temperature_7_mean FLOAT, 
	mt_salindex108_temperature_7_stddev FLOAT, 
	mt_salindex108_temperature_7_min FLOAT, 
	mt_salindex108_temperature_7_max FLOAT, 
	mt_salindex301_temperature_0_mean FLOAT, 
	mt_salindex301_temperature_0_stddev FLOAT, 
	mt_salindex301_temperature_0_min FLOAT, 
	mt_salindex301_temperature_1_mean FLOAT, 
	mt_salindex301_temperature_0_max FLOAT, 
	mt_salindex301_temperature_1_stddev FLOAT, 
	mt_salindex301_temperature_1_min FLOAT, 
	mt_salindex301_temperature_1_max FLOAT, 
	mt_salindex301_temperature_2_mean FLOAT, 
	mt_salindex301_temperature_2_stddev FLOAT, 
	mt_salindex301_temperature_2_min FLOAT, 
	mt_salindex301_temperature_2_max FLOAT, 
	mt_salindex301_temperature_3_mean FLOAT, 
	mt_salindex301_temperature_3_stddev FLOAT, 
	mt_salindex301_temperature_3_min FLOAT, 
	mt_salindex301_temperature_3_max FLOAT, 
	mt_salindex301_temperature_4_mean FLOAT, 
	mt_salindex301_temperature_4_stddev FLOAT, 
	mt_salindex301_temperature_4_min FLOAT, 
	mt_salindex301_temperature_4_max FLOAT, 
	mt_salindex301_temperature_5_mean FLOAT, 
	mt_salindex301_temperature_5_stddev FLOAT, 
	mt_salindex301_temperature_5_min FLOAT, 
	mt_salindex301_temperature_5_max FLOAT, 
	mt_salindex301_temperature_6_mean FLOAT, 
	mt_salindex301_temperature_6_stddev FLOAT, 
	mt_salindex301_temperature_6_min FLOAT, 
	mt_salindex301_temperature_6_max FLOAT, 
	mt_salindex301_temperature_7_mean FLOAT, 
	mt_salindex301_temperature_7_stddev FLOAT, 
	mt_salindex301_temperature_7_min FLOAT, 
	mt_salindex301_temperature_7_max FLOAT, 
	mt_dimm_fwhm_mean FLOAT, 
	mt_azimuth_encoder_absolute_position_0_mean FLOAT, 
	mt_azimuth_encoder_absolute_position_1_mean FLOAT, 
	mt_azimuth_encoder_absolute_position_2_mean FLOAT, 
	mt_azimuth_encoder_absolute_position_3_mean FLOAT, 
	mt_elevation_encoder_absolute_position_0_mean FLOAT, 
	mt_elevation_encoder_absolute_position_1_mean FLOAT, 
	mt_elevation_encoder_absolute_position_2_mean FLOAT, 
	mt_elevation_encoder_absolute_position_3_mean FLOAT, 
	mt_hexapod_uncompensated_position_u_mean FLOAT, 
	mt_hexapod_uncompensated_position_u_max FLOAT, 
	mt_hexapod_uncompensated_position_u_min FLOAT, 
	mt_hexapod_uncompensated_position_v_mean FLOAT, 
	mt_hexapod_uncompensated_position_v_max FLOAT, 
	mt_hexapod_uncompensated_position_v_min FLOAT, 
	mt_hexapod_uncompensated_position_w_mean FLOAT, 
	mt_hexapod_uncompensated_position_w_max FLOAT, 
	mt_hexapod_uncompensated_position_w_min FLOAT, 
	mt_hexapod_uncompensated_position_x_mean FLOAT, 
	mt_hexapod_uncompensated_position_x_max FLOAT, 
	mt_hexapod_uncompensated_position_x_min FLOAT, 
	mt_hexapod_uncompensated_position_y_mean FLOAT, 
	mt_hexapod_uncompensated_position_y_max FLOAT, 
	mt_hexapod_uncompensated_position_y_min FLOAT, 
	mt_hexapod_uncompensated_position_z_mean FLOAT, 
	mt_hexapod_uncompensated_position_z_max FLOAT, 
	mt_hexapod_uncompensated_position_z_min FLOAT, 
	mt_salindex111_dewpoint_mean FLOAT, 
	mt_salindex112_dewpoint_mean FLOAT, 
	mt_salindex113_dewpoint_mean FLOAT, 
	mt_salindex111_relativehumidity_mean FLOAT, 
	mt_salindex112_relativehumidity_mean FLOAT, 
	mt_salindex113_relativehumidity_mean FLOAT, 
	mt_salindex113_pressure_0_mean FLOAT, 
	mt_salindex113_pressure_1_mean FLOAT, 
	mt_salindex301_pressure_0_mean FLOAT, 
	mt_salindex301_pressure_1_mean FLOAT, 
	mt_pointing_mount_position_ra_mean FLOAT, 
	mt_pointing_mount_position_ra_stddev FLOAT, 
	mt_pointing_mount_position_dec_mean FLOAT, 
	mt_pointing_mount_position_dec_stddev FLOAT, 
	mt_pointing_mount_position_sky_angle_mean FLOAT, 
	mt_pointing_mount_position_sky_angle_stddev FLOAT, 
	mt_pointing_mount_position_rotator_mean FLOAT, 
	mt_pointing_mount_position_rotator_stddev FLOAT, 
	camera_hexapod_aos_corrections_u FLOAT, 
	camera_hexapod_aos_corrections_v FLOAT, 
	camera_hexapod_aos_corrections_w FLOAT, 
	camera_hexapod_aos_corrections_x FLOAT, 
	camera_hexapod_aos_corrections_y FLOAT, 
	camera_hexapod_aos_corrections_z FLOAT, 
	m2_hexapod_aos_corrections_u FLOAT, 
	m2_hexapod_aos_corrections_v FLOAT, 
	m2_hexapod_aos_corrections_w FLOAT, 
	m2_hexapod_aos_corrections_x FLOAT, 
	m2_hexapod_aos_corrections_y FLOAT, 
	m2_hexapod_aos_corrections_z FLOAT, 
	m2_stress FLOAT, 
	m1m3_stress FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_0_mean" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_0_stddev" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_0_max" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_0_min" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_1_mean" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_1_stddev" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_1_max" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_1_min" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_2_mean" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_2_stddev" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_2_max" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_2_min" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_3_mean" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_3_stddev" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_3_max" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_3_min" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_4_mean" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_4_stddev" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_4_max" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_4_min" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_5_mean" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_5_stddev" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_5_max" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_5_min" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_6_mean" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_6_stddev" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_6_max" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_6_min" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_7_mean" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_7_stddev" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_7_max" FLOAT, 
	"mt_salIndex104_m1m3_accelerometer_7_min" FLOAT, 
	"mt_salIndex104_m1m3_angular_acceleration_x_mean" FLOAT, 
	"mt_salIndex104_m1m3_angular_acceleration_x_stddev" FLOAT, 
	"mt_salIndex104_m1m3_angular_acceleration_x_max" FLOAT, 
	"mt_salIndex104_m1m3_angular_acceleration_x_min" FLOAT, 
	"mt_salIndex104_m1m3_angular_acceleration_y_mean" FLOAT, 
	"mt_salIndex104_m1m3_angular_acceleration_y_stddev" FLOAT, 
	"mt_salIndex104_m1m3_angular_acceleration_y_max" FLOAT, 
	"mt_salIndex104_m1m3_angular_acceleration_y_min" FLOAT, 
	"mt_salIndex104_m1m3_angular_acceleration_z_mean" FLOAT, 
	"mt_salIndex104_m1m3_angular_acceleration_z_stddev" FLOAT, 
	"mt_salIndex104_m1m3_angular_acceleration_z_max" FLOAT, 
	"mt_salIndex104_m1m3_angular_acceleration_z_min" FLOAT, 
	PRIMARY KEY (visit_id, instrument), 
	CONSTRAINT un_visit_id_instrument UNIQUE (visit_id, instrument)
)

;
COMMENT ON TABLE cdb_lsstcomcamsim.visit1_efd IS 'Transformed EFD topics by visit.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.visit_id IS 'Visit unique ID.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.created_at IS 'Timestamp when the record was created, default is the current timestamp';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.instrument IS 'Instrument name.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_sonic_temperature_mean IS 'Median sonic temperature (air temperature measured sonically). Sonic temperature has poor absolute accuracy (it can be off by several degrees) but good time resolution.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_sonic_temperature_stddev IS 'Median sonic temperature (air temperature measured sonically). Sonic temperature has poor absolute accuracy (it can be off by several degrees) but good time resolution.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.at_salindex110_sonic_temperature_stddev_mean IS 'Standard devation of sonic temperature (air temperature measured sonically) estimated from quartiles.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.at_salindex110_sonic_temperature_stddev_stddev IS 'Standard devation of sonic temperature (air temperature measured sonically) estimated from quartiles.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_wind_speed_0_mean IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 0 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_wind_speed_0_stddev IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 0 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_wind_speed_0_min IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 0 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_wind_speed_0_max IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 0 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_wind_speed_1_mean IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 1 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_wind_speed_1_stddev IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 1 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_wind_speed_1_min IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 1 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_wind_speed_1_max IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 1 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_wind_speed_2_mean IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 2 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_wind_speed_2_stddev IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 2 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_wind_speed_2_min IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 2 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_wind_speed_2_max IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 2 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_wind_speed_speedstddev_0_mean IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 0 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_wind_speed_speedstddev_0_stddev IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 0 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_wind_speed_speedstddev_0_min IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 0 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_wind_speed_speedstddev_0_max IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 0 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_wind_speed_speedstddev_1_mean IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 1 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_wind_speed_speedstddev_1_stddev IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 1 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_wind_speed_speedstddev_1_min IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 1 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_wind_speed_speedstddev_1_max IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 1 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_wind_speed_speedstddev_2_mean IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 2 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_wind_speed_speedstddev_2_stddev IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 2 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_wind_speed_speedstddev_2_min IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 2 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_wind_speed_speedstddev_2_max IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 2 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_wind_speed_magnitude_mean IS 'Median wind speed magnitude in TMA-GillLabJack01 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_wind_speed_magnitude_stddev IS 'Median wind speed magnitude in TMA-GillLabJack01 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_wind_speed_magnitude_min IS 'Median wind speed magnitude in TMA-GillLabJack01 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_wind_speed_magnitude_max IS 'Median wind speed magnitude in TMA-GillLabJack01 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_wind_speed_maxmagnitude_mean IS 'Maximum wind speed magnitude in TMA-GillLabJack01 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_wind_speed_maxmagnitude_stddev IS 'Maximum wind speed magnitude in TMA-GillLabJack01 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_wind_speed_maxmagnitude_min IS 'Maximum wind speed magnitude in TMA-GillLabJack01 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex110_wind_speed_maxmagnitude_max IS 'Maximum wind speed magnitude in TMA-GillLabJack01 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_airflow_speed_mean IS 'Median (mean for some sensors) wind speed in XX (salIndex 301)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_airflow_speed_stddev IS 'Median (mean for some sensors) wind speed in XX (salIndex 301)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_airflow_speed_min IS 'Median (mean for some sensors) wind speed in XX (salIndex 301)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_airflow_speed_max IS 'Median (mean for some sensors) wind speed in XX (salIndex 301)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_airflow_speedstddev_mean IS 'Standard deviation of wind speed estimated from quartiles in XX (salIndex 301). Not available for all sensor types.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_airflow_speedstddev_stddev IS 'Standard deviation of wind speed estimated from quartiles in XX (salIndex 301). Not available for all sensor types.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_airflow_speedstddev_min IS 'Standard deviation of wind speed estimated from quartiles in XX (salIndex 301). Not available for all sensor types.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_airflow_speedstddev_max IS 'Standard deviation of wind speed estimated from quartiles in XX (salIndex 301). Not available for all sensor types.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_airflow_direction_mean IS 'Median (mean for some sensors) wind speed in XX (salIndex 301)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_airflow_direction_stddev IS 'Median (mean for some sensors) wind speed in XX (salIndex 301)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_airflow_direction_min IS 'Median (mean for some sensors) wind speed in XX (salIndex 301)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_airflow_direction_max IS 'Median (mean for some sensors) wind speed in XX (salIndex 301)';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex1_temperature_0_mean IS 'MTCameraAssembly-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex1_temperature_0_stddev IS 'MTCameraAssembly-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex1_temperature_0_min IS 'MTCameraAssembly-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex1_temperature_1_mean IS 'MTCameraAssembly-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex1_temperature_0_max IS 'MTCameraAssembly-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex1_temperature_1_stddev IS 'MTCameraAssembly-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex1_temperature_1_min IS 'MTCameraAssembly-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex1_temperature_1_max IS 'MTCameraAssembly-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex1_temperature_2_mean IS 'MTCameraAssembly-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex1_temperature_2_stddev IS 'MTCameraAssembly-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex1_temperature_2_min IS 'MTCameraAssembly-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex1_temperature_2_max IS 'MTCameraAssembly-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex1_temperature_3_mean IS 'MTCameraAssembly-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex1_temperature_3_stddev IS 'MTCameraAssembly-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex1_temperature_3_min IS 'MTCameraAssembly-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex1_temperature_3_max IS 'MTCameraAssembly-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex1_temperature_4_mean IS 'MTCameraAssembly-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex1_temperature_4_stddev IS 'MTCameraAssembly-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex1_temperature_4_min IS 'MTCameraAssembly-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex1_temperature_4_max IS 'MTCameraAssembly-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex1_temperature_5_mean IS 'MTCameraAssembly-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex1_temperature_5_stddev IS 'MTCameraAssembly-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex1_temperature_5_min IS 'MTCameraAssembly-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex1_temperature_5_max IS 'MTCameraAssembly-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex1_temperature_6_mean IS 'MTCameraAssembly-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex1_temperature_6_stddev IS 'MTCameraAssembly-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex1_temperature_6_min IS 'MTCameraAssembly-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex1_temperature_6_max IS 'MTCameraAssembly-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex1_temperature_7_mean IS 'MTCameraAssembly-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex1_temperature_7_stddev IS 'MTCameraAssembly-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex1_temperature_7_min IS 'MTCameraAssembly-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex1_temperature_7_max IS 'MTCameraAssembly-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex101_temperature_0_mean IS 'MTCameraAssembly-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex101_temperature_0_stddev IS 'MTCameraAssembly-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex101_temperature_0_min IS 'MTCameraAssembly-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex101_temperature_1_mean IS 'MTCameraAssembly-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex101_temperature_0_max IS 'MTCameraAssembly-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex101_temperature_1_stddev IS 'MTCameraAssembly-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex101_temperature_1_min IS 'MTCameraAssembly-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex101_temperature_1_max IS 'MTCameraAssembly-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex101_temperature_2_mean IS 'MTCameraAssembly-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex101_temperature_2_stddev IS 'MTCameraAssembly-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex101_temperature_2_min IS 'MTCameraAssembly-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex101_temperature_2_max IS 'MTCameraAssembly-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex101_temperature_3_mean IS 'MTCameraAssembly-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex101_temperature_3_stddev IS 'MTCameraAssembly-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex101_temperature_3_min IS 'MTCameraAssembly-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex101_temperature_3_max IS 'MTCameraAssembly-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex101_temperature_4_mean IS 'MTCameraAssembly-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex101_temperature_4_stddev IS 'MTCameraAssembly-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex101_temperature_4_min IS 'MTCameraAssembly-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex101_temperature_4_max IS 'MTCameraAssembly-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex101_temperature_5_mean IS 'MTCameraAssembly-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex101_temperature_5_stddev IS 'MTCameraAssembly-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex101_temperature_5_min IS 'MTCameraAssembly-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex101_temperature_5_max IS 'MTCameraAssembly-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex101_temperature_6_mean IS 'MTCameraAssembly-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex101_temperature_6_stddev IS 'MTCameraAssembly-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex101_temperature_6_min IS 'MTCameraAssembly-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex101_temperature_6_max IS 'MTCameraAssembly-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex101_temperature_7_mean IS 'MTCameraAssembly-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex101_temperature_7_stddev IS 'MTCameraAssembly-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex101_temperature_7_min IS 'MTCameraAssembly-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex101_temperature_7_max IS 'MTCameraAssembly-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex102_temperature_0_mean IS 'XX temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex102_temperature_0_stddev IS 'XX temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex102_temperature_0_min IS 'XX temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex102_temperature_1_mean IS 'XX temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex102_temperature_0_max IS 'XX temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex102_temperature_1_stddev IS 'XX temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex102_temperature_1_min IS 'XX temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex102_temperature_1_max IS 'XX temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex102_temperature_2_mean IS 'XX temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex102_temperature_2_stddev IS 'XX temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex102_temperature_2_min IS 'XX temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex102_temperature_2_max IS 'XX temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex102_temperature_3_mean IS 'XX temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex102_temperature_3_stddev IS 'XX temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex102_temperature_3_min IS 'XX temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex102_temperature_3_max IS 'XX temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex102_temperature_4_mean IS 'XX temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex102_temperature_4_stddev IS 'XX temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex102_temperature_4_min IS 'XX temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex102_temperature_4_max IS 'XX temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex102_temperature_5_mean IS 'XX temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex102_temperature_5_stddev IS 'XX temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex102_temperature_5_min IS 'XX temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex102_temperature_5_max IS 'XX temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex102_temperature_6_mean IS 'XX temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex102_temperature_6_stddev IS 'XX temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex102_temperature_6_min IS 'XX temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex102_temperature_6_max IS 'XX temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex102_temperature_7_mean IS 'XX temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex102_temperature_7_stddev IS 'XX temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex102_temperature_7_min IS 'XX temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex102_temperature_7_max IS 'XX temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex103_temperature_0_mean IS 'XX temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex103_temperature_0_stddev IS 'XX temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex103_temperature_0_min IS 'XX temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex103_temperature_1_mean IS 'XX temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex103_temperature_0_max IS 'XX temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex103_temperature_1_stddev IS 'XX temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex103_temperature_1_min IS 'XX temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex103_temperature_1_max IS 'XX temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex103_temperature_2_mean IS 'XX temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex103_temperature_2_stddev IS 'XX temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex103_temperature_2_min IS 'XX temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex103_temperature_2_max IS 'XX temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex103_temperature_3_mean IS 'XX temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex103_temperature_3_stddev IS 'XX temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex103_temperature_3_min IS 'XX temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex103_temperature_3_max IS 'XX temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex103_temperature_4_mean IS 'XX temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex103_temperature_4_stddev IS 'XX temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex103_temperature_4_min IS 'XX temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex103_temperature_4_max IS 'XX temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex103_temperature_5_mean IS 'XX temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex103_temperature_5_stddev IS 'XX temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex103_temperature_5_min IS 'XX temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex103_temperature_5_max IS 'XX temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex103_temperature_6_mean IS 'XX temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex103_temperature_6_stddev IS 'XX temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex103_temperature_6_min IS 'XX temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex103_temperature_6_max IS 'XX temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex103_temperature_7_mean IS 'XX temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex103_temperature_7_stddev IS 'XX temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex103_temperature_7_min IS 'XX temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex103_temperature_7_max IS 'XX temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex106_temperature_0_mean IS 'M2-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex106_temperature_0_stddev IS 'M2-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex106_temperature_0_min IS 'M2-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex106_temperature_1_mean IS 'M2-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex106_temperature_0_max IS 'M2-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex106_temperature_1_stddev IS 'M2-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex106_temperature_1_min IS 'M2-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex106_temperature_1_max IS 'M2-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex106_temperature_2_mean IS 'M2-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex106_temperature_2_stddev IS 'M2-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex106_temperature_2_min IS 'M2-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex106_temperature_2_max IS 'M2-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex106_temperature_3_mean IS 'M2-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex106_temperature_3_stddev IS 'M2-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex106_temperature_3_min IS 'M2-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex106_temperature_3_max IS 'M2-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex106_temperature_4_mean IS 'M2-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex106_temperature_4_stddev IS 'M2-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex106_temperature_4_min IS 'M2-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex106_temperature_4_max IS 'M2-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex106_temperature_5_mean IS 'M2-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex106_temperature_5_stddev IS 'M2-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex106_temperature_5_min IS 'M2-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex106_temperature_5_max IS 'M2-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex106_temperature_6_mean IS 'M2-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex106_temperature_6_stddev IS 'M2-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex106_temperature_6_min IS 'M2-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex106_temperature_6_max IS 'M2-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex106_temperature_7_mean IS 'M2-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex106_temperature_7_stddev IS 'M2-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex106_temperature_7_min IS 'M2-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex106_temperature_7_max IS 'M2-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex107_temperature_0_mean IS 'Laser-ESS01, Laser-ESS02 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex107_temperature_0_stddev IS 'Laser-ESS01, Laser-ESS02 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex107_temperature_0_min IS 'Laser-ESS01, Laser-ESS02 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex107_temperature_1_mean IS 'Laser-ESS01, Laser-ESS02 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex107_temperature_0_max IS 'Laser-ESS01, Laser-ESS02 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex107_temperature_1_stddev IS 'Laser-ESS01, Laser-ESS02 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex107_temperature_1_min IS 'Laser-ESS01, Laser-ESS02 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex107_temperature_1_max IS 'Laser-ESS01, Laser-ESS02 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex107_temperature_2_mean IS 'Laser-ESS01, Laser-ESS02 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex107_temperature_2_stddev IS 'Laser-ESS01, Laser-ESS02 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex107_temperature_2_min IS 'Laser-ESS01, Laser-ESS02 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex107_temperature_2_max IS 'Laser-ESS01, Laser-ESS02 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex107_temperature_3_mean IS 'Laser-ESS01, Laser-ESS02 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex107_temperature_3_stddev IS 'Laser-ESS01, Laser-ESS02 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex107_temperature_3_min IS 'Laser-ESS01, Laser-ESS02 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex107_temperature_3_max IS 'Laser-ESS01, Laser-ESS02 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex107_temperature_4_mean IS 'Laser-ESS01, Laser-ESS02 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex107_temperature_4_stddev IS 'Laser-ESS01, Laser-ESS02 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex107_temperature_4_min IS 'Laser-ESS01, Laser-ESS02 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex107_temperature_4_max IS 'Laser-ESS01, Laser-ESS02 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex107_temperature_5_mean IS 'Laser-ESS01, Laser-ESS02 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex107_temperature_5_stddev IS 'Laser-ESS01, Laser-ESS02 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex107_temperature_5_min IS 'Laser-ESS01, Laser-ESS02 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex107_temperature_5_max IS 'Laser-ESS01, Laser-ESS02 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex107_temperature_6_mean IS 'Laser-ESS01, Laser-ESS02 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex107_temperature_6_stddev IS 'Laser-ESS01, Laser-ESS02 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex107_temperature_6_min IS 'Laser-ESS01, Laser-ESS02 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex107_temperature_6_max IS 'Laser-ESS01, Laser-ESS02 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex107_temperature_7_mean IS 'Laser-ESS01, Laser-ESS02 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex107_temperature_7_stddev IS 'Laser-ESS01, Laser-ESS02 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex107_temperature_7_min IS 'Laser-ESS01, Laser-ESS02 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex107_temperature_7_max IS 'Laser-ESS01, Laser-ESS02 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex108_temperature_0_mean IS 'CBP-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex108_temperature_0_stddev IS 'CBP-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex108_temperature_0_min IS 'CBP-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex108_temperature_1_mean IS 'CBP-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex108_temperature_0_max IS 'CBP-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex108_temperature_1_stddev IS 'CBP-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex108_temperature_1_min IS 'CBP-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex108_temperature_1_max IS 'CBP-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex108_temperature_2_mean IS 'CBP-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex108_temperature_2_stddev IS 'CBP-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex108_temperature_2_min IS 'CBP-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex108_temperature_2_max IS 'CBP-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex108_temperature_3_mean IS 'CBP-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex108_temperature_3_stddev IS 'CBP-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex108_temperature_3_min IS 'CBP-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex108_temperature_3_max IS 'CBP-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex108_temperature_4_mean IS 'CBP-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex108_temperature_4_stddev IS 'CBP-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex108_temperature_4_min IS 'CBP-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex108_temperature_4_max IS 'CBP-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex108_temperature_5_mean IS 'CBP-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex108_temperature_5_stddev IS 'CBP-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex108_temperature_5_min IS 'CBP-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex108_temperature_5_max IS 'CBP-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex108_temperature_6_mean IS 'CBP-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex108_temperature_6_stddev IS 'CBP-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex108_temperature_6_min IS 'CBP-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex108_temperature_6_max IS 'CBP-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex108_temperature_7_mean IS 'CBP-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex108_temperature_7_stddev IS 'CBP-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex108_temperature_7_min IS 'CBP-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex108_temperature_7_max IS 'CBP-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_temperature_0_mean IS 'Weather tower air temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_temperature_0_stddev IS 'Weather tower air temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_temperature_0_min IS 'Weather tower air temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_temperature_1_mean IS 'Weather tower air temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_temperature_0_max IS 'Weather tower air temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_temperature_1_stddev IS 'Weather tower air temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_temperature_1_min IS 'Weather tower air temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_temperature_1_max IS 'Weather tower air temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_temperature_2_mean IS 'Weather tower air temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_temperature_2_stddev IS 'Weather tower air temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_temperature_2_min IS 'Weather tower air temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_temperature_2_max IS 'Weather tower air temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_temperature_3_mean IS 'Weather tower air temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_temperature_3_stddev IS 'Weather tower air temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_temperature_3_min IS 'Weather tower air temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_temperature_3_max IS 'Weather tower air temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_temperature_4_mean IS 'Weather tower air temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_temperature_4_stddev IS 'Weather tower air temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_temperature_4_min IS 'Weather tower air temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_temperature_4_max IS 'Weather tower air temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_temperature_5_mean IS 'Weather tower air temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_temperature_5_stddev IS 'Weather tower air temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_temperature_5_min IS 'Weather tower air temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_temperature_5_max IS 'Weather tower air temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_temperature_6_mean IS 'Weather tower air temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_temperature_6_stddev IS 'Weather tower air temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_temperature_6_min IS 'Weather tower air temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_temperature_6_max IS 'Weather tower air temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_temperature_7_mean IS 'Weather tower air temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_temperature_7_stddev IS 'Weather tower air temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_temperature_7_min IS 'Weather tower air temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_temperature_7_max IS 'Weather tower air temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_dimm_fwhm_mean IS 'Combined full width half maximum';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_azimuth_encoder_absolute_position_0_mean IS 'Azimuth absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_azimuth_encoder_absolute_position_1_mean IS 'Azimuth absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_azimuth_encoder_absolute_position_2_mean IS 'Azimuth absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_azimuth_encoder_absolute_position_3_mean IS 'Azimuth absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_elevation_encoder_absolute_position_0_mean IS 'Elevation absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_elevation_encoder_absolute_position_1_mean IS 'Elevation absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_elevation_encoder_absolute_position_2_mean IS 'Elevation absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_elevation_encoder_absolute_position_3_mean IS 'Elevation absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_hexapod_uncompensated_position_u_mean IS 'U angle.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_hexapod_uncompensated_position_u_max IS 'U angle.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_hexapod_uncompensated_position_u_min IS 'U angle.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_hexapod_uncompensated_position_v_mean IS 'V angle.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_hexapod_uncompensated_position_v_max IS 'V angle.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_hexapod_uncompensated_position_v_min IS 'V angle.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_hexapod_uncompensated_position_w_mean IS 'W angle.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_hexapod_uncompensated_position_w_max IS 'W angle.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_hexapod_uncompensated_position_w_min IS 'W angle.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_hexapod_uncompensated_position_x_mean IS 'X position.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_hexapod_uncompensated_position_x_max IS 'X position.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_hexapod_uncompensated_position_x_min IS 'X position.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_hexapod_uncompensated_position_y_mean IS 'Y position.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_hexapod_uncompensated_position_y_max IS 'Y position.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_hexapod_uncompensated_position_y_min IS 'Y position.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_hexapod_uncompensated_position_z_mean IS 'Z position.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_hexapod_uncompensated_position_z_max IS 'Z position.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_hexapod_uncompensated_position_z_min IS 'Z position.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex111_dewpoint_mean IS 'Dew point.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex112_dewpoint_mean IS 'Dew point.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex113_dewpoint_mean IS 'Dew point.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex111_relativehumidity_mean IS 'Relative humidity.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex112_relativehumidity_mean IS 'Relative humidity.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex113_relativehumidity_mean IS 'Relative humidity.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex113_pressure_0_mean IS 'The pressures.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex113_pressure_1_mean IS 'The pressures.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_pressure_0_mean IS 'The pressures.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_salindex301_pressure_1_mean IS 'The pressures.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_pointing_mount_position_ra_mean IS 'RA calculated from the azimuthActualPosition and elevationActualPosition.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_pointing_mount_position_ra_stddev IS 'RA calculated from the azimuthActualPosition and elevationActualPosition.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_pointing_mount_position_dec_mean IS 'Dec calculated from the azimuthActualPosition and elevationActualPosition.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_pointing_mount_position_dec_stddev IS 'Dec calculated from the azimuthActualPosition and elevationActualPosition.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_pointing_mount_position_sky_angle_mean IS 'Calculated sky angle.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_pointing_mount_position_sky_angle_stddev IS 'Calculated sky angle.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_pointing_mount_position_rotator_mean IS 'Rotator axis position reported by rotator component.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.mt_pointing_mount_position_rotator_stddev IS 'Rotator axis position reported by rotator component.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.camera_hexapod_aos_corrections_u IS 'U position offset.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.camera_hexapod_aos_corrections_v IS 'V position offset.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.camera_hexapod_aos_corrections_w IS 'W position offset.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.camera_hexapod_aos_corrections_x IS 'X position offset.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.camera_hexapod_aos_corrections_y IS 'Y position offset.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.camera_hexapod_aos_corrections_z IS 'Z position offset.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.m2_hexapod_aos_corrections_u IS 'U position offset.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.m2_hexapod_aos_corrections_v IS 'V position offset.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.m2_hexapod_aos_corrections_w IS 'W position offset.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.m2_hexapod_aos_corrections_x IS 'X position offset.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.m2_hexapod_aos_corrections_y IS 'Y position offset.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.m2_hexapod_aos_corrections_z IS 'Z position offset.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.m2_stress IS 'Calculate M2 stress computed RSS the stress contribution of each bending mode.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd.m1m3_stress IS 'Calculate M1M3 stress computed RSS the stress contribution of each bending mode.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_accelerometer_0_mean" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_accelerometer_0_stddev" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_accelerometer_0_max" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_accelerometer_0_min" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_accelerometer_1_mean" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_accelerometer_1_stddev" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_accelerometer_1_max" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_accelerometer_1_min" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_accelerometer_2_mean" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_accelerometer_2_stddev" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_accelerometer_2_max" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_accelerometer_2_min" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_accelerometer_3_mean" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_accelerometer_3_stddev" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_accelerometer_3_max" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_accelerometer_3_min" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_accelerometer_4_mean" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_accelerometer_4_stddev" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_accelerometer_4_max" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_accelerometer_4_min" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_accelerometer_5_mean" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_accelerometer_5_stddev" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_accelerometer_5_max" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_accelerometer_5_min" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_accelerometer_6_mean" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_accelerometer_6_stddev" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_accelerometer_6_max" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_accelerometer_6_min" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_accelerometer_7_mean" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_accelerometer_7_stddev" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_accelerometer_7_max" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_accelerometer_7_min" IS 'Accelerometer data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_angular_acceleration_x_mean" IS 'Accelerometer data angular Acceleration X.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_angular_acceleration_x_stddev" IS 'Accelerometer data angular Acceleration X.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_angular_acceleration_x_max" IS 'Accelerometer data angular Acceleration X.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_angular_acceleration_x_min" IS 'Accelerometer data angular Acceleration X.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_angular_acceleration_y_mean" IS 'Accelerometer data angular Acceleration Y.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_angular_acceleration_y_stddev" IS 'Accelerometer data angular Acceleration Y.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_angular_acceleration_y_max" IS 'Accelerometer data angular Acceleration Y.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_angular_acceleration_y_min" IS 'Accelerometer data angular Acceleration Y.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_angular_acceleration_z_mean" IS 'Accelerometer data angular Acceleration Z.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_angular_acceleration_z_stddev" IS 'Accelerometer data angular Acceleration Z.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_angular_acceleration_z_max" IS 'Accelerometer data angular Acceleration Z.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd."mt_salIndex104_m1m3_angular_acceleration_z_min" IS 'Accelerometer data angular Acceleration Z.';
COMMENT ON CONSTRAINT un_visit_id_instrument ON cdb_lsstcomcamsim.visit1_efd IS 'Ensure visit_id is unique.';

CREATE TABLE cdb_lsstcomcamsim.visit1_efd_unpivoted (
	visit_id INTEGER NOT NULL, 
	topic CHAR(255) NOT NULL, 
	"column" CHAR(255) NOT NULL, 
	value DOUBLE PRECISION, 
	created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (visit_id, topic, "column"), 
	CONSTRAINT un_visit_topic_column UNIQUE (visit_id, topic, "column")
)

;
COMMENT ON TABLE cdb_lsstcomcamsim.visit1_efd_unpivoted IS 'Unpivoted EFD visit data.';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd_unpivoted.visit_id IS 'Unique identifier for the visit';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd_unpivoted.topic IS 'Topic name for the unpivoted data';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd_unpivoted."column" IS 'Column name for the unpivoted data';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd_unpivoted.value IS 'Value corresponding to the parameter';
COMMENT ON COLUMN cdb_lsstcomcamsim.visit1_efd_unpivoted.created_at IS 'Timestamp when the record was created, default is the current timestamp';
COMMENT ON CONSTRAINT un_visit_topic_column ON cdb_lsstcomcamsim.visit1_efd_unpivoted IS 'Ensure the combination of visit_id, topic, and column is unique.';

CREATE TABLE cdb_lsstcomcamsim.transformed_efd_scheduler (
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
COMMENT ON TABLE cdb_lsstcomcamsim.transformed_efd_scheduler IS 'Transformed EFD scheduler.';
COMMENT ON COLUMN cdb_lsstcomcamsim.transformed_efd_scheduler.id IS 'Unique ID, auto-incremented';
COMMENT ON COLUMN cdb_lsstcomcamsim.transformed_efd_scheduler.start_time IS 'Start time of the transformation interval, must be provided';
COMMENT ON COLUMN cdb_lsstcomcamsim.transformed_efd_scheduler.end_time IS 'End time of the transformation interval, must be provided';
COMMENT ON COLUMN cdb_lsstcomcamsim.transformed_efd_scheduler.timewindow IS 'Time window used to expand start and end times by, in minutes';
COMMENT ON COLUMN cdb_lsstcomcamsim.transformed_efd_scheduler.status IS 'Status of the process, default is ''pending''';
COMMENT ON COLUMN cdb_lsstcomcamsim.transformed_efd_scheduler.process_start_time IS 'Timestamp when the process started';
COMMENT ON COLUMN cdb_lsstcomcamsim.transformed_efd_scheduler.process_end_time IS 'Timestamp when the process ended';
COMMENT ON COLUMN cdb_lsstcomcamsim.transformed_efd_scheduler.process_exec_time IS 'Execution time of the process in seconds, default is 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.transformed_efd_scheduler.exposures IS 'Number of exposures processed, default is 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.transformed_efd_scheduler.visits1 IS 'Number of visits recorded, default is 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.transformed_efd_scheduler.retries IS 'Number of retries attempted, default is 0';
COMMENT ON COLUMN cdb_lsstcomcamsim.transformed_efd_scheduler.error IS 'Error message, if any';
COMMENT ON COLUMN cdb_lsstcomcamsim.transformed_efd_scheduler.created_at IS 'Timestamp when the record was created, default is the current timestamp';
COMMENT ON CONSTRAINT un_id ON cdb_lsstcomcamsim.transformed_efd_scheduler IS 'Ensure id is unique.';
