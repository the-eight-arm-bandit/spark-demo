import logging
import argparse
import json
import uuid
import random

from pyspark import SparkContext, SparkConf


def make_one_record(_):
    return "\t".join(
        [
            "k=%s" % uuid.uuid4().hex,
            "y=%s" % json.dumps({"geo": {"country": random.choice(["usa", "can", "mex"])}})
        ]
    )


if __name__ == "__main__":
    logger = logging.getLogger("py4j")
    logger.setLevel(logging.ERROR)

    parser = argparse.ArgumentParser()
    parser.add_argument("--app_name")
    parser.add_argument("--event_count")
    parser.add_argument("--o_dummy_logs")
    args = parser.parse_args()

    conf = SparkConf().setAppName(args.app_name)
    conf.set('spark.ui.showConsoleProgress', False)

    sc = SparkContext(conf=conf)
    sc.parallelize(_ for _ in range(int(args.event_count))).\
        map(make_one_record).\
        saveAsTextFile(args.o_dummy_logs, "org.apache.hadoop.io.compress.GzipCodec")

"""
hadoop fs -rm -r -f -skipTrash /users/vagrant/events/2019/03/27/12/LOGS;
/usr/lib/spark/bin/spark-submit --master local[1] \
demo_spark_job/lib/generate_data.py \
--o_dummy_logs /users/vagrant/events/2019/03/27/12/LOGS \
--event_count 100
"""
