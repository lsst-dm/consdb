############
Schema Migration Process
############

* Add columns to sdm_schemas
* Create alembic migration
* Test migration and code to populate the new columns/tables at TTS/BTS if Summit schema is changing
* Deploy migration in synchrony at Summit (if necessary), USDF, and Prompt Release (if necessary)
* Deploy code to populate at Summit and/or USDF

