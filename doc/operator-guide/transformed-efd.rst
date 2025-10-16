Transformed EFD
===============

This guide shows how to deploy the Transformed EFD service to staging or production environments. The service processes EFD telemetry data into database tables for analysis, running as Kubernetes jobs or cronjobs.

**What this service does**: Transforms raw Engineering and Facilities Database (EFD) telemetry into structured, queryable metrics organized by exposure and visit timespans.

**Deployment options**:

- **One-time Jobs**: Process specific date ranges or historical data
- **CronJobs**: Continuous processing for ongoing telemetry transformation
- **Failure Monitors**: Automatic retry mechanisms for failed processing tasks

**Supported Instruments**: LATISS, LSSTCam, LSSTComCam

Prerequisites
-------------

**Cluster Access and Context**

- Access to the appropriate Kubernetes cluster with deployment permissions
- Correct kubectl context set: ``usdf-consdb-dev`` (development) or ``usdf-consdb`` (production)
- Verify with: ``kubectl config current-context``

**Repository Access**

- Clone the deployment repository: ``git clone https://github.com/slaclab/usdf-consdb-deploy.git``
- Navigate to the repository directory before running deployment commands

**Vault Authentication**

- Vault CLI installed and configured
- Valid Vault credentials for the target environment
- Network access to the Vault server
- Test with: ``vault status``

**Required Tools**

- ``kubectl`` (configured and tested)
- ``make`` (usually pre-installed)
- ``vault`` CLI tool

**Environment-Specific Requirements**

- **Development**: Access to dev cluster, dev Vault secrets, embargoed Butler data
- **Production**: Access to prod cluster, prod Vault secrets, embargoed Butler data



Quick Reference for Experienced Users
-------------------------------------

.. note::
   **For users familiar with Kubernetes and this service**: Jump directly to the deployment commands below. See the detailed sections for explanations and troubleshooting.

**Deploy Job (one-time processing):**

.. code-block:: bash

   cd kubernetes/overlays/dev/latiss-job
   make apply file=job.yaml embargo=true

**Deploy CronJob (continuous processing):**

.. code-block:: bash

   cd kubernetes/overlays/dev/latiss-cronjob
   make apply file=cronjob.yaml embargo=true

**Check deployment status:**

.. code-block:: bash

   kubectl get pods -n dev-latiss
   kubectl get jobs -n dev-latiss

**View logs:**

.. code-block:: bash

   kubectl logs <pod-name> -n dev-latiss


Deploy to Development
---------------------

1. **Set Kubernetes Context**

   Use context ``usdf-consdb-dev`` for development.

2. **Get Vault Access**

   .. code-block:: bash

      export VAULT_ADDR=<your-vault-url>
      vault login -method ldap -username <your-username>

3. **Deploy a Job (one-time processing)**

   .. code-block:: bash

      cd kubernetes/overlays/dev/latiss-job
      make apply file=job.yaml embargo=true

4. **Deploy a CronJob (continuous processing)**

   .. code-block:: bash

      cd kubernetes/overlays/dev/latiss-cronjob
      make apply file=cronjob.yaml embargo=true

Deploy to Production
--------------------

Same steps as development, but use ``prod`` directories:

1. **Set Kubernetes Context**

   Use context ``usdf-consdb`` for production.

2. **Deploy Job**

   .. code-block:: bash

      cd kubernetes/overlays/prod/latiss-job
      make apply file=job.yaml embargo=true

3. **Deploy CronJob**

   .. code-block:: bash

      cd kubernetes/overlays/prod/latiss-cronjob
      make apply file=cronjob.yaml embargo=true

Available Instruments
---------------------

- **LATISS**: ``latiss-job`` or ``latiss-cronjob``
- **LSSTCam**: ``lsstcam-job`` or ``lsstcam-cronjob``
- **LSSTComCam**: ``lsstcomcam-job`` or ``lsstcomcam-cronjob``

Configuration Files
-------------------

Each instrument has its own directory with these files:

- ``job.yaml`` - One-time processing job
- ``cronjob.yaml`` - Continuous processing
- ``failure-monitor.yaml`` - Special CronJob that retries failed tasks hourly
- ``kustomization.yaml`` - Kustomize configuration

