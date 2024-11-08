
CREATE TABLE cdb_lsstcomcam.exposure_efd (
	exposure_id BIGINT,
	created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	instrument CHAR(20),
	mt_azimuth_encoder_absolute_position0_rms_jitter FLOAT,
	mt_azimuth_encoder_absolute_position1_rms_jitter FLOAT,
	mt_azimuth_encoder_absolute_position2_rms_jitter FLOAT,
	mt_azimuth_encoder_absolute_position3_rms_jitter FLOAT,
	mt_elevation_encoder_absolute_position0_rms_jitter FLOAT,
	mt_elevation_encoder_absolute_position1_rms_jitter FLOAT,
	mt_elevation_encoder_absolute_position2_rms_jitter FLOAT,
	mt_elevation_encoder_absolute_position3_rms_jitter FLOAT,
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
	mt_salindex1_temperatureitem_0_mean FLOAT,
	mt_salindex1_temperatureitem_0_stddev FLOAT,
	mt_salindex1_temperatureitem_0_min FLOAT,
	mt_salindex1_temperatureitem_1_mean FLOAT,
	mt_salindex1_temperatureitem_0_max FLOAT,
	mt_salindex1_temperatureitem_1_stddev FLOAT,
	mt_salindex1_temperatureitem_1_min FLOAT,
	mt_salindex1_temperatureitem_1_max FLOAT,
	mt_salindex1_temperatureitem_2_mean FLOAT,
	mt_salindex1_temperatureitem_2_stddev FLOAT,
	mt_salindex1_temperatureitem_2_min FLOAT,
	mt_salindex1_temperatureitem_2_max FLOAT,
	mt_salindex1_temperatureitem_3_mean FLOAT,
	mt_salindex1_temperatureitem_3_stddev FLOAT,
	mt_salindex1_temperatureitem_3_min FLOAT,
	mt_salindex1_temperatureitem_3_max FLOAT,
	mt_salindex1_temperatureitem_4_mean FLOAT,
	mt_salindex1_temperatureitem_4_stddev FLOAT,
	mt_salindex1_temperatureitem_4_min FLOAT,
	mt_salindex1_temperatureitem_4_max FLOAT,
	mt_salindex1_temperatureitem_5_mean FLOAT,
	mt_salindex1_temperatureitem_5_stddev FLOAT,
	mt_salindex1_temperatureitem_5_min FLOAT,
	mt_salindex1_temperatureitem_5_max FLOAT,
	mt_salindex1_temperatureitem_6_mean FLOAT,
	mt_salindex1_temperatureitem_6_stddev FLOAT,
	mt_salindex1_temperatureitem_6_min FLOAT,
	mt_salindex1_temperatureitem_6_max FLOAT,
	mt_salindex1_temperatureitem_7_mean FLOAT,
	mt_salindex1_temperatureitem_7_stddev FLOAT,
	mt_salindex1_temperatureitem_7_min FLOAT,
	mt_salindex1_temperatureitem_7_max FLOAT,
	mt_salindex101_temperatureitem_0_mean FLOAT,
	mt_salindex101_temperatureitem_0_stddev FLOAT,
	mt_salindex101_temperatureitem_0_min FLOAT,
	mt_salindex101_temperatureitem_1_mean FLOAT,
	mt_salindex101_temperatureitem_0_max FLOAT,
	mt_salindex101_temperatureitem_1_stddev FLOAT,
	mt_salindex101_temperatureitem_1_min FLOAT,
	mt_salindex101_temperatureitem_1_max FLOAT,
	mt_salindex101_temperatureitem_2_mean FLOAT,
	mt_salindex101_temperatureitem_2_stddev FLOAT,
	mt_salindex101_temperatureitem_2_min FLOAT,
	mt_salindex101_temperatureitem_2_max FLOAT,
	mt_salindex101_temperatureitem_3_mean FLOAT,
	mt_salindex101_temperatureitem_3_stddev FLOAT,
	mt_salindex101_temperatureitem_3_min FLOAT,
	mt_salindex101_temperatureitem_3_max FLOAT,
	mt_salindex101_temperatureitem_4_mean FLOAT,
	mt_salindex101_temperatureitem_4_stddev FLOAT,
	mt_salindex101_temperatureitem_4_min FLOAT,
	mt_salindex101_temperatureitem_4_max FLOAT,
	mt_salindex101_temperatureitem_5_mean FLOAT,
	mt_salindex101_temperatureitem_5_stddev FLOAT,
	mt_salindex101_temperatureitem_5_min FLOAT,
	mt_salindex101_temperatureitem_5_max FLOAT,
	mt_salindex101_temperatureitem_6_mean FLOAT,
	mt_salindex101_temperatureitem_6_stddev FLOAT,
	mt_salindex101_temperatureitem_6_min FLOAT,
	mt_salindex101_temperatureitem_6_max FLOAT,
	mt_salindex101_temperatureitem_7_mean FLOAT,
	mt_salindex101_temperatureitem_7_stddev FLOAT,
	mt_salindex101_temperatureitem_7_min FLOAT,
	mt_salindex101_temperatureitem_7_max FLOAT,
	mt_salindex102_temperatureitem_0_mean FLOAT,
	mt_salindex102_temperatureitem_0_stddev FLOAT,
	mt_salindex102_temperatureitem_0_min FLOAT,
	mt_salindex102_temperatureitem_1_mean FLOAT,
	mt_salindex102_temperatureitem_0_max FLOAT,
	mt_salindex102_temperatureitem_1_stddev FLOAT,
	mt_salindex102_temperatureitem_1_min FLOAT,
	mt_salindex102_temperatureitem_1_max FLOAT,
	mt_salindex102_temperatureitem_2_mean FLOAT,
	mt_salindex102_temperatureitem_2_stddev FLOAT,
	mt_salindex102_temperatureitem_2_min FLOAT,
	mt_salindex102_temperatureitem_2_max FLOAT,
	mt_salindex102_temperatureitem_3_mean FLOAT,
	mt_salindex102_temperatureitem_3_stddev FLOAT,
	mt_salindex102_temperatureitem_3_min FLOAT,
	mt_salindex102_temperatureitem_3_max FLOAT,
	mt_salindex102_temperatureitem_4_mean FLOAT,
	mt_salindex102_temperatureitem_4_stddev FLOAT,
	mt_salindex102_temperatureitem_4_min FLOAT,
	mt_salindex102_temperatureitem_4_max FLOAT,
	mt_salindex102_temperatureitem_5_mean FLOAT,
	mt_salindex102_temperatureitem_5_stddev FLOAT,
	mt_salindex102_temperatureitem_5_min FLOAT,
	mt_salindex102_temperatureitem_5_max FLOAT,
	mt_salindex102_temperatureitem_6_mean FLOAT,
	mt_salindex102_temperatureitem_6_stddev FLOAT,
	mt_salindex102_temperatureitem_6_min FLOAT,
	mt_salindex102_temperatureitem_6_max FLOAT,
	mt_salindex102_temperatureitem_7_mean FLOAT,
	mt_salindex102_temperatureitem_7_stddev FLOAT,
	mt_salindex102_temperatureitem_7_min FLOAT,
	mt_salindex102_temperatureitem_7_max FLOAT,
	mt_salindex103_temperatureitem_0_mean FLOAT,
	mt_salindex103_temperatureitem_0_stddev FLOAT,
	mt_salindex103_temperatureitem_0_min FLOAT,
	mt_salindex103_temperatureitem_1_mean FLOAT,
	mt_salindex103_temperatureitem_0_max FLOAT,
	mt_salindex103_temperatureitem_1_stddev FLOAT,
	mt_salindex103_temperatureitem_1_min FLOAT,
	mt_salindex103_temperatureitem_1_max FLOAT,
	mt_salindex103_temperatureitem_2_mean FLOAT,
	mt_salindex103_temperatureitem_2_stddev FLOAT,
	mt_salindex103_temperatureitem_2_min FLOAT,
	mt_salindex103_temperatureitem_2_max FLOAT,
	mt_salindex103_temperatureitem_3_mean FLOAT,
	mt_salindex103_temperatureitem_3_stddev FLOAT,
	mt_salindex103_temperatureitem_3_min FLOAT,
	mt_salindex103_temperatureitem_3_max FLOAT,
	mt_salindex103_temperatureitem_4_mean FLOAT,
	mt_salindex103_temperatureitem_4_stddev FLOAT,
	mt_salindex103_temperatureitem_4_min FLOAT,
	mt_salindex103_temperatureitem_4_max FLOAT,
	mt_salindex103_temperatureitem_5_mean FLOAT,
	mt_salindex103_temperatureitem_5_stddev FLOAT,
	mt_salindex103_temperatureitem_5_min FLOAT,
	mt_salindex103_temperatureitem_5_max FLOAT,
	mt_salindex103_temperatureitem_6_mean FLOAT,
	mt_salindex103_temperatureitem_6_stddev FLOAT,
	mt_salindex103_temperatureitem_6_min FLOAT,
	mt_salindex103_temperatureitem_6_max FLOAT,
	mt_salindex103_temperatureitem_7_mean FLOAT,
	mt_salindex103_temperatureitem_7_stddev FLOAT,
	mt_salindex103_temperatureitem_7_min FLOAT,
	mt_salindex103_temperatureitem_7_max FLOAT,
	mt_salindex106_temperatureitem_0_mean FLOAT,
	mt_salindex106_temperatureitem_0_stddev FLOAT,
	mt_salindex106_temperatureitem_0_min FLOAT,
	mt_salindex106_temperatureitem_1_mean FLOAT,
	mt_salindex106_temperatureitem_0_max FLOAT,
	mt_salindex106_temperatureitem_1_stddev FLOAT,
	mt_salindex106_temperatureitem_1_min FLOAT,
	mt_salindex106_temperatureitem_1_max FLOAT,
	mt_salindex106_temperatureitem_2_mean FLOAT,
	mt_salindex106_temperatureitem_2_stddev FLOAT,
	mt_salindex106_temperatureitem_2_min FLOAT,
	mt_salindex106_temperatureitem_2_max FLOAT,
	mt_salindex106_temperatureitem_3_mean FLOAT,
	mt_salindex106_temperatureitem_3_stddev FLOAT,
	mt_salindex106_temperatureitem_3_min FLOAT,
	mt_salindex106_temperatureitem_3_max FLOAT,
	mt_salindex106_temperatureitem_4_mean FLOAT,
	mt_salindex106_temperatureitem_4_stddev FLOAT,
	mt_salindex106_temperatureitem_4_min FLOAT,
	mt_salindex106_temperatureitem_4_max FLOAT,
	mt_salindex106_temperatureitem_5_mean FLOAT,
	mt_salindex106_temperatureitem_5_stddev FLOAT,
	mt_salindex106_temperatureitem_5_min FLOAT,
	mt_salindex106_temperatureitem_5_max FLOAT,
	mt_salindex106_temperatureitem_6_mean FLOAT,
	mt_salindex106_temperatureitem_6_stddev FLOAT,
	mt_salindex106_temperatureitem_6_min FLOAT,
	mt_salindex106_temperatureitem_6_max FLOAT,
	mt_salindex106_temperatureitem_7_mean FLOAT,
	mt_salindex106_temperatureitem_7_stddev FLOAT,
	mt_salindex106_temperatureitem_7_min FLOAT,
	mt_salindex106_temperatureitem_7_max FLOAT,
	mt_salindex107_temperatureitem_0_mean FLOAT,
	mt_salindex107_temperatureitem_0_stddev FLOAT,
	mt_salindex107_temperatureitem_0_min FLOAT,
	mt_salindex107_temperatureitem_1_mean FLOAT,
	mt_salindex107_temperatureitem_0_max FLOAT,
	mt_salindex107_temperatureitem_1_stddev FLOAT,
	mt_salindex107_temperatureitem_1_min FLOAT,
	mt_salindex107_temperatureitem_1_max FLOAT,
	mt_salindex107_temperatureitem_2_mean FLOAT,
	mt_salindex107_temperatureitem_2_stddev FLOAT,
	mt_salindex107_temperatureitem_2_min FLOAT,
	mt_salindex107_temperatureitem_2_max FLOAT,
	mt_salindex107_temperatureitem_3_mean FLOAT,
	mt_salindex107_temperatureitem_3_stddev FLOAT,
	mt_salindex107_temperatureitem_3_min FLOAT,
	mt_salindex107_temperatureitem_3_max FLOAT,
	mt_salindex107_temperatureitem_4_mean FLOAT,
	mt_salindex107_temperatureitem_4_stddev FLOAT,
	mt_salindex107_temperatureitem_4_min FLOAT,
	mt_salindex107_temperatureitem_4_max FLOAT,
	mt_salindex107_temperatureitem_5_mean FLOAT,
	mt_salindex107_temperatureitem_5_stddev FLOAT,
	mt_salindex107_temperatureitem_5_min FLOAT,
	mt_salindex107_temperatureitem_5_max FLOAT,
	mt_salindex107_temperatureitem_6_mean FLOAT,
	mt_salindex107_temperatureitem_6_stddev FLOAT,
	mt_salindex107_temperatureitem_6_min FLOAT,
	mt_salindex107_temperatureitem_6_max FLOAT,
	mt_salindex107_temperatureitem_7_mean FLOAT,
	mt_salindex107_temperatureitem_7_stddev FLOAT,
	mt_salindex107_temperatureitem_7_min FLOAT,
	mt_salindex107_temperatureitem_7_max FLOAT,
	mt_salindex108_temperatureitem_0_mean FLOAT,
	mt_salindex108_temperatureitem_0_stddev FLOAT,
	mt_salindex108_temperatureitem_0_min FLOAT,
	mt_salindex108_temperatureitem_1_mean FLOAT,
	mt_salindex108_temperatureitem_0_max FLOAT,
	mt_salindex108_temperatureitem_1_stddev FLOAT,
	mt_salindex108_temperatureitem_1_min FLOAT,
	mt_salindex108_temperatureitem_1_max FLOAT,
	mt_salindex108_temperatureitem_2_mean FLOAT,
	mt_salindex108_temperatureitem_2_stddev FLOAT,
	mt_salindex108_temperatureitem_2_min FLOAT,
	mt_salindex108_temperatureitem_2_max FLOAT,
	mt_salindex108_temperatureitem_3_mean FLOAT,
	mt_salindex108_temperatureitem_3_stddev FLOAT,
	mt_salindex108_temperatureitem_3_min FLOAT,
	mt_salindex108_temperatureitem_3_max FLOAT,
	mt_salindex108_temperatureitem_4_mean FLOAT,
	mt_salindex108_temperatureitem_4_stddev FLOAT,
	mt_salindex108_temperatureitem_4_min FLOAT,
	mt_salindex108_temperatureitem_4_max FLOAT,
	mt_salindex108_temperatureitem_5_mean FLOAT,
	mt_salindex108_temperatureitem_5_stddev FLOAT,
	mt_salindex108_temperatureitem_5_min FLOAT,
	mt_salindex108_temperatureitem_5_max FLOAT,
	mt_salindex108_temperatureitem_6_mean FLOAT,
	mt_salindex108_temperatureitem_6_stddev FLOAT,
	mt_salindex108_temperatureitem_6_min FLOAT,
	mt_salindex108_temperatureitem_6_max FLOAT,
	mt_salindex108_temperatureitem_7_mean FLOAT,
	mt_salindex108_temperatureitem_7_stddev FLOAT,
	mt_salindex108_temperatureitem_7_min FLOAT,
	mt_salindex108_temperatureitem_7_max FLOAT,
	mt_salindex301_temperatureitem_0_mean FLOAT,
	mt_salindex301_temperatureitem_0_stddev FLOAT,
	mt_salindex301_temperatureitem_0_min FLOAT,
	mt_salindex301_temperatureitem_1_mean FLOAT,
	mt_salindex301_temperatureitem_0_max FLOAT,
	mt_salindex301_temperatureitem_1_stddev FLOAT,
	mt_salindex301_temperatureitem_1_min FLOAT,
	mt_salindex301_temperatureitem_1_max FLOAT,
	mt_salindex301_temperatureitem_2_mean FLOAT,
	mt_salindex301_temperatureitem_2_stddev FLOAT,
	mt_salindex301_temperatureitem_2_min FLOAT,
	mt_salindex301_temperatureitem_2_max FLOAT,
	mt_salindex301_temperatureitem_3_mean FLOAT,
	mt_salindex301_temperatureitem_3_stddev FLOAT,
	mt_salindex301_temperatureitem_3_min FLOAT,
	mt_salindex301_temperatureitem_3_max FLOAT,
	mt_salindex301_temperatureitem_4_mean FLOAT,
	mt_salindex301_temperatureitem_4_stddev FLOAT,
	mt_salindex301_temperatureitem_4_min FLOAT,
	mt_salindex301_temperatureitem_4_max FLOAT,
	mt_salindex301_temperatureitem_5_mean FLOAT,
	mt_salindex301_temperatureitem_5_stddev FLOAT,
	mt_salindex301_temperatureitem_5_min FLOAT,
	mt_salindex301_temperatureitem_5_max FLOAT,
	mt_salindex301_temperatureitem_6_mean FLOAT,
	mt_salindex301_temperatureitem_6_stddev FLOAT,
	mt_salindex301_temperatureitem_6_min FLOAT,
	mt_salindex301_temperatureitem_6_max FLOAT,
	mt_salindex301_temperatureitem_7_mean FLOAT,
	mt_salindex301_temperatureitem_7_stddev FLOAT,
	mt_salindex301_temperatureitem_7_min FLOAT,
	mt_salindex301_temperatureitem_7_max FLOAT,
	mt_dimm_fwhm_mean FLOAT,
	mt_azimuth_encoder_absolute_position0_mean FLOAT,
	mt_azimuth_encoder_absolute_position1_mean FLOAT,
	mt_azimuth_encoder_absolute_position2_mean FLOAT,
	mt_azimuth_encoder_absolute_position3_mean FLOAT,
	mt_elevation_encoder_absolute_position0_mean FLOAT,
	mt_elevation_encoder_absolute_position1_mean FLOAT,
	mt_elevation_encoder_absolute_position2_mean FLOAT,
	mt_elevation_encoder_absolute_position3_mean FLOAT,
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
	mt_salindex104_acceleration_x_mean FLOAT,
	mt_salindex104_acceleration_x_stddev FLOAT,
	mt_salindex104_acceleration_x_min FLOAT,
	mt_salindex104_acceleration_x_max FLOAT,
	mt_salindey104_acceleration_y_mean FLOAT,
	mt_salindex104_acceleration_y_stddev FLOAT,
	mt_salindex104_acceleration_y_min FLOAT,
	mt_salindex104_acceleration_y_max FLOAT,
	mt_salindez104_acceleration_z_mean FLOAT,
	mt_salindex104_acceleration_z_stddev FLOAT,
	mt_salindex104_acceleration_z_min FLOAT,
	mt_salindex104_acceleration_z_max FLOAT,
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
	PRIMARY KEY (exposure_id, instrument),
	CONSTRAINT un_exposure_id_instrument UNIQUE (exposure_id, instrument)
)

