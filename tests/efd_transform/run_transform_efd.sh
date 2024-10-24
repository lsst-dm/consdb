# Example of command used to execute transform_efd
# Considering the command is being executed at the root of the consdb repository

# python python/lsst/consdb/efd_transform/transform_efd.py \
#     -i LATISS \
#     -r s3://rubin-summit-users/butler.yaml \
#     -d sqlite:///$PWD/tests/efd_transform/test.db \
#     -E usdf_efd \
#     -c python/lsst/consdb/efd_transform/config_LATISS.yaml \
#     -t 60 \
#     -l $PWD/tmp/transform.log

python python/lsst/consdb/efd_transform/transform_efd.py \
    -i LATISS \
    -s 2024-04-25T00:00:00  \
    -e 2024-04-25T00:05:00 \
    -r s3://rubin-summit-users/butler.yaml \
    -d sqlite:///$PWD/tests/efd_transform/test.db \
    -E usdf_efd \
    -c python/lsst/consdb/efd_transform/config_LATISS.yaml \
    -l $PWD/tmp/transform.log