**Multiple Configuration Files**

Each directory can contain multiple job and cronjob files with different configurations:

- ``job-recent.yaml`` - Process recent data (last 24 hours)
- ``job-historical.yaml`` - Process historical data (specific date range)

**Important Settings**:

- ``DATETIME_START`` / ``DATETIME_END`` - Time range to process (Jobs only)
- ``TIMEDELTA`` - Processing chunk size in minutes (default: 5)
- ``TIMEWINDOW`` - Overlap between chunks in minutes (default: 1)
- ``EFD_PATH`` - Specific InfluxDB instance path (optional, for different database instances)

Configuration Examples
~~~~~~~~~~~~~~~~~~~~~~

**Complete Job Example - Process LATISS data from Oct 1-2, 2025 using different InfluxDB**

.. code-block:: yaml

   apiVersion: batch/v1
   kind: Job
   metadata:
     name: transformed-efd-latiss-job-historical
   spec:
     template:
       spec:
         containers:
         - name: processor
           image: ghcr.io/lsst-dm/consdb-transformed-efd:latest
           env:
           - name: INSTRUMENT
             value: "LATISS"
           - name: CONFIG_FILE
             value: "/opt/lsst/software/stack/python/lsst/consdb/transformed_efd/config/config_latiss.yaml"
           - name: DATETIME_START
             value: "2025-10-01T00:00:00"
           - name: DATETIME_END
             value: "2025-10-02T00:00:00"
           - name: TIMEDELTA
             value: "5"
           - name: TIMEWINDOW
             value: "1"
           - name: MODE
             value: "job"
           - name: BUTLER_REPO
             value: "s3://embargo@rubin-summit-users/butler.yaml"
           - name: CONSDB_URL
             valueFrom:
               secretKeyRef:
                 name: efd-transform-secrets
                 key: consdb-url-dev
           - name: EFD_PASSWORD
             valueFrom:
               secretKeyRef:
                 name: efd-transform-secrets
                 key: usdf-efd-password
           - name: EFD_PATH
             value: "influxdb-enterprise-standby-data"
         restartPolicy: Never

**Complete CronJob Example - Continuous LATISS processing every hour**

.. code-block:: yaml

   apiVersion: batch/v1
   kind: CronJob
   metadata:
     name: transformed-efd-latiss-cronjob-hourly
   spec:
     schedule: "0 * * * *"
     jobTemplate:
       spec:
         template:
           spec:
             containers:
             - name: processor
               image: ghcr.io/lsst-dm/consdb-transformed-efd:latest
               env:
               - name: INSTRUMENT
                 value: "LATISS"
               - name: CONFIG_FILE
                 value: "/opt/lsst/software/stack/python/lsst/consdb/transformed_efd/config/config_latiss.yaml"
               - name: MODE
                 value: "cronjob"
               - name: TIMEDELTA
                 value: "5"
               - name: TIMEWINDOW
                 value: "1"
               - name: BUTLER_REPO
                 value: "s3://embargo@rubin-summit-users/butler.yaml"
               - name: CONSDB_URL
                 valueFrom:
                   secretKeyRef:
                     name: efd-transform-secrets
                     key: consdb-url-dev
               - name: EFD_PASSWORD
                 valueFrom:
                   secretKeyRef:
                     name: efd-transform-secrets
                     key: usdf-efd-password
             restartPolicy: OnFailure

Working with Multiple Configurations
------------------------------------

**Different Use Cases**:

- **Recent Data**: ``job-recent.yaml`` - Process last 24 hours of data
- **Historical Data**: ``job-historical.yaml`` - Process specific date ranges
- **Hourly Processing**: ``cronjob-hourly.yaml`` - Continuous processing every hour

**Deploy Specific Configurations**:

.. code-block:: bash

   # Deploy recent data processing job
   make apply file=job-recent.yaml embargo=true

   # Deploy historical data processing job
   make apply file=job-historical.yaml embargo=true

   # Deploy hourly CronJob
   make apply file=cronjob-hourly.yaml embargo=true


