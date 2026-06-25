"""Per-instrument table consistency rules.

Each query takes a single ``:day_obs`` bind parameter and returns one row per
rule violation, with the columns:

``rule``
    The name of the consistency rule that failed.
``day_obs``, ``seq_num``
    The exposure the violation belongs to.
``detail``
    A short human-readable description of the specific violation.

The rules are documented in ``doc/operator-guide/monitoring.rst``.
Relationships already guaranteed by the database schema (primary keys,
unique keys, and the ``*_quicklook`` foreign keys) are intentionally not
re-checked here.
"""

CONSISTENCY_QUERIES = {
    "lsstcam": """
    WITH ccdexposure_completeness AS (
        -- Structural: every exposure has exactly 205 ccdexposure rows (0-204).
        SELECT
            'ccdexposure_completeness' AS rule,
            e.day_obs,
            e.seq_num,
            'expected 205 ccdexposure rows for detectors 0-204, found '
                || COUNT(c.detector) AS detail
        FROM cdb_lsstcam.exposure AS e
        LEFT JOIN cdb_lsstcam.ccdexposure AS c
            ON c.exposure_id = e.exposure_id
        WHERE e.day_obs = :day_obs
        GROUP BY e.day_obs, e.seq_num
        HAVING COUNT(c.detector) <> 205
            OR MIN(c.detector) <> 0
            OR MAX(c.detector) <> 204
            OR COALESCE(SUM(c.detector), -1) <> 20910
    ),
    exposure_id_encoding AS (
        -- Structural: exposure_id = day_obs * 100000 + seq_num.
        SELECT
            'exposure_id_encoding' AS rule,
            e.day_obs,
            e.seq_num,
            'exposure_id ' || e.exposure_id
                || ' <> day_obs * 100000 + seq_num' AS detail
        FROM cdb_lsstcam.exposure AS e
        WHERE e.day_obs = :day_obs
            AND e.exposure_id <> e.day_obs::bigint * 100000 + e.seq_num
    ),
    ccdexposure_key_agreement AS (
        -- Structural: a ccdexposure row's (day_obs, seq_num) must match the
        -- exposure it references through exposure_id.
        SELECT
            'ccdexposure_key_agreement' AS rule,
            e.day_obs,
            e.seq_num,
            'ccdexposure_id ' || c.ccdexposure_id
                || ' day_obs/seq_num disagree with exposure_id '
                || c.exposure_id AS detail
        FROM cdb_lsstcam.ccdexposure AS c
        JOIN cdb_lsstcam.exposure AS e
            ON e.exposure_id = c.exposure_id
        WHERE e.day_obs = :day_obs
            AND (c.day_obs <> e.day_obs OR c.seq_num <> e.seq_num)
    ),
    no_guider_products AS (
        -- Structural: guider detectors never carry derived imaging products.
        SELECT
            'no_guider_products' AS rule,
            c.day_obs,
            c.seq_num,
            'guider detector ' || c.detector
                || ' has a ccdexposure_quicklook row' AS detail
        FROM cdb_lsstcam.ccdexposure AS c
        JOIN cdb_lsstcam.ccdexposure_quicklook AS q
            ON q.ccdexposure_id = c.ccdexposure_id
        WHERE c.day_obs = :day_obs
            AND c.detector IN (189, 190, 193, 194, 197, 198, 201, 202)
        UNION ALL
        SELECT
            'no_guider_products' AS rule,
            c.day_obs,
            c.seq_num,
            'guider detector ' || c.detector
                || ' has a ccdvisit1_quicklook row' AS detail
        FROM cdb_lsstcam.ccdexposure AS c
        JOIN cdb_lsstcam.ccdvisit1_quicklook AS v
            ON v.ccdvisit_id = c.ccdexposure_id
        WHERE c.day_obs = :day_obs
            AND c.detector IN (189, 190, 193, 194, 197, 198, 201, 202)
    ),
    exposure_quicklook_coverage AS (
        -- Coverage: one exposure_quicklook row per on-sky exposure.
        SELECT
            'exposure_quicklook_coverage' AS rule,
            e.day_obs,
            e.seq_num,
            'missing exposure_quicklook row' AS detail
        FROM cdb_lsstcam.exposure AS e
        WHERE e.day_obs = :day_obs
            AND e.img_type IN ('science', 'acq', 'cwfs', 'focus', 'engtest')
            AND NOT EXISTS (
                SELECT 1
                FROM cdb_lsstcam.exposure_quicklook AS eq
                WHERE eq.exposure_id = e.exposure_id
            )
    ),
    visit1_quicklook_coverage AS (
        -- Coverage: one visit1_quicklook row per exposure (except indome/test).
        SELECT
            'visit1_quicklook_coverage' AS rule,
            e.day_obs,
            e.seq_num,
            'missing visit1_quicklook row' AS detail
        FROM cdb_lsstcam.exposure AS e
        WHERE e.day_obs = :day_obs
            AND e.img_type NOT IN ('indome', 'test')
            AND NOT EXISTS (
                SELECT 1
                FROM cdb_lsstcam.visit1_quicklook AS vq
                WHERE vq.visit_id = e.exposure_id
            )
    ),
    ccdexposure_quicklook_coverage AS (
        -- Coverage: 197 ccdexposure_quicklook rows per imaging exposure
        -- (189 for cwfs).
        SELECT
            'ccdexposure_quicklook_coverage' AS rule,
            t.day_obs,
            t.seq_num,
            'expected ' || t.expected || ' ccdexposure_quicklook rows, found '
                || t.found AS detail
        FROM (
            SELECT
                e.day_obs,
                e.seq_num,
                CASE WHEN e.img_type = 'cwfs' THEN 189 ELSE 197 END AS expected,
                COUNT(ceq.ccdexposure_id) AS found
            FROM cdb_lsstcam.exposure AS e
            JOIN cdb_lsstcam.ccdexposure AS c
                ON c.exposure_id = e.exposure_id
            LEFT JOIN cdb_lsstcam.ccdexposure_quicklook AS ceq
                ON ceq.ccdexposure_id = c.ccdexposure_id
            WHERE e.day_obs = :day_obs
                AND e.img_type NOT IN ('indome', 'test')
            GROUP BY e.day_obs, e.seq_num, e.img_type
        ) AS t
        WHERE t.found < t.expected
    ),
    ccdvisit1_quicklook_coverage AS (
        -- Coverage: 193 ccdvisit1_quicklook rows per on-sky science exposure
        -- (189 science detectors + 4 single-sided corner wavefront sensors).
        SELECT
            'ccdvisit1_quicklook_coverage' AS rule,
            t.day_obs,
            t.seq_num,
            'expected 193 ccdvisit1_quicklook rows, found ' || t.found AS detail
        FROM (
            SELECT
                e.day_obs,
                e.seq_num,
                COUNT(cvq.ccdvisit_id) AS found
            FROM cdb_lsstcam.exposure AS e
            JOIN cdb_lsstcam.ccdexposure AS c
                ON c.exposure_id = e.exposure_id
            LEFT JOIN cdb_lsstcam.ccdvisit1_quicklook AS cvq
                ON cvq.ccdvisit_id = c.ccdexposure_id
            WHERE e.day_obs = :day_obs
                AND e.img_type IN ('science', 'acq')
            GROUP BY e.day_obs, e.seq_num
        ) AS t
        WHERE t.found < 193
    ),
    no_calibration_science_products AS (
        -- Coverage: bias/flat/dark frames must have no ccdvisit1_quicklook rows.
        SELECT
            'no_calibration_science_products' AS rule,
            e.day_obs,
            e.seq_num,
            'calibration frame has ' || COUNT(cvq.ccdvisit_id)
                || ' ccdvisit1_quicklook rows' AS detail
        FROM cdb_lsstcam.exposure AS e
        JOIN cdb_lsstcam.ccdexposure AS c
            ON c.exposure_id = e.exposure_id
        JOIN cdb_lsstcam.ccdvisit1_quicklook AS cvq
            ON cvq.ccdvisit_id = c.ccdexposure_id
        WHERE e.day_obs = :day_obs
            AND e.img_type IN ('bias', 'flat', 'dark')
        GROUP BY e.day_obs, e.seq_num
    )
    SELECT rule, day_obs, seq_num, detail FROM ccdexposure_completeness
    UNION ALL
    SELECT rule, day_obs, seq_num, detail FROM exposure_id_encoding
    UNION ALL
    SELECT rule, day_obs, seq_num, detail FROM ccdexposure_key_agreement
    UNION ALL
    SELECT rule, day_obs, seq_num, detail FROM no_guider_products
    UNION ALL
    SELECT rule, day_obs, seq_num, detail FROM exposure_quicklook_coverage
    UNION ALL
    SELECT rule, day_obs, seq_num, detail FROM visit1_quicklook_coverage
    UNION ALL
    SELECT rule, day_obs, seq_num, detail FROM ccdexposure_quicklook_coverage
    UNION ALL
    SELECT rule, day_obs, seq_num, detail FROM ccdvisit1_quicklook_coverage
    UNION ALL
    SELECT rule, day_obs, seq_num, detail FROM no_calibration_science_products
    ORDER BY rule, day_obs, seq_num
    """,
    "latiss": """
    WITH ccdexposure_completeness AS (
        -- Structural: LATISS is single-detector; expect exactly one
        -- ccdexposure row for detector 0.
        SELECT
            'ccdexposure_completeness' AS rule,
            e.day_obs,
            e.seq_num,
            'expected 1 ccdexposure row for detector 0, found '
                || COUNT(c.detector) AS detail
        FROM cdb_latiss.exposure AS e
        LEFT JOIN cdb_latiss.ccdexposure AS c
            ON c.exposure_id = e.exposure_id
        WHERE e.day_obs = :day_obs
        GROUP BY e.day_obs, e.seq_num
        HAVING COUNT(c.detector) <> 1
            OR COALESCE(MIN(c.detector), -1) <> 0
            OR COALESCE(MAX(c.detector), -1) <> 0
    ),
    exposure_id_encoding AS (
        SELECT
            'exposure_id_encoding' AS rule,
            e.day_obs,
            e.seq_num,
            'exposure_id ' || e.exposure_id
                || ' <> day_obs * 100000 + seq_num' AS detail
        FROM cdb_latiss.exposure AS e
        WHERE e.day_obs = :day_obs
            AND e.exposure_id <> e.day_obs::bigint * 100000 + e.seq_num
    ),
    ccdexposure_key_agreement AS (
        SELECT
            'ccdexposure_key_agreement' AS rule,
            e.day_obs,
            e.seq_num,
            'ccdexposure_id ' || c.ccdexposure_id
                || ' day_obs/seq_num disagree with exposure_id '
                || c.exposure_id AS detail
        FROM cdb_latiss.ccdexposure AS c
        JOIN cdb_latiss.exposure AS e
            ON e.exposure_id = c.exposure_id
        WHERE e.day_obs = :day_obs
            AND (c.day_obs <> e.day_obs OR c.seq_num <> e.seq_num)
    ),
    exposure_quicklook_coverage AS (
        SELECT
            'exposure_quicklook_coverage' AS rule,
            e.day_obs,
            e.seq_num,
            'missing exposure_quicklook row' AS detail
        FROM cdb_latiss.exposure AS e
        WHERE e.day_obs = :day_obs
            AND e.img_type = 'science'
            AND NOT EXISTS (
                SELECT 1
                FROM cdb_latiss.exposure_quicklook AS eq
                WHERE eq.exposure_id = e.exposure_id
            )
    )
    SELECT rule, day_obs, seq_num, detail FROM ccdexposure_completeness
    UNION ALL
    SELECT rule, day_obs, seq_num, detail FROM exposure_id_encoding
    UNION ALL
    SELECT rule, day_obs, seq_num, detail FROM ccdexposure_key_agreement
    UNION ALL
    SELECT rule, day_obs, seq_num, detail FROM exposure_quicklook_coverage
    ORDER BY rule, day_obs, seq_num
    """,
}
