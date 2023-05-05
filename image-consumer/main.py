from pyspark.sql import SparkSession
from pyspark.sql.avro.functions import from_avro
from pyspark.sql.functions import expr

from clip_model import load_model_udf

schema_registry_url = "http://localhost:8081"

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
        spark.read
        .format("kafka")
        .option("kafka.bootstrap.servers", "localhost:9092")
        .option("subscribe", "flickr-images")
        .option("startingOffsets", "earliest")
        .load()
        .withColumn("value", expr("substring(value, 6, length(value)-5)"))  # needed when using confluent
        .withColumn("value", from_avro("value", avroSchema))
    )

    df.select("value.*").show(truncate=False)