**Customize Your Own Files**:

1. Copy an existing file: ``cp job.yaml my-custom-job.yaml``
2. Edit the configuration: ``nano my-custom-job.yaml``
3. Deploy your custom configuration: ``make apply file=my-custom-job.yaml embargo=true``

Makefile Parameters
-------------------

The Makefile handles secret management and deployment with these key parameters:

**file=<config-file>**

- Specifies which YAML configuration file to use
- Example: ``file=job.yaml``, ``file=cronjob.yaml``, ``file=failure-monitor.yaml``

**embargo=<true|false>**

- Controls which Butler database password is fetched from Vault
- **Default**: ``embargo=true``
- **embargo=true**: Uses embargoed data access
- **embargo=false**: Uses public data access

Makefile Workflow
~~~~~~~~~~~~~~~~~

The ``make apply`` command executes these steps:

1. **get-secrets-from-vault**: Fetches secrets from Vault

   - Downloads all required secrets to temporary directory
   - Automatically selects Butler password based on embargo setting

2. **link-patch**: Links your config file

   - Creates symbolic link: ``<your-file> → patch.yaml``
   - Required for Kustomize to apply your configuration

3. **run-apply**: Applies to Kubernetes

   - Executes ``kubectl apply -k .``
   - Uses Kustomize to merge base + overlay + your patch

4. **clean-secrets**: Cleanup

   - Removes temporary secrets directory

Examples:

.. code-block:: bash

   # Process embargoed data (default)
   make apply file=job.yaml embargo=true

   # Process public data
   make apply file=job.yaml embargo=false

   # Deploy CronJob with embargoed access
   make apply file=cronjob.yaml embargo=true

   # Deploy failure monitor with public access
   make apply file=failure-monitor.yaml embargo=false

Secret Management
-----------------

The Makefile fetches these secrets from Vault:

**Required Secrets:**

- AWS credentials for S3 access
- Database connection strings
- S3 profile configurations
- EFD InfluxDB password

**Conditional Butler Passwords:**

- Embargoed Butler password (used when ``embargo=true``)
- Main Butler password (used when ``embargo=false``)

**Vault Paths:**

- **Development**: Environment-specific Vault path for dev secrets
- **Production**: Environment-specific Vault path for prod secrets

**Secret Flow:**

1. Makefile reads ``embargo`` parameter
2. Selects appropriate Butler password key
3. Fetches all secrets from Vault
4. Stores in temporary secrets directory
5. Kustomize generates Kubernetes secrets
6. Temporary files are cleaned up

Namespaces
----------

Jobs deploy to these namespaces:

**Development**:

- ``dev-latiss``
- ``dev-lsstcam``
- ``dev-lsstcomcam``

**Production**:

- ``prod-latiss``
- ``prod-lsstcam``
- ``prod-lsstcomcam``

Scheduler Tables and Task Management
------------------------------------

The transformed EFD system uses a dedicated ``efd_scheduler`` schema to coordinate processing tasks across all instruments. Understanding this schema is essential for monitoring and troubleshooting the service.

**Scheduler Schema Structure**

The ``efd_scheduler`` schema contains separate tables for each instrument:

- **efd_scheduler.latiss**: LATISS instrument task management
- **efd_scheduler.lsstcam**: LSSTCam instrument task management
- **efd_scheduler.lsstcomcam**: LSSTComCam instrument task management

This schema is shared across all environments (development and production).

**Key Table Columns**:

- **id**: Unique task identifier (auto-incrementing)
- **start_time/end_time**: Processing time window boundaries
- **status**: Task state (pending, idle, running, completed, failed)
- **process_start_time/process_end_time**: Execution timestamps
- **exposures/visits1**: Processing counts and metrics
- **retries**: Number of retry attempts
- **error**: Error messages for failed tasks
- **butler_repo**: Butler repository path used

**Task Status Lifecycle**:

1. **pending**: Default status for CronJob tasks, ready for processing
2. **idle**: Status for Job tasks, ready for processing
3. **running**: Task currently being processed
4. **completed**: Task finished successfully
5. **failed**: Task failed with error (eligible for retry)
6. **stale**: Task marked as stale after 72 hours (no longer eligible for retry)

