from pyspark.sql import SparkSession


if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .master("local[3]") \
        .appName("Validator App") \
        .config("spark.streaming.stopGracefullyOnShutdown", "true") \
        .getOrCreate()

    df = (
        spark.read
        .format("json")
        .option("path", "output")
        .load()
    )

    df.show()