;
COMMENT ON TABLE cdb_lsstcomcam.exposure_efd IS 'Transformed EFD topics by exposure.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.exposure_id IS 'Exposure unique ID.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.created_at IS 'Timestamp when the record was created, default is the current timestamp';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.instrument IS 'Instrument name.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_azimuth_encoder_absolute_position0_rms_jitter IS 'RMS after 4th order polynomial fit of Azimuth absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_azimuth_encoder_absolute_position1_rms_jitter IS 'RMS after 4th order polynomial fit of Azimuth absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_azimuth_encoder_absolute_position2_rms_jitter IS 'RMS after 4th order polynomial fit of Azimuth absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_azimuth_encoder_absolute_position3_rms_jitter IS 'RMS after 4th order polynomial fit of Azimuth absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_elevation_encoder_absolute_position0_rms_jitter IS 'RMS after 4th order polynomial fit of Elevation absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_elevation_encoder_absolute_position1_rms_jitter IS 'RMS after 4th order polynomial fit of Elevation absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_elevation_encoder_absolute_position2_rms_jitter IS 'RMS after 4th order polynomial fit of Elevation absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_elevation_encoder_absolute_position3_rms_jitter IS 'RMS after 4th order polynomial fit of Elevation absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_sonic_temperature_mean IS 'Median sonic temperature (air temperature measured sonically). Sonic temperature has poor absolute accuracy (it can be off by several degrees) but good time resolution.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_sonic_temperature_stddev IS 'Median sonic temperature (air temperature measured sonically). Sonic temperature has poor absolute accuracy (it can be off by several degrees) but good time resolution.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.at_salindex110_sonic_temperature_stddev_mean IS 'Standard devation of sonic temperature (air temperature measured sonically) estimated from quartiles.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.at_salindex110_sonic_temperature_stddev_stddev IS 'Standard devation of sonic temperature (air temperature measured sonically) estimated from quartiles.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_wind_speed_0_mean IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 0 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_wind_speed_0_stddev IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 0 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_wind_speed_0_min IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 0 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_wind_speed_0_max IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 0 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_wind_speed_1_mean IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 1 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_wind_speed_1_stddev IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 1 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_wind_speed_1_min IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 1 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_wind_speed_1_max IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 1 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_wind_speed_2_mean IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 2 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_wind_speed_2_stddev IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 2 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_wind_speed_2_min IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 2 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_wind_speed_2_max IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 2 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_wind_speed_speedstddev_0_mean IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 0 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_wind_speed_speedstddev_0_stddev IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 0 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_wind_speed_speedstddev_0_min IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 0 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_wind_speed_speedstddev_0_max IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 0 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_wind_speed_speedstddev_1_mean IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 1 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_wind_speed_speedstddev_1_stddev IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 1 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_wind_speed_speedstddev_1_min IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 1 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_wind_speed_speedstddev_1_max IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 1 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_wind_speed_speedstddev_2_mean IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 2 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_wind_speed_speedstddev_2_stddev IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 2 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_wind_speed_speedstddev_2_min IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 2 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_wind_speed_speedstddev_2_max IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 2 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_wind_speed_magnitude_mean IS 'Median wind speed magnitude in TMA-GillLabJack01 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_wind_speed_magnitude_stddev IS 'Median wind speed magnitude in TMA-GillLabJack01 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_wind_speed_magnitude_min IS 'Median wind speed magnitude in TMA-GillLabJack01 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_wind_speed_magnitude_max IS 'Median wind speed magnitude in TMA-GillLabJack01 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_wind_speed_maxmagnitude_mean IS 'Maximum wind speed magnitude in TMA-GillLabJack01 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_wind_speed_maxmagnitude_stddev IS 'Maximum wind speed magnitude in TMA-GillLabJack01 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_wind_speed_maxmagnitude_min IS 'Maximum wind speed magnitude in TMA-GillLabJack01 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex110_wind_speed_maxmagnitude_max IS 'Maximum wind speed magnitude in TMA-GillLabJack01 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex1_temperatureitem_0_mean IS 'MTCameraAssembly-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex1_temperatureitem_0_stddev IS 'MTCameraAssembly-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex1_temperatureitem_0_min IS 'MTCameraAssembly-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex1_temperatureitem_1_mean IS 'MTCameraAssembly-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex1_temperatureitem_0_max IS 'MTCameraAssembly-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex1_temperatureitem_1_stddev IS 'MTCameraAssembly-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex1_temperatureitem_1_min IS 'MTCameraAssembly-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex1_temperatureitem_1_max IS 'MTCameraAssembly-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex1_temperatureitem_2_mean IS 'MTCameraAssembly-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex1_temperatureitem_2_stddev IS 'MTCameraAssembly-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex1_temperatureitem_2_min IS 'MTCameraAssembly-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex1_temperatureitem_2_max IS 'MTCameraAssembly-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex1_temperatureitem_3_mean IS 'MTCameraAssembly-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex1_temperatureitem_3_stddev IS 'MTCameraAssembly-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex1_temperatureitem_3_min IS 'MTCameraAssembly-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex1_temperatureitem_3_max IS 'MTCameraAssembly-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex1_temperatureitem_4_mean IS 'MTCameraAssembly-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex1_temperatureitem_4_stddev IS 'MTCameraAssembly-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex1_temperatureitem_4_min IS 'MTCameraAssembly-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex1_temperatureitem_4_max IS 'MTCameraAssembly-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex1_temperatureitem_5_mean IS 'MTCameraAssembly-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex1_temperatureitem_5_stddev IS 'MTCameraAssembly-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex1_temperatureitem_5_min IS 'MTCameraAssembly-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex1_temperatureitem_5_max IS 'MTCameraAssembly-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex1_temperatureitem_6_mean IS 'MTCameraAssembly-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex1_temperatureitem_6_stddev IS 'MTCameraAssembly-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex1_temperatureitem_6_min IS 'MTCameraAssembly-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex1_temperatureitem_6_max IS 'MTCameraAssembly-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex1_temperatureitem_7_mean IS 'MTCameraAssembly-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex1_temperatureitem_7_stddev IS 'MTCameraAssembly-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex1_temperatureitem_7_min IS 'MTCameraAssembly-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex1_temperatureitem_7_max IS 'MTCameraAssembly-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex101_temperatureitem_0_mean IS 'MTCameraAssembly-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex101_temperatureitem_0_stddev IS 'MTCameraAssembly-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex101_temperatureitem_0_min IS 'MTCameraAssembly-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex101_temperatureitem_1_mean IS 'MTCameraAssembly-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex101_temperatureitem_0_max IS 'MTCameraAssembly-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex101_temperatureitem_1_stddev IS 'MTCameraAssembly-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex101_temperatureitem_1_min IS 'MTCameraAssembly-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex101_temperatureitem_1_max IS 'MTCameraAssembly-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex101_temperatureitem_2_mean IS 'MTCameraAssembly-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex101_temperatureitem_2_stddev IS 'MTCameraAssembly-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex101_temperatureitem_2_min IS 'MTCameraAssembly-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex101_temperatureitem_2_max IS 'MTCameraAssembly-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex101_temperatureitem_3_mean IS 'MTCameraAssembly-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex101_temperatureitem_3_stddev IS 'MTCameraAssembly-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex101_temperatureitem_3_min IS 'MTCameraAssembly-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex101_temperatureitem_3_max IS 'MTCameraAssembly-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex101_temperatureitem_4_mean IS 'MTCameraAssembly-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex101_temperatureitem_4_stddev IS 'MTCameraAssembly-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex101_temperatureitem_4_min IS 'MTCameraAssembly-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex101_temperatureitem_4_max IS 'MTCameraAssembly-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex101_temperatureitem_5_mean IS 'MTCameraAssembly-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex101_temperatureitem_5_stddev IS 'MTCameraAssembly-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex101_temperatureitem_5_min IS 'MTCameraAssembly-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex101_temperatureitem_5_max IS 'MTCameraAssembly-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex101_temperatureitem_6_mean IS 'MTCameraAssembly-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex101_temperatureitem_6_stddev IS 'MTCameraAssembly-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex101_temperatureitem_6_min IS 'MTCameraAssembly-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex101_temperatureitem_6_max IS 'MTCameraAssembly-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex101_temperatureitem_7_mean IS 'MTCameraAssembly-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex101_temperatureitem_7_stddev IS 'MTCameraAssembly-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex101_temperatureitem_7_min IS 'MTCameraAssembly-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex101_temperatureitem_7_max IS 'MTCameraAssembly-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex102_temperatureitem_0_mean IS 'temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex102_temperatureitem_0_stddev IS 'temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex102_temperatureitem_0_min IS 'temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex102_temperatureitem_1_mean IS 'temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex102_temperatureitem_0_max IS 'temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex102_temperatureitem_1_stddev IS 'temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex102_temperatureitem_1_min IS 'temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex102_temperatureitem_1_max IS 'temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex102_temperatureitem_2_mean IS 'temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex102_temperatureitem_2_stddev IS 'temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex102_temperatureitem_2_min IS 'temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex102_temperatureitem_2_max IS 'temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex102_temperatureitem_3_mean IS 'temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex102_temperatureitem_3_stddev IS 'temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex102_temperatureitem_3_min IS 'temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex102_temperatureitem_3_max IS 'temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex102_temperatureitem_4_mean IS 'temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex102_temperatureitem_4_stddev IS 'temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex102_temperatureitem_4_min IS 'temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex102_temperatureitem_4_max IS 'temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex102_temperatureitem_5_mean IS 'temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex102_temperatureitem_5_stddev IS 'temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex102_temperatureitem_5_min IS 'temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex102_temperatureitem_5_max IS 'temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex102_temperatureitem_6_mean IS 'temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex102_temperatureitem_6_stddev IS 'temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex102_temperatureitem_6_min IS 'temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex102_temperatureitem_6_max IS 'temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex102_temperatureitem_7_mean IS 'temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex102_temperatureitem_7_stddev IS 'temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex102_temperatureitem_7_min IS 'temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex102_temperatureitem_7_max IS 'temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex103_temperatureitem_0_mean IS 'temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex103_temperatureitem_0_stddev IS 'temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex103_temperatureitem_0_min IS 'temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex103_temperatureitem_1_mean IS 'temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex103_temperatureitem_0_max IS 'temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex103_temperatureitem_1_stddev IS 'temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex103_temperatureitem_1_min IS 'temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex103_temperatureitem_1_max IS 'temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex103_temperatureitem_2_mean IS 'temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex103_temperatureitem_2_stddev IS 'temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex103_temperatureitem_2_min IS 'temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex103_temperatureitem_2_max IS 'temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex103_temperatureitem_3_mean IS 'temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex103_temperatureitem_3_stddev IS 'temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex103_temperatureitem_3_min IS 'temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex103_temperatureitem_3_max IS 'temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex103_temperatureitem_4_mean IS 'temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex103_temperatureitem_4_stddev IS 'temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex103_temperatureitem_4_min IS 'temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex103_temperatureitem_4_max IS 'temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex103_temperatureitem_5_mean IS 'temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex103_temperatureitem_5_stddev IS 'temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex103_temperatureitem_5_min IS 'temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex103_temperatureitem_5_max IS 'temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex103_temperatureitem_6_mean IS 'temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex103_temperatureitem_6_stddev IS 'temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex103_temperatureitem_6_min IS 'temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex103_temperatureitem_6_max IS 'temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex103_temperatureitem_7_mean IS 'temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex103_temperatureitem_7_stddev IS 'temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex103_temperatureitem_7_min IS 'temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex103_temperatureitem_7_max IS 'temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex106_temperatureitem_0_mean IS 'M2-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex106_temperatureitem_0_stddev IS 'M2-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex106_temperatureitem_0_min IS 'M2-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex106_temperatureitem_1_mean IS 'M2-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex106_temperatureitem_0_max IS 'M2-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex106_temperatureitem_1_stddev IS 'M2-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex106_temperatureitem_1_min IS 'M2-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex106_temperatureitem_1_max IS 'M2-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex106_temperatureitem_2_mean IS 'M2-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex106_temperatureitem_2_stddev IS 'M2-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex106_temperatureitem_2_min IS 'M2-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex106_temperatureitem_2_max IS 'M2-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex106_temperatureitem_3_mean IS 'M2-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex106_temperatureitem_3_stddev IS 'M2-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex106_temperatureitem_3_min IS 'M2-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex106_temperatureitem_3_max IS 'M2-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex106_temperatureitem_4_mean IS 'M2-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex106_temperatureitem_4_stddev IS 'M2-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex106_temperatureitem_4_min IS 'M2-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex106_temperatureitem_4_max IS 'M2-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex106_temperatureitem_5_mean IS 'M2-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex106_temperatureitem_5_stddev IS 'M2-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex106_temperatureitem_5_min IS 'M2-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex106_temperatureitem_5_max IS 'M2-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex106_temperatureitem_6_mean IS 'M2-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex106_temperatureitem_6_stddev IS 'M2-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex106_temperatureitem_6_min IS 'M2-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex106_temperatureitem_6_max IS 'M2-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex106_temperatureitem_7_mean IS 'M2-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex106_temperatureitem_7_stddev IS 'M2-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex106_temperatureitem_7_min IS 'M2-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex106_temperatureitem_7_max IS 'M2-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex107_temperatureitem_0_mean IS 'Laser-ESS01, Laser-ESS02 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex107_temperatureitem_0_stddev IS 'Laser-ESS01, Laser-ESS02 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex107_temperatureitem_0_min IS 'Laser-ESS01, Laser-ESS02 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex107_temperatureitem_1_mean IS 'Laser-ESS01, Laser-ESS02 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex107_temperatureitem_0_max IS 'Laser-ESS01, Laser-ESS02 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex107_temperatureitem_1_stddev IS 'Laser-ESS01, Laser-ESS02 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex107_temperatureitem_1_min IS 'Laser-ESS01, Laser-ESS02 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex107_temperatureitem_1_max IS 'Laser-ESS01, Laser-ESS02 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex107_temperatureitem_2_mean IS 'Laser-ESS01, Laser-ESS02 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex107_temperatureitem_2_stddev IS 'Laser-ESS01, Laser-ESS02 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex107_temperatureitem_2_min IS 'Laser-ESS01, Laser-ESS02 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex107_temperatureitem_2_max IS 'Laser-ESS01, Laser-ESS02 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex107_temperatureitem_3_mean IS 'Laser-ESS01, Laser-ESS02 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex107_temperatureitem_3_stddev IS 'Laser-ESS01, Laser-ESS02 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex107_temperatureitem_3_min IS 'Laser-ESS01, Laser-ESS02 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex107_temperatureitem_3_max IS 'Laser-ESS01, Laser-ESS02 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex107_temperatureitem_4_mean IS 'Laser-ESS01, Laser-ESS02 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex107_temperatureitem_4_stddev IS 'Laser-ESS01, Laser-ESS02 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex107_temperatureitem_4_min IS 'Laser-ESS01, Laser-ESS02 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex107_temperatureitem_4_max IS 'Laser-ESS01, Laser-ESS02 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex107_temperatureitem_5_mean IS 'Laser-ESS01, Laser-ESS02 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex107_temperatureitem_5_stddev IS 'Laser-ESS01, Laser-ESS02 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex107_temperatureitem_5_min IS 'Laser-ESS01, Laser-ESS02 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex107_temperatureitem_5_max IS 'Laser-ESS01, Laser-ESS02 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex107_temperatureitem_6_mean IS 'Laser-ESS01, Laser-ESS02 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex107_temperatureitem_6_stddev IS 'Laser-ESS01, Laser-ESS02 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex107_temperatureitem_6_min IS 'Laser-ESS01, Laser-ESS02 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex107_temperatureitem_6_max IS 'Laser-ESS01, Laser-ESS02 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex107_temperatureitem_7_mean IS 'Laser-ESS01, Laser-ESS02 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex107_temperatureitem_7_stddev IS 'Laser-ESS01, Laser-ESS02 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex107_temperatureitem_7_min IS 'Laser-ESS01, Laser-ESS02 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex107_temperatureitem_7_max IS 'Laser-ESS01, Laser-ESS02 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex108_temperatureitem_0_mean IS 'CBP-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex108_temperatureitem_0_stddev IS 'CBP-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex108_temperatureitem_0_min IS 'CBP-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex108_temperatureitem_1_mean IS 'CBP-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex108_temperatureitem_0_max IS 'CBP-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex108_temperatureitem_1_stddev IS 'CBP-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex108_temperatureitem_1_min IS 'CBP-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex108_temperatureitem_1_max IS 'CBP-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex108_temperatureitem_2_mean IS 'CBP-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex108_temperatureitem_2_stddev IS 'CBP-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex108_temperatureitem_2_min IS 'CBP-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex108_temperatureitem_2_max IS 'CBP-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex108_temperatureitem_3_mean IS 'CBP-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex108_temperatureitem_3_stddev IS 'CBP-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex108_temperatureitem_3_min IS 'CBP-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex108_temperatureitem_3_max IS 'CBP-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex108_temperatureitem_4_mean IS 'CBP-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex108_temperatureitem_4_stddev IS 'CBP-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex108_temperatureitem_4_min IS 'CBP-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex108_temperatureitem_4_max IS 'CBP-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex108_temperatureitem_5_mean IS 'CBP-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex108_temperatureitem_5_stddev IS 'CBP-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex108_temperatureitem_5_min IS 'CBP-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex108_temperatureitem_5_max IS 'CBP-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex108_temperatureitem_6_mean IS 'CBP-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex108_temperatureitem_6_stddev IS 'CBP-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex108_temperatureitem_6_min IS 'CBP-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex108_temperatureitem_6_max IS 'CBP-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex108_temperatureitem_7_mean IS 'CBP-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex108_temperatureitem_7_stddev IS 'CBP-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex108_temperatureitem_7_min IS 'CBP-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex108_temperatureitem_7_max IS 'CBP-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex301_temperatureitem_0_mean IS 'Weather tower air temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex301_temperatureitem_0_stddev IS 'Weather tower air temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex301_temperatureitem_0_min IS 'Weather tower air temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex301_temperatureitem_1_mean IS 'Weather tower air temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex301_temperatureitem_0_max IS 'Weather tower air temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex301_temperatureitem_1_stddev IS 'Weather tower air temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex301_temperatureitem_1_min IS 'Weather tower air temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex301_temperatureitem_1_max IS 'Weather tower air temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex301_temperatureitem_2_mean IS 'Weather tower air temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex301_temperatureitem_2_stddev IS 'Weather tower air temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex301_temperatureitem_2_min IS 'Weather tower air temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex301_temperatureitem_2_max IS 'Weather tower air temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex301_temperatureitem_3_mean IS 'Weather tower air temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex301_temperatureitem_3_stddev IS 'Weather tower air temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex301_temperatureitem_3_min IS 'Weather tower air temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex301_temperatureitem_3_max IS 'Weather tower air temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex301_temperatureitem_4_mean IS 'Weather tower air temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex301_temperatureitem_4_stddev IS 'Weather tower air temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex301_temperatureitem_4_min IS 'Weather tower air temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex301_temperatureitem_4_max IS 'Weather tower air temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex301_temperatureitem_5_mean IS 'Weather tower air temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex301_temperatureitem_5_stddev IS 'Weather tower air temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex301_temperatureitem_5_min IS 'Weather tower air temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex301_temperatureitem_5_max IS 'Weather tower air temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex301_temperatureitem_6_mean IS 'Weather tower air temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex301_temperatureitem_6_stddev IS 'Weather tower air temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex301_temperatureitem_6_min IS 'Weather tower air temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex301_temperatureitem_6_max IS 'Weather tower air temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex301_temperatureitem_7_mean IS 'Weather tower air temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex301_temperatureitem_7_stddev IS 'Weather tower air temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex301_temperatureitem_7_min IS 'Weather tower air temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex301_temperatureitem_7_max IS 'Weather tower air temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_dimm_fwhm_mean IS 'Combined full width half maximum';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_azimuth_encoder_absolute_position0_mean IS 'Azimuth absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_azimuth_encoder_absolute_position1_mean IS 'Azimuth absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_azimuth_encoder_absolute_position2_mean IS 'Azimuth absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_azimuth_encoder_absolute_position3_mean IS 'Azimuth absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_elevation_encoder_absolute_position0_mean IS 'Elevation absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_elevation_encoder_absolute_position1_mean IS 'Elevation absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_elevation_encoder_absolute_position2_mean IS 'Elevation absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_elevation_encoder_absolute_position3_mean IS 'Elevation absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_hexapod_uncompensated_position_u_mean IS 'U angle.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_hexapod_uncompensated_position_u_max IS 'U angle.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_hexapod_uncompensated_position_u_min IS 'U angle.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_hexapod_uncompensated_position_v_mean IS 'V angle.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_hexapod_uncompensated_position_v_max IS 'V angle.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_hexapod_uncompensated_position_v_min IS 'V angle.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_hexapod_uncompensated_position_w_mean IS 'W angle.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_hexapod_uncompensated_position_w_max IS 'W angle.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_hexapod_uncompensated_position_w_min IS 'W angle.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_hexapod_uncompensated_position_x_mean IS 'X position.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_hexapod_uncompensated_position_x_max IS 'X position.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_hexapod_uncompensated_position_x_min IS 'X position.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_hexapod_uncompensated_position_y_mean IS 'Y position.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_hexapod_uncompensated_position_y_max IS 'Y position.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_hexapod_uncompensated_position_y_min IS 'Y position.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_hexapod_uncompensated_position_z_mean IS 'Z position.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_hexapod_uncompensated_position_z_max IS 'Z position.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_hexapod_uncompensated_position_z_min IS 'Z position.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex104_acceleration_x_mean IS 'Acceleration in x direction in SST top end ring +x -y, SST top end ring -x -y, SST spider spindle, SST M2 surrogate.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex104_acceleration_x_stddev IS 'Acceleration in x direction in SST top end ring +x -y, SST top end ring -x -y, SST spider spindle, SST M2 surrogate.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex104_acceleration_x_min IS 'Acceleration in x direction in SST top end ring +x -y, SST top end ring -x -y, SST spider spindle, SST M2 surrogate.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex104_acceleration_x_max IS 'Acceleration in x direction in SST top end ring +x -y, SST top end ring -x -y, SST spider spindle, SST M2 surrogate.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindey104_acceleration_y_mean IS 'Acceleration in y direction in SST top end ring +x -y, SST top end ring -x -y, SST spider spindle, SST M2 surrogate.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex104_acceleration_y_stddev IS 'Acceleration in y direction in SST top end ring +x -y, SST top end ring -x -y, SST spider spindle, SST M2 surrogate.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex104_acceleration_y_min IS 'Acceleration in y direction in SST top end ring +x -y, SST top end ring -x -y, SST spider spindle, SST M2 surrogate.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex104_acceleration_y_max IS 'Acceleration in y direction in SST top end ring +x -y, SST top end ring -x -y, SST spider spindle, SST M2 surrogate.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindez104_acceleration_z_mean IS 'Acceleration in z direction in SST top end ring +x -y, SST top end ring -x -y, SST spider spindle, SST M2 surrogate.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex104_acceleration_z_stddev IS 'Acceleration in z direction in SST top end ring +x -y, SST top end ring -x -y, SST spider spindle, SST M2 surrogate.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex104_acceleration_z_min IS 'Acceleration in z direction in SST top end ring +x -y, SST top end ring -x -y, SST spider spindle, SST M2 surrogate.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_salindex104_acceleration_z_max IS 'Acceleration in z direction in SST top end ring +x -y, SST top end ring -x -y, SST spider spindle, SST M2 surrogate.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_pointing_mount_position_ra_mean IS 'RA calculated from the azimuthActualPosition and elevationActualPosition.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_pointing_mount_position_ra_stddev IS 'RA calculated from the azimuthActualPosition and elevationActualPosition.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_pointing_mount_position_dec_mean IS 'Dec calculated from the azimuthActualPosition and elevationActualPosition.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_pointing_mount_position_dec_stddev IS 'Dec calculated from the azimuthActualPosition and elevationActualPosition.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_pointing_mount_position_sky_angle_mean IS 'Calculated sky angle.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_pointing_mount_position_sky_angle_stddev IS 'Calculated sky angle.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_pointing_mount_position_rotator_mean IS 'Rotator axis position reported by rotator component.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.mt_pointing_mount_position_rotator_stddev IS 'Rotator axis position reported by rotator component.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.camera_hexapod_aos_corrections_u IS 'U position offset.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.camera_hexapod_aos_corrections_v IS 'V position offset.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.camera_hexapod_aos_corrections_w IS 'W position offset.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.camera_hexapod_aos_corrections_x IS 'X position offset.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.camera_hexapod_aos_corrections_y IS 'Y position offset.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.camera_hexapod_aos_corrections_z IS 'Z position offset.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.m2_hexapod_aos_corrections_u IS 'U position offset.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.m2_hexapod_aos_corrections_v IS 'V position offset.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.m2_hexapod_aos_corrections_w IS 'W position offset.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.m2_hexapod_aos_corrections_x IS 'X position offset.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.m2_hexapod_aos_corrections_y IS 'Y position offset.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.m2_hexapod_aos_corrections_z IS 'Z position offset.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.m2_stress IS 'Calculate M2 stress computed RSS the stress contribution of each bending mode.';
COMMENT ON COLUMN cdb_lsstcomcam.exposure_efd.m1m3_stress IS 'Calculate M1M3 stress computed RSS the stress contribution of each bending mode.';
COMMENT ON CONSTRAINT un_exposure_id_instrument ON cdb_lsstcomcam.exposure_efd IS 'Ensure exposure_id is unique.';

