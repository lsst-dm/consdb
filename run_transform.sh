# Example of command used to execute transform_efd
python python/lsst/consdb/transform_efd.py \
    -i LATISS \
    -s 2024-04-24T23:00:00  \
    -e 2024-04-25T00:00:00 \
    -r /repo/embargo \
    -d sqlite:///$PWD/tmp/test.db \
    -E usdf_efd \
    -c $PWD/tmp/config_LATISS.yaml \
    -l $PWD/tmp/transform.log
