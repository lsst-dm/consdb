###########
Monitoring
###########

Reporting channels
==================

- Users of ConsDB, ConsDBClient (``pqserver``) will usually report via #consolidated-database in rubin-obs.slack.com when they are having issues.
- ConsDB operators should monitor this channel and #ops-usdf, #ops-usdf-alerts for issues and outages reported, as well as escalate verified database issues.

Database
========

- The ConsDB team is responsible for verifying whether or not the database is up when issues are reported
  - They can check the method reported by the users, check using ``psql``/ ``pgcli``, and check in the #ops-usdf slack channel for currently reported issues.

- Once the ConsDB team has confirmed there is an issue with the database, they should notify #ops-usdf slack channel and USDF DBAs should be responsible for fixing/restarting.

REST API Server
===============

- If we suspect the API server died, the ConsDB team should be responsible for checking and restarting
- Use the appropriate argo-cd deployment graph to check deployment logs, and potentially restart the service.


Other issues
------------

- K8s infrastructure died The ConsDB team can verify that that is the problem, but there are likely to be wider issues seen
- USDF or Summit K8s/IT support should be responsible for fixing.
