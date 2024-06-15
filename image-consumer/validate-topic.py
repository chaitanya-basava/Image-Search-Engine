import argparse
import pyspark.sql.functions as f
from pyspark.sql.avro.functions import from_avro
from pyspark.sql import SparkSession, DataFrameReader

parser = argparse.ArgumentParser(description="Flickr image embedding extractor spark application")
parser.add_argument("-t", "--topic", dest="topic_name", type=str, required=True)
parser.add_argument("-kp", "--kafka_props", dest="kafka_props_path", default="../kafka/local.properties", type=str)
parser.add_argument("-ep", "--es_props", dest="es_props_path", default="../elasticsearch/local.properties", type=str)
args = parser.parse_args()


def load_configs(path: str, stream: DataFrameReader):
    with open(path, 'r') as file:
        for line in file:
            line = line.strip().split("=")
            key, value = line[0], line[1]

            if path.find("kafka"):
                key = f"kafka.{key}"

            stream = stream.option(key, value)

    return stream


if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .master("local[3]") \
        .appName("Image Consumer App - Test") \
        .getOrCreate()

    avroSchema = open("../schemas/flickr_image.avsc", "r").read()

    topic_name = args.topic_name
    kafka_stream_source = load_configs(
        args.kafka_props_path,
        spark.read.format("kafka")
    )

    kafka_df = (
        kafka_stream_source
        .option("subscribe", topic_name)
        .option("startingOffsets", "earliest")
        .load()
    )

    img_emb_df = (
        kafka_df
        .withColumn("key", f.col("key").cast("string"))
        .withColumn("value", f.expr("substring(value, 6, length(value)-5)"))  # needed when using confluent
        .withColumn("value", from_avro("value", avroSchema))
    )

    img_emb_df.show(truncate=True)