**Execution Mode Differences**:

- **Jobs**: Create tasks with "idle" status for one-time processing
- **CronJobs**: Create tasks with "pending" status for continuous processing


Failure Monitor
---------------

The failure monitor is a special CronJob that runs hourly to retry failed tasks:

**How it works**:

- Runs every hour (``"0 * * * *"`` schedule)
- Uses ``--resume`` flag to retry failed tasks
- Implements exponential backoff (2.8^retries hours wait time)
- Maximum 3 retries per task
- Tasks older than 72 hours are marked as "stale" status and no longer eligible for retry

**Deploy failure monitor**:

.. code-block:: bash

   make apply file=failure-monitor.yaml embargo=true

**Check failed tasks**:

.. code-block:: bash

   kubectl get jobs -n <namespace> | grep Failed

Check Deployment Status
-----------------------

1. **List pods**

.. code-block:: bash

   kubectl get pods -n dev-latiss

2. **Check job status**

.. code-block:: bash

   kubectl get jobs -n dev-latiss

3. **View logs**

.. code-block:: bash

   kubectl logs <pod-name> -n dev-latiss

4. **Check CronJob schedule**

.. code-block:: bash

   kubectl get cronjobs -n dev-latiss

Common Issues
-------------

**Setup Issues**

**kubectl context errors**:
- Run: ``kubectl config get-contexts`` to see available contexts
- Switch context: ``kubectl config use-context usdf-consdb-dev``
- Verify: ``kubectl config current-context``

**Vault authentication failures**:
- Check Vault server accessibility: ``vault status``
- Re-authenticate: ``vault login -method ldap -username <your-username>``
- Verify permissions for the target environment

**Repository access issues**:
- Ensure you're in the correct directory: ``pwd``
- Check repository structure: ``ls kubernetes/overlays/dev/``
- Verify you have the latest code: ``git pull``

**Deployment Issues**

**Job hangs**:

- Check logs: ``kubectl logs <pod-name> -n <namespace>``
- Verify time range has data
- Check database connectivity

**CronJob not running**:

- Check schedule: ``kubectl describe cronjob <name> -n <namespace>``
- Look for failed jobs: ``kubectl get jobs -n <namespace>``

**Failed tasks not retrying**:

- Deploy failure monitor: ``make apply file=failure-monitor.yaml embargo=true``
- Check failure monitor logs: ``kubectl logs <failure-monitor-pod> -n <namespace>``
- Verify exponential backoff timing (2.8^retries hours between retries)

**Scheduler table issues**:

- Check for orphaned tasks: Query tasks stuck in "running" status
- Verify task creation: Ensure new tasks are being created for cronjobs
- Monitor task queue: Check if tasks are accumulating in "pending" status
- Database connectivity: Verify scheduler table access and permissions

**Image pull errors**:

- Update image tag in ``kustomization.yaml``
- Check image exists: ``docker pull ghcr.io/lsst-dm/consdb-transformed-efd:<tag>``

Update Image Version
--------------------

1. Edit ``kustomization.yaml`` in your overlay directory
2. Change the ``newTag`` value:

.. code-block:: yaml

   images:
   - name: ghcr.io/lsst-dm/consdb-transformed-efd
     newTag: "25.5.3"

3. Deploy:

.. code-block:: bash

   make apply file=job.yaml embargo=true

Complete Examples
-----------------

**Deploy LATISS CronJob to production**:

.. code-block:: bash

   cd kubernetes/overlays/prod/latiss-cronjob
   make apply file=cronjob.yaml embargo=true
   kubectl get pods -n prod-latiss

**Process LSSTCam data for specific date range**:

.. code-block:: bash

   # Edit job.yaml to set DATETIME_START and DATETIME_END
   cd kubernetes/overlays/dev/lsstcam-job
   make apply file=job.yaml embargo=true
   kubectl logs -f <pod-name> -n dev-lsstcam

**Monitor failed jobs**:

.. code-block:: bash

   # Deploy failure monitor
   make apply file=failure-monitor.yaml embargo=true

   # Check for failed jobs
   kubectl get jobs -n dev-latiss | grep Failed

