CONSISTENCY_QUERIES = {
    "lsstcam": """
    WITH exposure_quicklook_missing AS (
        SELECT
            'exposure_quicklook' AS table_name,
            e.day_obs,
            e.seq_num,
            1 - COUNT(eq.exposure_id) AS num_rows_missing
        FROM cdb_lsstcam.exposure AS e
        LEFT JOIN cdb_lsstcam.exposure_quicklook AS eq
            ON eq.exposure_id = e.exposure_id
        WHERE e.day_obs = :day_obs
        GROUP BY e.day_obs, e.seq_num
        HAVING COUNT(eq.exposure_id) < 1
    ),
    visit1_quicklook_missing AS (
        SELECT
            'visit1_quicklook' AS table_name,
            v.day_obs,
            v.seq_num,
            1 - COUNT(vq.visit_id) AS num_rows_missing
        FROM cdb_lsstcam.visit1 AS v
        LEFT JOIN cdb_lsstcam.visit1_quicklook AS vq
            ON vq.visit_id = v.visit_id
        WHERE v.day_obs = :day_obs
        GROUP BY v.day_obs, v.seq_num
        HAVING COUNT(vq.visit_id) < 1
    ),
    ccdvisit1_quicklook_missing AS (
        SELECT
            'ccdvisit1_quicklook' AS table_name,
            v.day_obs,
            v.seq_num,
            193 - COUNT(cvq.ccdvisit_id) AS num_rows_missing
        FROM cdb_lsstcam.visit1 AS v
        LEFT JOIN cdb_lsstcam.ccdvisit1 AS cv
            ON cv.visit_id = v.visit_id
        LEFT JOIN cdb_lsstcam.ccdvisit1_quicklook AS cvq
            ON cvq.ccdvisit_id = cv.ccdvisit_id
        WHERE v.day_obs = :day_obs
        GROUP BY v.day_obs, v.seq_num
        HAVING COUNT(cvq.ccdvisit_id) < 193
    ),
    ccdexposure_quicklook_missing AS (
        SELECT
            'ccdexposure_quicklook' AS table_name,
            e.day_obs,
            e.seq_num,
            CASE
                WHEN e.img_type = 'cwfs' THEN 189
                ELSE 197
            END - COUNT(ceq.ccdexposure_id) AS num_rows_missing
        FROM cdb_lsstcam.exposure AS e
        LEFT JOIN cdb_lsstcam.ccdexposure AS ce
            ON ce.exposure_id = e.exposure_id
        LEFT JOIN cdb_lsstcam.ccdexposure_quicklook AS ceq
            ON ceq.ccdexposure_id = ce.ccdexposure_id
        WHERE e.day_obs = :day_obs
        GROUP BY e.day_obs, e.seq_num, e.img_type
        HAVING COUNT(ceq.ccdexposure_id) < CASE
            WHEN e.img_type = 'cwfs' THEN 189
            ELSE 197
        END
    )
    SELECT table_name, day_obs, seq_num, num_rows_missing
    FROM exposure_quicklook_missing
    UNION ALL
    SELECT table_name, day_obs, seq_num, num_rows_missing
    FROM visit1_quicklook_missing
    UNION ALL
    SELECT table_name, day_obs, seq_num, num_rows_missing
    FROM ccdvisit1_quicklook_missing
    UNION ALL
    SELECT table_name, day_obs, seq_num, num_rows_missing
    FROM ccdexposure_quicklook_missing
    ORDER BY table_name, day_obs, seq_num
    """,
    "latiss": """
    WITH exposure_quicklook_missing AS (
        SELECT
            'exposure_quicklook' AS table_name,
            e.day_obs,
            e.seq_num,
            1 - COUNT(eq.exposure_id) AS num_rows_missing
        FROM cdb_latiss.exposure AS e
        LEFT JOIN cdb_latiss.exposure_quicklook AS eq
            ON eq.exposure_id = e.exposure_id
        WHERE e.day_obs = :day_obs
        GROUP BY e.day_obs, e.seq_num
        HAVING COUNT(eq.exposure_id) < 1
    )
    SELECT table_name, day_obs, seq_num, num_rows_missing
    FROM exposure_quicklook_missing
    ORDER BY table_name, day_obs, seq_num
    """,
}
