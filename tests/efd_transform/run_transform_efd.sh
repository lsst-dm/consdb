# Example of command used to execute transform_efd
# Considering the command is being executed at the root of the consdb repository

# Real-time mode proccess 5 minuts of data
python python/lsst/consdb/efd_transform/transform_efd.py \
    -i LATISS \
    -r s3://rubin-summit-users/butler.yaml \
    -d sqlite:///$PWD/tests/efd_transform/LATISS.db \
    -E usdf_efd \
    -c python/lsst/consdb/efd_transform/config_LATISS.yml \
    -t 5 \
    -w 1 \
    -l $PWD/tmp/transform.log


python python/lsst/consdb/efd_transform/transform_efd.py \
    -i LATISS \
    -r s3://rubin-summit-users/butler.yaml \
    -d sqlite:///$PWD/tests/efd_transform/LSSTComCam.db \
    -E usdf_efd \
    -c python/lsst/consdb/efd_transform/config_LSSTComCam.yml \
    -t 5 \
    -w 1 \
    -l $PWD/tmp/transform.log


python python/lsst/consdb/efd_transform/transform_efd.py \
    -i LATISS \
    -r s3://rubin-summit-users/butler.yaml \
    -d sqlite:///$PWD/tests/efd_transform/LSSTComCamSim.db \
    -E usdf_efd \
    -c python/lsst/consdb/efd_transform/config_LSSTComCamSim.yml \
    -t 5 \
    -w 1 \
    -l $PWD/tmp/transform.log
# Processing fixed period of data in chunks of 20 minutes
# python python/lsst/consdb/efd_transform/transform_efd.py \
#     -i LATISS \
#     -r s3://rubin-summit-users/butler.yaml \
#     -d sqlite:///$PWD/tests/efd_transform/test.db \
#     -E usdf_efd \
#     -c python/lsst/consdb/efd_transform/config_LATISS.yaml \
#     -t 20 \
#     -w 1 \
#     -l $PWD/tmp/transform.log
