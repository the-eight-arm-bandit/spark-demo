import logging
import argparse
import json
import uuid
import re

from pyspark import SparkContext, SparkConf, SQLContext
from pyspark.sql.types import StructType, StringType, StructField

TAG_SCHEMA = StructType(
    [
        StructField("cookie", StringType()),
        StructField("country", StringType()),
    ]
)


def parse_cookie(maybe):
    try:
        return uuid.UUID(maybe).hex
    except:
        # This is terrible
        return None


def to_str(maybe):
    return str(maybe) if maybe is not None else None


def parse_extra_info(maybe):
    try:
        return json.loads(maybe)
    except:
        return None


def project_geo(maybe):
    try:
        geo_location = maybe.get("geo") or {}
        country = to_str(geo_location.get("country"))

        return country
    except:
        return None


def field_from_log(line):
    cookie, country = None, None
    for s in line.split("\t"):
        match = re.match(r"^k=(.*)$", s)
        if match:
            cookie = parse_cookie(match.group(1))
            continue

        match = re.match(r"^y=(.*)$", s)
        if match:
            extra_info = parse_extra_info(match.group(1))
            country = project_geo(extra_info)
            continue

    return cookie, country


if __name__ == "__main__":
    logger = logging.getLogger("py4j")
    logger.setLevel(logging.ERROR)

    parser = argparse.ArgumentParser()
    parser.add_argument("--app_name")
    parser.add_argument("--i_tag_logs")
    parser.add_argument("--o_results")

    args = parser.parse_args()
    conf = SparkConf().setAppName(args.app_name)
    conf.set('spark.ui.showConsoleProgress', False)

    sc = SparkContext(conf=conf)
    sql_ctx = SQLContext(sc)

    sql_ctx.createDataFrame(
        sc.textFile(args.i_tag_logs).map(field_from_log),
        TAG_SCHEMA
    ).write.parquet(args.o_results)

"""
hadoop fs -rm -r -f -skipTrash /users/vagrant/events/2019/03/27/12/TAGS;
/usr/lib/spark/bin/spark-submit --master local[1] \
lib/parse_logs.py \
--i_tag_logs /users/vagrant/events/2019/03/27/12/LOGS \
--o_results /users/vagrant/events/2019/03/27/12/TAGS
"""