CREATE TABLE cdb_lsstcomcam.visit1_efd (
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
	mt_salindex1_temperatureitem_0_mean FLOAT,
	mt_salindex1_temperatureitem_0_stddev FLOAT,
	mt_salindex1_temperatureitem_0_min FLOAT,
	mt_salindex1_temperatureitem_1_mean FLOAT,
	mt_salindex1_temperatureitem_0_max FLOAT,
	mt_salindex1_temperatureitem_1_stddev FLOAT,
	mt_salindex1_temperatureitem_1_min FLOAT,
	mt_salindex1_temperatureitem_1_max FLOAT,
	mt_salindex1_temperatureitem_2_mean FLOAT,
	mt_salindex1_temperatureitem_2_stddev FLOAT,
	mt_salindex1_temperatureitem_2_min FLOAT,
	mt_salindex1_temperatureitem_2_max FLOAT,
	mt_salindex1_temperatureitem_3_mean FLOAT,
	mt_salindex1_temperatureitem_3_stddev FLOAT,
	mt_salindex1_temperatureitem_3_min FLOAT,
	mt_salindex1_temperatureitem_3_max FLOAT,
	mt_salindex1_temperatureitem_4_mean FLOAT,
	mt_salindex1_temperatureitem_4_stddev FLOAT,
	mt_salindex1_temperatureitem_4_min FLOAT,
	mt_salindex1_temperatureitem_4_max FLOAT,
	mt_salindex1_temperatureitem_5_mean FLOAT,
	mt_salindex1_temperatureitem_5_stddev FLOAT,
	mt_salindex1_temperatureitem_5_min FLOAT,
	mt_salindex1_temperatureitem_5_max FLOAT,
	mt_salindex1_temperatureitem_6_mean FLOAT,
	mt_salindex1_temperatureitem_6_stddev FLOAT,
	mt_salindex1_temperatureitem_6_min FLOAT,
	mt_salindex1_temperatureitem_6_max FLOAT,
	mt_salindex1_temperatureitem_7_mean FLOAT,
	mt_salindex1_temperatureitem_7_stddev FLOAT,
	mt_salindex1_temperatureitem_7_min FLOAT,
	mt_salindex1_temperatureitem_7_max FLOAT,
	mt_salindex101_temperatureitem_0_mean FLOAT,
	mt_salindex101_temperatureitem_0_stddev FLOAT,
	mt_salindex101_temperatureitem_0_min FLOAT,
	mt_salindex101_temperatureitem_1_mean FLOAT,
	mt_salindex101_temperatureitem_0_max FLOAT,
	mt_salindex101_temperatureitem_1_stddev FLOAT,
	mt_salindex101_temperatureitem_1_min FLOAT,
	mt_salindex101_temperatureitem_1_max FLOAT,
	mt_salindex101_temperatureitem_2_mean FLOAT,
	mt_salindex101_temperatureitem_2_stddev FLOAT,
	mt_salindex101_temperatureitem_2_min FLOAT,
	mt_salindex101_temperatureitem_2_max FLOAT,
	mt_salindex101_temperatureitem_3_mean FLOAT,
	mt_salindex101_temperatureitem_3_stddev FLOAT,
	mt_salindex101_temperatureitem_3_min FLOAT,
	mt_salindex101_temperatureitem_3_max FLOAT,
	mt_salindex101_temperatureitem_4_mean FLOAT,
	mt_salindex101_temperatureitem_4_stddev FLOAT,
	mt_salindex101_temperatureitem_4_min FLOAT,
	mt_salindex101_temperatureitem_4_max FLOAT,
	mt_salindex101_temperatureitem_5_mean FLOAT,
	mt_salindex101_temperatureitem_5_stddev FLOAT,
	mt_salindex101_temperatureitem_5_min FLOAT,
	mt_salindex101_temperatureitem_5_max FLOAT,
	mt_salindex101_temperatureitem_6_mean FLOAT,
	mt_salindex101_temperatureitem_6_stddev FLOAT,
	mt_salindex101_temperatureitem_6_min FLOAT,
	mt_salindex101_temperatureitem_6_max FLOAT,
	mt_salindex101_temperatureitem_7_mean FLOAT,
	mt_salindex101_temperatureitem_7_stddev FLOAT,
	mt_salindex101_temperatureitem_7_min FLOAT,
	mt_salindex101_temperatureitem_7_max FLOAT,
	mt_salindex102_temperatureitem_0_mean FLOAT,
	mt_salindex102_temperatureitem_0_stddev FLOAT,
	mt_salindex102_temperatureitem_0_min FLOAT,
	mt_salindex102_temperatureitem_1_mean FLOAT,
	mt_salindex102_temperatureitem_0_max FLOAT,
	mt_salindex102_temperatureitem_1_stddev FLOAT,
	mt_salindex102_temperatureitem_1_min FLOAT,
	mt_salindex102_temperatureitem_1_max FLOAT,
	mt_salindex102_temperatureitem_2_mean FLOAT,
	mt_salindex102_temperatureitem_2_stddev FLOAT,
	mt_salindex102_temperatureitem_2_min FLOAT,
	mt_salindex102_temperatureitem_2_max FLOAT,
	mt_salindex102_temperatureitem_3_mean FLOAT,
	mt_salindex102_temperatureitem_3_stddev FLOAT,
	mt_salindex102_temperatureitem_3_min FLOAT,
	mt_salindex102_temperatureitem_3_max FLOAT,
	mt_salindex102_temperatureitem_4_mean FLOAT,
	mt_salindex102_temperatureitem_4_stddev FLOAT,
	mt_salindex102_temperatureitem_4_min FLOAT,
	mt_salindex102_temperatureitem_4_max FLOAT,
	mt_salindex102_temperatureitem_5_mean FLOAT,
	mt_salindex102_temperatureitem_5_stddev FLOAT,
	mt_salindex102_temperatureitem_5_min FLOAT,
	mt_salindex102_temperatureitem_5_max FLOAT,
	mt_salindex102_temperatureitem_6_mean FLOAT,
	mt_salindex102_temperatureitem_6_stddev FLOAT,
	mt_salindex102_temperatureitem_6_min FLOAT,
	mt_salindex102_temperatureitem_6_max FLOAT,
	mt_salindex102_temperatureitem_7_mean FLOAT,
	mt_salindex102_temperatureitem_7_stddev FLOAT,
	mt_salindex102_temperatureitem_7_min FLOAT,
	mt_salindex102_temperatureitem_7_max FLOAT,
	mt_salindex103_temperatureitem_0_mean FLOAT,
	mt_salindex103_temperatureitem_0_stddev FLOAT,
	mt_salindex103_temperatureitem_0_min FLOAT,
	mt_salindex103_temperatureitem_1_mean FLOAT,
	mt_salindex103_temperatureitem_0_max FLOAT,
	mt_salindex103_temperatureitem_1_stddev FLOAT,
	mt_salindex103_temperatureitem_1_min FLOAT,
	mt_salindex103_temperatureitem_1_max FLOAT,
	mt_salindex103_temperatureitem_2_mean FLOAT,
	mt_salindex103_temperatureitem_2_stddev FLOAT,
	mt_salindex103_temperatureitem_2_min FLOAT,
	mt_salindex103_temperatureitem_2_max FLOAT,
	mt_salindex103_temperatureitem_3_mean FLOAT,
	mt_salindex103_temperatureitem_3_stddev FLOAT,
	mt_salindex103_temperatureitem_3_min FLOAT,
	mt_salindex103_temperatureitem_3_max FLOAT,
	mt_salindex103_temperatureitem_4_mean FLOAT,
	mt_salindex103_temperatureitem_4_stddev FLOAT,
	mt_salindex103_temperatureitem_4_min FLOAT,
	mt_salindex103_temperatureitem_4_max FLOAT,
	mt_salindex103_temperatureitem_5_mean FLOAT,
	mt_salindex103_temperatureitem_5_stddev FLOAT,
	mt_salindex103_temperatureitem_5_min FLOAT,
	mt_salindex103_temperatureitem_5_max FLOAT,
	mt_salindex103_temperatureitem_6_mean FLOAT,
	mt_salindex103_temperatureitem_6_stddev FLOAT,
	mt_salindex103_temperatureitem_6_min FLOAT,
	mt_salindex103_temperatureitem_6_max FLOAT,
	mt_salindex103_temperatureitem_7_mean FLOAT,
	mt_salindex103_temperatureitem_7_stddev FLOAT,
	mt_salindex103_temperatureitem_7_min FLOAT,
	mt_salindex103_temperatureitem_7_max FLOAT,
	mt_salindex106_temperatureitem_0_mean FLOAT,
	mt_salindex106_temperatureitem_0_stddev FLOAT,
	mt_salindex106_temperatureitem_0_min FLOAT,
	mt_salindex106_temperatureitem_1_mean FLOAT,
	mt_salindex106_temperatureitem_0_max FLOAT,
	mt_salindex106_temperatureitem_1_stddev FLOAT,
	mt_salindex106_temperatureitem_1_min FLOAT,
	mt_salindex106_temperatureitem_1_max FLOAT,
	mt_salindex106_temperatureitem_2_mean FLOAT,
	mt_salindex106_temperatureitem_2_stddev FLOAT,
	mt_salindex106_temperatureitem_2_min FLOAT,
	mt_salindex106_temperatureitem_2_max FLOAT,
	mt_salindex106_temperatureitem_3_mean FLOAT,
	mt_salindex106_temperatureitem_3_stddev FLOAT,
	mt_salindex106_temperatureitem_3_min FLOAT,
	mt_salindex106_temperatureitem_3_max FLOAT,
	mt_salindex106_temperatureitem_4_mean FLOAT,
	mt_salindex106_temperatureitem_4_stddev FLOAT,
	mt_salindex106_temperatureitem_4_min FLOAT,
	mt_salindex106_temperatureitem_4_max FLOAT,
	mt_salindex106_temperatureitem_5_mean FLOAT,
	mt_salindex106_temperatureitem_5_stddev FLOAT,
	mt_salindex106_temperatureitem_5_min FLOAT,
	mt_salindex106_temperatureitem_5_max FLOAT,
	mt_salindex106_temperatureitem_6_mean FLOAT,
	mt_salindex106_temperatureitem_6_stddev FLOAT,
	mt_salindex106_temperatureitem_6_min FLOAT,
	mt_salindex106_temperatureitem_6_max FLOAT,
	mt_salindex106_temperatureitem_7_mean FLOAT,
	mt_salindex106_temperatureitem_7_stddev FLOAT,
	mt_salindex106_temperatureitem_7_min FLOAT,
	mt_salindex106_temperatureitem_7_max FLOAT,
	mt_salindex107_temperatureitem_0_mean FLOAT,
	mt_salindex107_temperatureitem_0_stddev FLOAT,
	mt_salindex107_temperatureitem_0_min FLOAT,
	mt_salindex107_temperatureitem_1_mean FLOAT,
	mt_salindex107_temperatureitem_0_max FLOAT,
	mt_salindex107_temperatureitem_1_stddev FLOAT,
	mt_salindex107_temperatureitem_1_min FLOAT,
	mt_salindex107_temperatureitem_1_max FLOAT,
	mt_salindex107_temperatureitem_2_mean FLOAT,
	mt_salindex107_temperatureitem_2_stddev FLOAT,
	mt_salindex107_temperatureitem_2_min FLOAT,
	mt_salindex107_temperatureitem_2_max FLOAT,
	mt_salindex107_temperatureitem_3_mean FLOAT,
	mt_salindex107_temperatureitem_3_stddev FLOAT,
	mt_salindex107_temperatureitem_3_min FLOAT,
	mt_salindex107_temperatureitem_3_max FLOAT,
	mt_salindex107_temperatureitem_4_mean FLOAT,
	mt_salindex107_temperatureitem_4_stddev FLOAT,
	mt_salindex107_temperatureitem_4_min FLOAT,
	mt_salindex107_temperatureitem_4_max FLOAT,
	mt_salindex107_temperatureitem_5_mean FLOAT,
	mt_salindex107_temperatureitem_5_stddev FLOAT,
	mt_salindex107_temperatureitem_5_min FLOAT,
	mt_salindex107_temperatureitem_5_max FLOAT,
	mt_salindex107_temperatureitem_6_mean FLOAT,
	mt_salindex107_temperatureitem_6_stddev FLOAT,
	mt_salindex107_temperatureitem_6_min FLOAT,
	mt_salindex107_temperatureitem_6_max FLOAT,
	mt_salindex107_temperatureitem_7_mean FLOAT,
	mt_salindex107_temperatureitem_7_stddev FLOAT,
	mt_salindex107_temperatureitem_7_min FLOAT,
	mt_salindex107_temperatureitem_7_max FLOAT,
	mt_salindex108_temperatureitem_0_mean FLOAT,
	mt_salindex108_temperatureitem_0_stddev FLOAT,
	mt_salindex108_temperatureitem_0_min FLOAT,
	mt_salindex108_temperatureitem_1_mean FLOAT,
	mt_salindex108_temperatureitem_0_max FLOAT,
	mt_salindex108_temperatureitem_1_stddev FLOAT,
	mt_salindex108_temperatureitem_1_min FLOAT,
	mt_salindex108_temperatureitem_1_max FLOAT,
	mt_salindex108_temperatureitem_2_mean FLOAT,
	mt_salindex108_temperatureitem_2_stddev FLOAT,
	mt_salindex108_temperatureitem_2_min FLOAT,
	mt_salindex108_temperatureitem_2_max FLOAT,
	mt_salindex108_temperatureitem_3_mean FLOAT,
	mt_salindex108_temperatureitem_3_stddev FLOAT,
	mt_salindex108_temperatureitem_3_min FLOAT,
	mt_salindex108_temperatureitem_3_max FLOAT,
	mt_salindex108_temperatureitem_4_mean FLOAT,
	mt_salindex108_temperatureitem_4_stddev FLOAT,
	mt_salindex108_temperatureitem_4_min FLOAT,
	mt_salindex108_temperatureitem_4_max FLOAT,
	mt_salindex108_temperatureitem_5_mean FLOAT,
	mt_salindex108_temperatureitem_5_stddev FLOAT,
	mt_salindex108_temperatureitem_5_min FLOAT,
	mt_salindex108_temperatureitem_5_max FLOAT,
	mt_salindex108_temperatureitem_6_mean FLOAT,
	mt_salindex108_temperatureitem_6_stddev FLOAT,
	mt_salindex108_temperatureitem_6_min FLOAT,
	mt_salindex108_temperatureitem_6_max FLOAT,
	mt_salindex108_temperatureitem_7_mean FLOAT,
	mt_salindex108_temperatureitem_7_stddev FLOAT,
	mt_salindex108_temperatureitem_7_min FLOAT,
	mt_salindex108_temperatureitem_7_max FLOAT,
	mt_salindex301_temperatureitem_0_mean FLOAT,
	mt_salindex301_temperatureitem_0_stddev FLOAT,
	mt_salindex301_temperatureitem_0_min FLOAT,
	mt_salindex301_temperatureitem_1_mean FLOAT,
	mt_salindex301_temperatureitem_0_max FLOAT,
	mt_salindex301_temperatureitem_1_stddev FLOAT,
	mt_salindex301_temperatureitem_1_min FLOAT,
	mt_salindex301_temperatureitem_1_max FLOAT,
	mt_salindex301_temperatureitem_2_mean FLOAT,
	mt_salindex301_temperatureitem_2_stddev FLOAT,
	mt_salindex301_temperatureitem_2_min FLOAT,
	mt_salindex301_temperatureitem_2_max FLOAT,
	mt_salindex301_temperatureitem_3_mean FLOAT,
	mt_salindex301_temperatureitem_3_stddev FLOAT,
	mt_salindex301_temperatureitem_3_min FLOAT,
	mt_salindex301_temperatureitem_3_max FLOAT,
	mt_salindex301_temperatureitem_4_mean FLOAT,
	mt_salindex301_temperatureitem_4_stddev FLOAT,
	mt_salindex301_temperatureitem_4_min FLOAT,
	mt_salindex301_temperatureitem_4_max FLOAT,
	mt_salindex301_temperatureitem_5_mean FLOAT,
	mt_salindex301_temperatureitem_5_stddev FLOAT,
	mt_salindex301_temperatureitem_5_min FLOAT,
	mt_salindex301_temperatureitem_5_max FLOAT,
	mt_salindex301_temperatureitem_6_mean FLOAT,
	mt_salindex301_temperatureitem_6_stddev FLOAT,
	mt_salindex301_temperatureitem_6_min FLOAT,
	mt_salindex301_temperatureitem_6_max FLOAT,
	mt_salindex301_temperatureitem_7_mean FLOAT,
	mt_salindex301_temperatureitem_7_stddev FLOAT,
	mt_salindex301_temperatureitem_7_min FLOAT,
	mt_salindex301_temperatureitem_7_max FLOAT,
	mt_dimm_fwhm_mean FLOAT,
	mt_azimuth_encoder_absolute_position0_mean FLOAT,
	mt_azimuth_encoder_absolute_position1_mean FLOAT,
	mt_azimuth_encoder_absolute_position2_mean FLOAT,
	mt_azimuth_encoder_absolute_position3_mean FLOAT,
	mt_elevation_encoder_absolute_position0_mean FLOAT,
	mt_elevation_encoder_absolute_position1_mean FLOAT,
	mt_elevation_encoder_absolute_position2_mean FLOAT,
	mt_elevation_encoder_absolute_position3_mean FLOAT,
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
	mt_salindex104_acceleration_x_mean FLOAT,
	mt_salindex104_acceleration_x_stddev FLOAT,
	mt_salindex104_acceleration_x_min FLOAT,
	mt_salindex104_acceleration_x_max FLOAT,
	mt_salindey104_acceleration_y_mean FLOAT,
	mt_salindex104_acceleration_y_stddev FLOAT,
	mt_salindex104_acceleration_y_min FLOAT,
	mt_salindex104_acceleration_y_max FLOAT,
	mt_salindez104_acceleration_z_mean FLOAT,
	mt_salindex104_acceleration_z_stddev FLOAT,
	mt_salindex104_acceleration_z_min FLOAT,
	mt_salindex104_acceleration_z_max FLOAT,
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
	PRIMARY KEY (visit_id, instrument),
	CONSTRAINT un_visit_id_instrument UNIQUE (visit_id, instrument)
)

