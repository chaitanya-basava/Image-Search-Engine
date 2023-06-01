import mlflow
import argparse
from typing import Union
import pyspark.sql.functions as f
from pyspark.sql import SparkSession
from pyspark.sql.avro.functions import from_avro
from pyspark.sql.types import ArrayType, DoubleType
from pyspark.sql.streaming import DataStreamReader, DataStreamWriter


def load_model_udf(_spark: SparkSession, path: str):
    return mlflow.pyfunc.spark_udf(spark=_spark, model_uri=path, result_type=ArrayType(DoubleType()))


parser = argparse.ArgumentParser(description="Flickr image embedding extractor spark application")
parser.add_argument("-t", "--topic", dest="topic_name", type=str, required=True)
parser.add_argument("-m", "--model_uri", dest="model_uri", default="../model/mlflow_clip_model", type=str)
parser.add_argument("-kp", "--kafka_props", dest="kafka_props_path", default="../kafka/local.properties", type=str)
parser.add_argument("-ep", "--es_props", dest="es_props_path", default="../elasticsearch/local.properties", type=str)
args = parser.parse_args()


def load_configs(path: str, stream: Union[DataStreamReader, DataStreamWriter]):
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
        .appName("Image Consumer App") \
        .config("spark.streaming.stopGracefullyOnShutdown", "true") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("INFO")

    predict = load_model_udf(spark, args.model_uri)
    avroSchema = open("../schemas/flickr_image.avsc", "r").read()

    topic_name = args.topic_name
    kafka_stream_source = load_configs(
        args.kafka_props_path,
        spark.readStream.format("kafka")
    )

    kafka_df = (
        kafka_stream_source
        .option("subscribe", topic_name)
        .option("startingOffsets", "earliest")
        .option("maxOffsetsPerTrigger", 30)
        .load()
    )

    img_emb_df = (
        kafka_df
        .withColumn("value", f.expr("substring(value, 6, length(value)-5)"))  # needed when using confluent
        .withColumn("value", from_avro("value", avroSchema))
        .select(
            "value.*",
            predict(
                f.concat(f.lit("https://farm66.staticflickr.com/"), f.col("value.imgUrl"))
            ).alias("image_emb")
        )
    )

    es_stream_sink = load_configs(
        args.es_props_path,
        img_emb_df.writeStream.format("org.elasticsearch.spark.sql")
    )

    query = (
        es_stream_sink
        .queryName("Image embedding extractor")
        .outputMode("append")
        .option("es.mapping.id", "id")
        .option("es.nodes.discovery", "false")
        .option("es.resource", f"{topic_name}")
        .option("es.nodes.wan.only", "true")  # needed to connect to specified node with http
        .option("checkpointLocation", "chk-point-dir/img_emb_extractor-es")
        .trigger(processingTime="1 minute")
        .start()
    )

    # write to json for testing
    # query = (
    #     img_emb_df.writeStream
    #     .format("json")
    #     .queryName("Image embedding extractor")
    #     .outputMode("append")
    #     .option("path", "output")
    #     .option("checkpointLocation", "chk-point-dir/img_emb_extractor")
    #     .trigger(processingTime="1 minute")
    #     .start()
    # )

    query.awaitTermination()
