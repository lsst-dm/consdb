# Example of command used to execute transform_efd
python python/lsst/consdb/transform_efd.py \
    -i LATISS \
    -s 2024-04-25T00:00:00  \
    -e 2024-04-30T23:59:59 \
    -r /repo/embargo \
    -d sqlite:///$PWD/tmp/test.db \
    -E usdf_efd \
    -c $PWD/tmp/config.yaml \
    -l $PWD/tmp/transform.log