;
COMMENT ON TABLE cdb_lsstcomcam.visit1_efd IS 'Transformed EFD topics by visit.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.visit_id IS 'Visit unique ID.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.created_at IS 'Timestamp when the record was created, default is the current timestamp';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.instrument IS 'Instrument name.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_sonic_temperature_mean IS 'Median sonic temperature (air temperature measured sonically). Sonic temperature has poor absolute accuracy (it can be off by several degrees) but good time resolution.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_sonic_temperature_stddev IS 'Median sonic temperature (air temperature measured sonically). Sonic temperature has poor absolute accuracy (it can be off by several degrees) but good time resolution.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.at_salindex110_sonic_temperature_stddev_mean IS 'Standard devation of sonic temperature (air temperature measured sonically) estimated from quartiles.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.at_salindex110_sonic_temperature_stddev_stddev IS 'Standard devation of sonic temperature (air temperature measured sonically) estimated from quartiles.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_wind_speed_0_mean IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 0 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_wind_speed_0_stddev IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 0 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_wind_speed_0_min IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 0 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_wind_speed_0_max IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 0 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_wind_speed_1_mean IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 1 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_wind_speed_1_stddev IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 1 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_wind_speed_1_min IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 1 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_wind_speed_1_max IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 1 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_wind_speed_2_mean IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 2 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_wind_speed_2_stddev IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 2 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_wind_speed_2_min IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 2 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_wind_speed_2_max IS 'Median wind speed (x, y, z) in TMA-GillLabJack01 along axis 2 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_wind_speed_speedstddev_0_mean IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 0 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_wind_speed_speedstddev_0_stddev IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 0 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_wind_speed_speedstddev_0_min IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 0 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_wind_speed_speedstddev_0_max IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 0 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_wind_speed_speedstddev_1_mean IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 1 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_wind_speed_speedstddev_1_stddev IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 1 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_wind_speed_speedstddev_1_min IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 1 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_wind_speed_speedstddev_1_max IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 1 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_wind_speed_speedstddev_2_mean IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 2 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_wind_speed_speedstddev_2_stddev IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 2 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_wind_speed_speedstddev_2_min IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 2 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_wind_speed_speedstddev_2_max IS 'Standard deviation of wind speed (x, y, z) estimated from quartiles in TMA-GillLabJack01 along axis 2 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_wind_speed_magnitude_mean IS 'Median wind speed magnitude in TMA-GillLabJack01 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_wind_speed_magnitude_stddev IS 'Median wind speed magnitude in TMA-GillLabJack01 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_wind_speed_magnitude_min IS 'Median wind speed magnitude in TMA-GillLabJack01 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_wind_speed_magnitude_max IS 'Median wind speed magnitude in TMA-GillLabJack01 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_wind_speed_maxmagnitude_mean IS 'Maximum wind speed magnitude in TMA-GillLabJack01 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_wind_speed_maxmagnitude_stddev IS 'Maximum wind speed magnitude in TMA-GillLabJack01 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_wind_speed_maxmagnitude_min IS 'Maximum wind speed magnitude in TMA-GillLabJack01 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex110_wind_speed_maxmagnitude_max IS 'Maximum wind speed magnitude in TMA-GillLabJack01 (salIndex 110)';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex1_temperatureitem_0_mean IS 'MTCameraAssembly-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex1_temperatureitem_0_stddev IS 'MTCameraAssembly-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex1_temperatureitem_0_min IS 'MTCameraAssembly-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex1_temperatureitem_1_mean IS 'MTCameraAssembly-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex1_temperatureitem_0_max IS 'MTCameraAssembly-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex1_temperatureitem_1_stddev IS 'MTCameraAssembly-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex1_temperatureitem_1_min IS 'MTCameraAssembly-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex1_temperatureitem_1_max IS 'MTCameraAssembly-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex1_temperatureitem_2_mean IS 'MTCameraAssembly-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex1_temperatureitem_2_stddev IS 'MTCameraAssembly-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex1_temperatureitem_2_min IS 'MTCameraAssembly-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex1_temperatureitem_2_max IS 'MTCameraAssembly-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex1_temperatureitem_3_mean IS 'MTCameraAssembly-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex1_temperatureitem_3_stddev IS 'MTCameraAssembly-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex1_temperatureitem_3_min IS 'MTCameraAssembly-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex1_temperatureitem_3_max IS 'MTCameraAssembly-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex1_temperatureitem_4_mean IS 'MTCameraAssembly-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex1_temperatureitem_4_stddev IS 'MTCameraAssembly-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex1_temperatureitem_4_min IS 'MTCameraAssembly-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex1_temperatureitem_4_max IS 'MTCameraAssembly-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex1_temperatureitem_5_mean IS 'MTCameraAssembly-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex1_temperatureitem_5_stddev IS 'MTCameraAssembly-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex1_temperatureitem_5_min IS 'MTCameraAssembly-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex1_temperatureitem_5_max IS 'MTCameraAssembly-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex1_temperatureitem_6_mean IS 'MTCameraAssembly-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex1_temperatureitem_6_stddev IS 'MTCameraAssembly-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex1_temperatureitem_6_min IS 'MTCameraAssembly-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex1_temperatureitem_6_max IS 'MTCameraAssembly-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex1_temperatureitem_7_mean IS 'MTCameraAssembly-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex1_temperatureitem_7_stddev IS 'MTCameraAssembly-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex1_temperatureitem_7_min IS 'MTCameraAssembly-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex1_temperatureitem_7_max IS 'MTCameraAssembly-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex101_temperatureitem_0_mean IS 'MTCameraAssembly-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex101_temperatureitem_0_stddev IS 'MTCameraAssembly-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex101_temperatureitem_0_min IS 'MTCameraAssembly-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex101_temperatureitem_1_mean IS 'MTCameraAssembly-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex101_temperatureitem_0_max IS 'MTCameraAssembly-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex101_temperatureitem_1_stddev IS 'MTCameraAssembly-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex101_temperatureitem_1_min IS 'MTCameraAssembly-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex101_temperatureitem_1_max IS 'MTCameraAssembly-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex101_temperatureitem_2_mean IS 'MTCameraAssembly-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex101_temperatureitem_2_stddev IS 'MTCameraAssembly-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex101_temperatureitem_2_min IS 'MTCameraAssembly-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex101_temperatureitem_2_max IS 'MTCameraAssembly-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex101_temperatureitem_3_mean IS 'MTCameraAssembly-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex101_temperatureitem_3_stddev IS 'MTCameraAssembly-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex101_temperatureitem_3_min IS 'MTCameraAssembly-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex101_temperatureitem_3_max IS 'MTCameraAssembly-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex101_temperatureitem_4_mean IS 'MTCameraAssembly-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex101_temperatureitem_4_stddev IS 'MTCameraAssembly-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex101_temperatureitem_4_min IS 'MTCameraAssembly-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex101_temperatureitem_4_max IS 'MTCameraAssembly-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex101_temperatureitem_5_mean IS 'MTCameraAssembly-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex101_temperatureitem_5_stddev IS 'MTCameraAssembly-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex101_temperatureitem_5_min IS 'MTCameraAssembly-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex101_temperatureitem_5_max IS 'MTCameraAssembly-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex101_temperatureitem_6_mean IS 'MTCameraAssembly-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex101_temperatureitem_6_stddev IS 'MTCameraAssembly-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex101_temperatureitem_6_min IS 'MTCameraAssembly-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex101_temperatureitem_6_max IS 'MTCameraAssembly-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex101_temperatureitem_7_mean IS 'MTCameraAssembly-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex101_temperatureitem_7_stddev IS 'MTCameraAssembly-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex101_temperatureitem_7_min IS 'MTCameraAssembly-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex101_temperatureitem_7_max IS 'MTCameraAssembly-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex102_temperatureitem_0_mean IS 'temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex102_temperatureitem_0_stddev IS 'temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex102_temperatureitem_0_min IS 'temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex102_temperatureitem_1_mean IS 'temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex102_temperatureitem_0_max IS 'temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex102_temperatureitem_1_stddev IS 'temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex102_temperatureitem_1_min IS 'temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex102_temperatureitem_1_max IS 'temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex102_temperatureitem_2_mean IS 'temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex102_temperatureitem_2_stddev IS 'temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex102_temperatureitem_2_min IS 'temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex102_temperatureitem_2_max IS 'temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex102_temperatureitem_3_mean IS 'temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex102_temperatureitem_3_stddev IS 'temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex102_temperatureitem_3_min IS 'temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex102_temperatureitem_3_max IS 'temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex102_temperatureitem_4_mean IS 'temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex102_temperatureitem_4_stddev IS 'temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex102_temperatureitem_4_min IS 'temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex102_temperatureitem_4_max IS 'temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex102_temperatureitem_5_mean IS 'temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex102_temperatureitem_5_stddev IS 'temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex102_temperatureitem_5_min IS 'temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex102_temperatureitem_5_max IS 'temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex102_temperatureitem_6_mean IS 'temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex102_temperatureitem_6_stddev IS 'temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex102_temperatureitem_6_min IS 'temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex102_temperatureitem_6_max IS 'temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex102_temperatureitem_7_mean IS 'temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex102_temperatureitem_7_stddev IS 'temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex102_temperatureitem_7_min IS 'temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex102_temperatureitem_7_max IS 'temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex103_temperatureitem_0_mean IS 'temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex103_temperatureitem_0_stddev IS 'temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex103_temperatureitem_0_min IS 'temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex103_temperatureitem_1_mean IS 'temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex103_temperatureitem_0_max IS 'temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex103_temperatureitem_1_stddev IS 'temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex103_temperatureitem_1_min IS 'temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex103_temperatureitem_1_max IS 'temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex103_temperatureitem_2_mean IS 'temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex103_temperatureitem_2_stddev IS 'temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex103_temperatureitem_2_min IS 'temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex103_temperatureitem_2_max IS 'temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex103_temperatureitem_3_mean IS 'temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex103_temperatureitem_3_stddev IS 'temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex103_temperatureitem_3_min IS 'temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex103_temperatureitem_3_max IS 'temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex103_temperatureitem_4_mean IS 'temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex103_temperatureitem_4_stddev IS 'temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex103_temperatureitem_4_min IS 'temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex103_temperatureitem_4_max IS 'temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex103_temperatureitem_5_mean IS 'temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex103_temperatureitem_5_stddev IS 'temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex103_temperatureitem_5_min IS 'temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex103_temperatureitem_5_max IS 'temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex103_temperatureitem_6_mean IS 'temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex103_temperatureitem_6_stddev IS 'temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex103_temperatureitem_6_min IS 'temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex103_temperatureitem_6_max IS 'temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex103_temperatureitem_7_mean IS 'temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex103_temperatureitem_7_stddev IS 'temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex103_temperatureitem_7_min IS 'temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex103_temperatureitem_7_max IS 'temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex106_temperatureitem_0_mean IS 'M2-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex106_temperatureitem_0_stddev IS 'M2-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex106_temperatureitem_0_min IS 'M2-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex106_temperatureitem_1_mean IS 'M2-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex106_temperatureitem_0_max IS 'M2-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex106_temperatureitem_1_stddev IS 'M2-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex106_temperatureitem_1_min IS 'M2-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex106_temperatureitem_1_max IS 'M2-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex106_temperatureitem_2_mean IS 'M2-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex106_temperatureitem_2_stddev IS 'M2-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex106_temperatureitem_2_min IS 'M2-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex106_temperatureitem_2_max IS 'M2-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex106_temperatureitem_3_mean IS 'M2-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex106_temperatureitem_3_stddev IS 'M2-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex106_temperatureitem_3_min IS 'M2-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex106_temperatureitem_3_max IS 'M2-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex106_temperatureitem_4_mean IS 'M2-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex106_temperatureitem_4_stddev IS 'M2-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex106_temperatureitem_4_min IS 'M2-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex106_temperatureitem_4_max IS 'M2-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex106_temperatureitem_5_mean IS 'M2-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex106_temperatureitem_5_stddev IS 'M2-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex106_temperatureitem_5_min IS 'M2-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex106_temperatureitem_5_max IS 'M2-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex106_temperatureitem_6_mean IS 'M2-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex106_temperatureitem_6_stddev IS 'M2-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex106_temperatureitem_6_min IS 'M2-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex106_temperatureitem_6_max IS 'M2-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex106_temperatureitem_7_mean IS 'M2-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex106_temperatureitem_7_stddev IS 'M2-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex106_temperatureitem_7_min IS 'M2-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex106_temperatureitem_7_max IS 'M2-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex107_temperatureitem_0_mean IS 'Laser-ESS01, Laser-ESS02 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex107_temperatureitem_0_stddev IS 'Laser-ESS01, Laser-ESS02 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex107_temperatureitem_0_min IS 'Laser-ESS01, Laser-ESS02 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex107_temperatureitem_1_mean IS 'Laser-ESS01, Laser-ESS02 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex107_temperatureitem_0_max IS 'Laser-ESS01, Laser-ESS02 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex107_temperatureitem_1_stddev IS 'Laser-ESS01, Laser-ESS02 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex107_temperatureitem_1_min IS 'Laser-ESS01, Laser-ESS02 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex107_temperatureitem_1_max IS 'Laser-ESS01, Laser-ESS02 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex107_temperatureitem_2_mean IS 'Laser-ESS01, Laser-ESS02 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex107_temperatureitem_2_stddev IS 'Laser-ESS01, Laser-ESS02 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex107_temperatureitem_2_min IS 'Laser-ESS01, Laser-ESS02 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex107_temperatureitem_2_max IS 'Laser-ESS01, Laser-ESS02 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex107_temperatureitem_3_mean IS 'Laser-ESS01, Laser-ESS02 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex107_temperatureitem_3_stddev IS 'Laser-ESS01, Laser-ESS02 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex107_temperatureitem_3_min IS 'Laser-ESS01, Laser-ESS02 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex107_temperatureitem_3_max IS 'Laser-ESS01, Laser-ESS02 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex107_temperatureitem_4_mean IS 'Laser-ESS01, Laser-ESS02 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex107_temperatureitem_4_stddev IS 'Laser-ESS01, Laser-ESS02 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex107_temperatureitem_4_min IS 'Laser-ESS01, Laser-ESS02 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex107_temperatureitem_4_max IS 'Laser-ESS01, Laser-ESS02 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex107_temperatureitem_5_mean IS 'Laser-ESS01, Laser-ESS02 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex107_temperatureitem_5_stddev IS 'Laser-ESS01, Laser-ESS02 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex107_temperatureitem_5_min IS 'Laser-ESS01, Laser-ESS02 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex107_temperatureitem_5_max IS 'Laser-ESS01, Laser-ESS02 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex107_temperatureitem_6_mean IS 'Laser-ESS01, Laser-ESS02 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex107_temperatureitem_6_stddev IS 'Laser-ESS01, Laser-ESS02 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex107_temperatureitem_6_min IS 'Laser-ESS01, Laser-ESS02 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex107_temperatureitem_6_max IS 'Laser-ESS01, Laser-ESS02 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex107_temperatureitem_7_mean IS 'Laser-ESS01, Laser-ESS02 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex107_temperatureitem_7_stddev IS 'Laser-ESS01, Laser-ESS02 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex107_temperatureitem_7_min IS 'Laser-ESS01, Laser-ESS02 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex107_temperatureitem_7_max IS 'Laser-ESS01, Laser-ESS02 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex108_temperatureitem_0_mean IS 'CBP-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex108_temperatureitem_0_stddev IS 'CBP-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex108_temperatureitem_0_min IS 'CBP-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex108_temperatureitem_1_mean IS 'CBP-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex108_temperatureitem_0_max IS 'CBP-ESS01 temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex108_temperatureitem_1_stddev IS 'CBP-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex108_temperatureitem_1_min IS 'CBP-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex108_temperatureitem_1_max IS 'CBP-ESS01 temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex108_temperatureitem_2_mean IS 'CBP-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex108_temperatureitem_2_stddev IS 'CBP-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex108_temperatureitem_2_min IS 'CBP-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex108_temperatureitem_2_max IS 'CBP-ESS01 temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex108_temperatureitem_3_mean IS 'CBP-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex108_temperatureitem_3_stddev IS 'CBP-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex108_temperatureitem_3_min IS 'CBP-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex108_temperatureitem_3_max IS 'CBP-ESS01 temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex108_temperatureitem_4_mean IS 'CBP-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex108_temperatureitem_4_stddev IS 'CBP-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex108_temperatureitem_4_min IS 'CBP-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex108_temperatureitem_4_max IS 'CBP-ESS01 temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex108_temperatureitem_5_mean IS 'CBP-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex108_temperatureitem_5_stddev IS 'CBP-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex108_temperatureitem_5_min IS 'CBP-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex108_temperatureitem_5_max IS 'CBP-ESS01 temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex108_temperatureitem_6_mean IS 'CBP-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex108_temperatureitem_6_stddev IS 'CBP-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex108_temperatureitem_6_min IS 'CBP-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex108_temperatureitem_6_max IS 'CBP-ESS01 temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex108_temperatureitem_7_mean IS 'CBP-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex108_temperatureitem_7_stddev IS 'CBP-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex108_temperatureitem_7_min IS 'CBP-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex108_temperatureitem_7_max IS 'CBP-ESS01 temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex301_temperatureitem_0_mean IS 'Weather tower air temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex301_temperatureitem_0_stddev IS 'Weather tower air temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex301_temperatureitem_0_min IS 'Weather tower air temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex301_temperatureitem_1_mean IS 'Weather tower air temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex301_temperatureitem_0_max IS 'Weather tower air temperature item 0';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex301_temperatureitem_1_stddev IS 'Weather tower air temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex301_temperatureitem_1_min IS 'Weather tower air temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex301_temperatureitem_1_max IS 'Weather tower air temperature item 1';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex301_temperatureitem_2_mean IS 'Weather tower air temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex301_temperatureitem_2_stddev IS 'Weather tower air temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex301_temperatureitem_2_min IS 'Weather tower air temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex301_temperatureitem_2_max IS 'Weather tower air temperature item 2';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex301_temperatureitem_3_mean IS 'Weather tower air temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex301_temperatureitem_3_stddev IS 'Weather tower air temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex301_temperatureitem_3_min IS 'Weather tower air temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex301_temperatureitem_3_max IS 'Weather tower air temperature item 3';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex301_temperatureitem_4_mean IS 'Weather tower air temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex301_temperatureitem_4_stddev IS 'Weather tower air temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex301_temperatureitem_4_min IS 'Weather tower air temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex301_temperatureitem_4_max IS 'Weather tower air temperature item 4';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex301_temperatureitem_5_mean IS 'Weather tower air temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex301_temperatureitem_5_stddev IS 'Weather tower air temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex301_temperatureitem_5_min IS 'Weather tower air temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex301_temperatureitem_5_max IS 'Weather tower air temperature item 5';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex301_temperatureitem_6_mean IS 'Weather tower air temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex301_temperatureitem_6_stddev IS 'Weather tower air temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex301_temperatureitem_6_min IS 'Weather tower air temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex301_temperatureitem_6_max IS 'Weather tower air temperature item 6';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex301_temperatureitem_7_mean IS 'Weather tower air temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex301_temperatureitem_7_stddev IS 'Weather tower air temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex301_temperatureitem_7_min IS 'Weather tower air temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex301_temperatureitem_7_max IS 'Weather tower air temperature item 7';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_dimm_fwhm_mean IS 'Combined full width half maximum';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_azimuth_encoder_absolute_position0_mean IS 'Azimuth absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_azimuth_encoder_absolute_position1_mean IS 'Azimuth absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_azimuth_encoder_absolute_position2_mean IS 'Azimuth absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_azimuth_encoder_absolute_position3_mean IS 'Azimuth absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_elevation_encoder_absolute_position0_mean IS 'Elevation absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_elevation_encoder_absolute_position1_mean IS 'Elevation absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_elevation_encoder_absolute_position2_mean IS 'Elevation absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_elevation_encoder_absolute_position3_mean IS 'Elevation absolute position read by each encoder head.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_hexapod_uncompensated_position_u_mean IS 'U angle.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_hexapod_uncompensated_position_u_max IS 'U angle.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_hexapod_uncompensated_position_u_min IS 'U angle.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_hexapod_uncompensated_position_v_mean IS 'V angle.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_hexapod_uncompensated_position_v_max IS 'V angle.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_hexapod_uncompensated_position_v_min IS 'V angle.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_hexapod_uncompensated_position_w_mean IS 'W angle.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_hexapod_uncompensated_position_w_max IS 'W angle.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_hexapod_uncompensated_position_w_min IS 'W angle.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_hexapod_uncompensated_position_x_mean IS 'X position.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_hexapod_uncompensated_position_x_max IS 'X position.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_hexapod_uncompensated_position_x_min IS 'X position.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_hexapod_uncompensated_position_y_mean IS 'Y position.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_hexapod_uncompensated_position_y_max IS 'Y position.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_hexapod_uncompensated_position_y_min IS 'Y position.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_hexapod_uncompensated_position_z_mean IS 'Z position.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_hexapod_uncompensated_position_z_max IS 'Z position.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_hexapod_uncompensated_position_z_min IS 'Z position.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex104_acceleration_x_mean IS 'Acceleration in x direction in SST top end ring +x -y, SST top end ring -x -y, SST spider spindle, SST M2 surrogate.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex104_acceleration_x_stddev IS 'Acceleration in x direction in SST top end ring +x -y, SST top end ring -x -y, SST spider spindle, SST M2 surrogate.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex104_acceleration_x_min IS 'Acceleration in x direction in SST top end ring +x -y, SST top end ring -x -y, SST spider spindle, SST M2 surrogate.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex104_acceleration_x_max IS 'Acceleration in x direction in SST top end ring +x -y, SST top end ring -x -y, SST spider spindle, SST M2 surrogate.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindey104_acceleration_y_mean IS 'Acceleration in y direction in SST top end ring +x -y, SST top end ring -x -y, SST spider spindle, SST M2 surrogate.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex104_acceleration_y_stddev IS 'Acceleration in y direction in SST top end ring +x -y, SST top end ring -x -y, SST spider spindle, SST M2 surrogate.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex104_acceleration_y_min IS 'Acceleration in y direction in SST top end ring +x -y, SST top end ring -x -y, SST spider spindle, SST M2 surrogate.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex104_acceleration_y_max IS 'Acceleration in y direction in SST top end ring +x -y, SST top end ring -x -y, SST spider spindle, SST M2 surrogate.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindez104_acceleration_z_mean IS 'Acceleration in z direction in SST top end ring +x -y, SST top end ring -x -y, SST spider spindle, SST M2 surrogate.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex104_acceleration_z_stddev IS 'Acceleration in z direction in SST top end ring +x -y, SST top end ring -x -y, SST spider spindle, SST M2 surrogate.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex104_acceleration_z_min IS 'Acceleration in z direction in SST top end ring +x -y, SST top end ring -x -y, SST spider spindle, SST M2 surrogate.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_salindex104_acceleration_z_max IS 'Acceleration in z direction in SST top end ring +x -y, SST top end ring -x -y, SST spider spindle, SST M2 surrogate.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_pointing_mount_position_ra_mean IS 'RA calculated from the azimuthActualPosition and elevationActualPosition.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_pointing_mount_position_ra_stddev IS 'RA calculated from the azimuthActualPosition and elevationActualPosition.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_pointing_mount_position_dec_mean IS 'Dec calculated from the azimuthActualPosition and elevationActualPosition.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_pointing_mount_position_dec_stddev IS 'Dec calculated from the azimuthActualPosition and elevationActualPosition.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_pointing_mount_position_sky_angle_mean IS 'Calculated sky angle.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_pointing_mount_position_sky_angle_stddev IS 'Calculated sky angle.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_pointing_mount_position_rotator_mean IS 'Rotator axis position reported by rotator component.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.mt_pointing_mount_position_rotator_stddev IS 'Rotator axis position reported by rotator component.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.camera_hexapod_aos_corrections_u IS 'U position offset.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.camera_hexapod_aos_corrections_v IS 'V position offset.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.camera_hexapod_aos_corrections_w IS 'W position offset.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.camera_hexapod_aos_corrections_x IS 'X position offset.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.camera_hexapod_aos_corrections_y IS 'Y position offset.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.camera_hexapod_aos_corrections_z IS 'Z position offset.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.m2_hexapod_aos_corrections_u IS 'U position offset.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.m2_hexapod_aos_corrections_v IS 'V position offset.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.m2_hexapod_aos_corrections_w IS 'W position offset.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.m2_hexapod_aos_corrections_x IS 'X position offset.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.m2_hexapod_aos_corrections_y IS 'Y position offset.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.m2_hexapod_aos_corrections_z IS 'Z position offset.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.m2_stress IS 'Calculate M2 stress computed RSS the stress contribution of each bending mode.';
COMMENT ON COLUMN cdb_lsstcomcam.visit1_efd.m1m3_stress IS 'Calculate M1M3 stress computed RSS the stress contribution of each bending mode.';
COMMENT ON CONSTRAINT un_visit_id_instrument ON cdb_lsstcomcam.visit1_efd IS 'Ensure visit_id is unique.';

