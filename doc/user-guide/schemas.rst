############
Schemas
############

* Types of schemas
    * Summit for observers and Summit systems
        * Smallest, contains primary key information from HeaderService and additional information from other Summit systems, including experimental and engineering data
    * USDF for staff and analytical uses
        * Largest, contains a full replica of the Summit plus additional information from USDF systems including Prompt Processing and Data Release Production, possibly Calibration Products Production, and human annotations from processing campaigns
    * Release for science users
        * Near-real-time "prompt" ConsDB replicates a subset of the USDF version
        * Data Release ConsDB is a snapshot of a subset of the USDF version with data pertaining to the exposures/visits in the DR
* Schema browser
