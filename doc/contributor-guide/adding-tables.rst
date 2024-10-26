##############
Adding Tables
##############

- Each source of data should have its own table(s).
- Conversely, each new table being added should have its data source identified.
- Each dimension combination (exposure, visit, exposure+detector, visit+detector, etc.) should have its own table(s).
- Normalize when possible.  Try not to repeat non-key columns between tables with the same dimensions.
- De-normalize via views to make querying easier.