Common Scenarios
----------------

This section provides complete end-to-end examples for typical deployment scenarios.

Scenario 1: First-Time Development Deployment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal**: Deploy LATISS CronJob to development environment for the first time.

**Complete workflow:**

.. code-block:: bash

   # 1. Verify kubectl context
   kubectl config current-context
   # Should show: usdf-consdb-dev

   # 2. Get Vault access
   export VAULT_ADDR=<your-vault-url>
   vault login -method ldap -username <your-username>

   # 3. Navigate to LATISS CronJob directory
   cd kubernetes/overlays/dev/latiss-cronjob

   # 4. Deploy CronJob
   make apply file=cronjob.yaml embargo=true

   # 5. Verify deployment
   kubectl get cronjobs -n dev-latiss
   kubectl get pods -n dev-latiss

   # 6. Check logs
   kubectl logs -f <latest-pod-name> -n dev-latiss

Scenario 2: Processing Historical Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal**: Process LATISS data for a specific date range using a one-time job.

**Complete workflow:**

.. code-block:: bash

   # 1. Navigate to LATISS Job directory
   cd kubernetes/overlays/dev/latiss-job

   # 2. Edit job.yaml to set date range
   nano job.yaml
   # Set DATETIME_START: "2025-01-01T00:00:00"
   # Set DATETIME_END: "2025-01-02T00:00:00"

   # 3. Deploy the job
   make apply file=job.yaml embargo=true

   # 4. Monitor progress
   kubectl get jobs -n dev-latiss
   kubectl logs -f <job-pod-name> -n dev-latiss

   # 5. Check for completion
   kubectl describe job <job-name> -n dev-latiss

Scenario 3: Production Deployment with Monitoring
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal**: Deploy LSSTCam CronJob to production with failure monitoring.

**Complete workflow:**

.. code-block:: bash

   # 1. Switch to production context
   kubectl config use-context usdf-consdb

   # 2. Get Vault access for production
   vault login -method ldap -username <your-username>

   # 3. Deploy LSSTCam CronJob
   cd kubernetes/overlays/prod/lsstcam-cronjob
   make apply file=cronjob.yaml embargo=true

   # 4. Deploy failure monitor
   make apply file=failure-monitor.yaml embargo=true

   # 5. Verify both deployments
   kubectl get cronjobs -n prod-lsstcam
   kubectl get pods -n prod-lsstcam

   # 6. Set up monitoring
   watch kubectl get jobs -n prod-lsstcam

Scenario 4: Troubleshooting Failed Deployment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal**: Diagnose and fix a failed deployment.

**Complete workflow:**

.. code-block:: bash

   # 1. Check pod status
   kubectl get pods -n dev-latiss
   kubectl describe pod <failed-pod> -n dev-latiss

   # 2. Check logs for errors
   kubectl logs <failed-pod> -n dev-latiss

   # 3. Check job status
   kubectl get jobs -n dev-latiss
   kubectl describe job <failed-job> -n dev-latiss

   # 4. Check secrets
   kubectl get secrets -n dev-latiss

   # 5. Verify configuration
   kubectl get configmap -n dev-latiss

   # 6. Redeploy with corrected configuration
   make apply file=cronjob.yaml embargo=true

   # 7. Monitor new deployment
   kubectl logs -f <new-pod-name> -n dev-latiss

Repository Structure
--------------------

::

   kubernetes/
   ├── base/                   # Base templates
   │   ├── job/                # Job templates
   │   └── cronjob/            # CronJob templates
   └── overlays/               # Environment-specific configs
       ├── dev/                # Development environment
       │   ├── latiss-job/
       │   ├── latiss-cronjob/
       │   ├── lsstcam-job/
       │   ├── lsstcam-cronjob/
       │   ├── lsstcomcam-job/
       │   └── lsstcomcam-cronjob/
       └── prod/               # Production environment
           ├── latiss-job/
           ├── latiss-cronjob/
           ├── lsstcam-job/
           ├── lsstcam-cronjob/
           ├── lsstcomcam-job/
           └── lsstcomcam-cronjob/
