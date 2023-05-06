import pyspark.sql.functions as f
from pyspark.sql import SparkSession
from pyspark.sql.avro.functions import from_avro

from clip_model import load_model_udf


if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .master("local[3]") \
        .appName("Image Consumer App") \
        .config("spark.streaming.stopGracefullyOnShutdown", "true") \
        .getOrCreate()

    predict = load_model_udf(spark)
    avroSchema = open("../schemas/flickr_image.avsc", "r").read()

    df = (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", "localhost:9092")
        .option("subscribe", "flickr-images")
        .option("startingOffsets", "earliest")
        .load()
    )

    img_emb_df = (
        df
        .withColumn("value", f.expr("substring(value, 6, length(value)-5)"))  # needed when using confluent
        .withColumn("value", from_avro("value", avroSchema))
        .select(
            "value.*",
            predict(
                f.concat(f.lit("https://farm66.staticflickr.com/"), f.col("value.imgUrl"))
            ).alias("image_emb")
        )
    )

    # TODO: update sink to ElasticSearch
    query = (
        img_emb_df.writeStream
        .format("json")
        .queryName("Image embedding extractor")
        .outputMode("append")
        .option("path", "output")
        .option("checkpointLocation", "chk-point-dir/img_emb_extractor")
        .trigger(processingTime="1 minute")
        .start()
    )

    query.awaitTermination()
