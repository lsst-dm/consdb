########################
Schema Migration Process
########################

* How to add columns to sdm_schemas
edit the repository at <link to sdm_schemas>
check that valid sql tables can be created with felis

* Create an Alembic Migration
  <link to alembic>
  Alembic keeps track of our versioning so we can keep the test stands and summit databases in sync. Alembic helps to
  autogenerate the code to move from one version to the next. Versioning our changes to the database schema in this way
  helps us quickly apply schema edits and move the database's status forward and backward in time, dependent on issues and
   upgrades.

  * How to create an alembic migration to create a db version that includes your new sdm_schema edits
    We have created a script to aid with the generation of alembic migrations: consdb/alembic-autogenerate.py
    To use this script, you will need to have some local environment variables set.

    Have a local clone of sdm_schemas that includes your cdb_* schema changes. Set the environment variable ???
    SDM_SCHEMA to point to this repository so our autogenerate_alembic.py script will be able to reference the appropriate target schema configuration.

    You must have access to the database you want to create a new version on. This access can be defined through setting
    the database url environment variable (is it DB_URL or POSTGRES_URL)
    "postgresql://DB_NAME:DB_PASS@postgresdb01.tu.lsst.org/DB_NAME" or 'postgresdb01.ls.lsst.org' or something else
    depending on the location of the db you're trying to access

    specify which db table and which schema, to autogenerate those version upgrades.

    Running the alembic-autogenerate script will create some version files in the respective database named directories
    in consdb

* Test alembic migration and code to populate the new columns/tables at TTS/BTS if Summit schema is changing
  You will need to test your consdb branch before merging it to main or before applying the database changes to the
  the Summit.
  Choose the appropriate test stand (TTS), create a branch in phalanx, and edit the
  `phalanx/applications/consdb/values-<test stand>.yaml`` file to point to your branch name instead of the tagged
  version of the software.
  Update the consdb deployment in `<teststand>/argo-cd` to use your phalanx branch as the 'Target Revision'. Refresh the deployments and check the pod logs.
  (Make sure you have access to the test stand you are using, VPN, etc) Access the database via your terminal of choice
  using the database url environment variable above with `psql`. Using `psql`, verify the tables to upgrade exist.
  From within the consdb/ directory, where there is an alembic subdirectory, use the alembic commands to upgrade the
  database `alembic upgrade head -n <database name>`. The database names are cdb_latiss, cdb_* and otherwise noted
  <link to existing db tables in intro page>
  Once both the new consdb software is deployed (hinfo, pqserver) and the database tables have been updated, we can test by taking an image with LATISS.
  Access LOVE via `<teststand>/love` and use the 1Password admin information to sign in. Navigate to the ATQueue or Auxilary Telescope (AuxTel) Script Queue.
  See <links for using script queue and tts> for guidelines on using the test stands.
  Before editing these scripts, note their starting configurations, as we will return the configuration to that when we are done.
  Take a test/simulated picture with LATISS through the ATQueue using these three scripts:
  1. `set_summary_state.py` Change the configuration to enable ATHeaderService and ATCamera.
  2. `enable_latiss.py` Remove any existing configuration.
  3. `take_image_latiss.py` Update the configuration to remove anything that is not 'nimages' (1) and 'image_type' (ENGTEST)

   Once you have put these three scripts in the queue, click `run`.
   Pay attention to any errors that show up from the scripts.
   If there are no errors, check the argo-cd consdb application pod logs for the hinfo-latiss deployment.
   Note any errors. If there are none, and you expect an image to have successfully made it into the database, check the
   database by using `psql` commands like `\dt` to display the table names and maybe even
   `SELECT * from cdb_latiss.exposure where day_obs == <YYYYMMDD>;` to view the most recent data.
   If you have encountered errors in this process, do not proceed to the summit, but address those errors and retest
   them with your phalanx branch pointing to your consdb branch with the updates (that fix the errors).

* Deploy migration in synchrony at Summit (if necessary), USDF, and Prompt Release (if necessary)
* Deploy code to populate at Summit and/or USDF
If you have not already followed the directions above for testing alembic migration and code at TTS/BTS, follow those testing steps before the directions below.
To deploy code at the Summit, you'll follow similar steps as above, with access to argo-cd deployments via the Summit OpenVPN, but will need more coordination with the observers and site teams.
When you are ready to deploy an update to the summit, you'll need to go to CAP (acronym?) meeting on Tuesday mornings and announce your request. You can also add it to the agenda here: https://rubinobs.atlassian.net/wiki/spaces/LSSTCOM/pages/53765933/Agenda+Items+for+Future+CAP+Meetings
The CAP members will likely tell you a time frame that is acceptable for you to perform these changes. They may also tell you specific people to coordinate with to help you take images to test LATISS and LSSTCOMCAMSIM tables. There will be more tables to test eventually.
Some important channels to note: #rubinobs-test-planning; #summit-announce; #summit-auxtel, <add more here>.

When you get your final approval and time to perform the changes to ConsDb, make sure to announce on #summit-announce, and follow similar steps as test stand procedure above.
1. Use a branch in phalanx to point to the consdb tag you wish to make active.
2. Set the argo-cd application consdb's target revision to your phalanx branch.
3. Refresh the consdb application's deployment. Review the pods' logs.
4. Have an image be taken by coordinating with the observing team, and review the pods' logs again.
5. Check in the database using a jupyter notebook or SQL query in RSP that your new image has been inserted to the database as expected.
