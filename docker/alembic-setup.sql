-- Database environment expected by the consdb alembic migrations:
--   * cdb schema for alembic version bookkeeping
--   * pg_sphere extension for the pgs_region column
--   * usdf and oods roles referenced by GRANTs in the migrations
--
-- CREATE USER has no IF NOT EXISTS form; on a re-run it errors with
-- "role already exists" and psql continues to the next statement.

CREATE SCHEMA IF NOT EXISTS "cdb";
CREATE EXTENSION IF NOT EXISTS pg_sphere;
CREATE USER "usdf";
CREATE USER "oods";