CREATE TABLE cdb_lsstcomcam.transformed_efd_scheduler (
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
COMMENT ON TABLE cdb_lsstcomcam.transformed_efd_scheduler IS 'Transformed EFD scheduler.';
COMMENT ON COLUMN cdb_lsstcomcam.transformed_efd_scheduler.id IS 'Unique ID, auto-incremented';
COMMENT ON COLUMN cdb_lsstcomcam.transformed_efd_scheduler.start_time IS 'Start time of the transformation interval, must be provided';
COMMENT ON COLUMN cdb_lsstcomcam.transformed_efd_scheduler.end_time IS 'End time of the transformation interval, must be provided';
COMMENT ON COLUMN cdb_lsstcomcam.transformed_efd_scheduler.timewindow IS 'Time window used to expand start and end times by, in minutes';
COMMENT ON COLUMN cdb_lsstcomcam.transformed_efd_scheduler.status IS 'Status of the process, default is ''pending''';
COMMENT ON COLUMN cdb_lsstcomcam.transformed_efd_scheduler.process_start_time IS 'Timestamp when the process started';
COMMENT ON COLUMN cdb_lsstcomcam.transformed_efd_scheduler.process_end_time IS 'Timestamp when the process ended';
COMMENT ON COLUMN cdb_lsstcomcam.transformed_efd_scheduler.process_exec_time IS 'Execution time of the process in seconds, default is 0';
COMMENT ON COLUMN cdb_lsstcomcam.transformed_efd_scheduler.exposures IS 'Number of exposures processed, default is 0';
COMMENT ON COLUMN cdb_lsstcomcam.transformed_efd_scheduler.visits1 IS 'Number of visits recorded, default is 0';
COMMENT ON COLUMN cdb_lsstcomcam.transformed_efd_scheduler.retries IS 'Number of retries attempted, default is 0';
COMMENT ON COLUMN cdb_lsstcomcam.transformed_efd_scheduler.error IS 'Error message, if any';
COMMENT ON COLUMN cdb_lsstcomcam.transformed_efd_scheduler.created_at IS 'Timestamp when the record was created, default is the current timestamp';
COMMENT ON CONSTRAINT un_id ON cdb_lsstcomcam.transformed_efd_scheduler IS 'Ensure id is unique.';
