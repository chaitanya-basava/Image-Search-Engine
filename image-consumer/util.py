from typing import Union
from pyspark.sql import DataFrameReader
from pyspark.sql.streaming import DataStreamReader, DataStreamWriter


def load_configs(path: str, stream: Union[DataFrameReader, DataStreamReader, DataStreamWriter]):
    with open(path, 'r') as file:
        for line in file:
            line = line.strip().split("=")
            key, value = line[0], line[1]

            if path.find("kafka"):
                key = f"kafka.{key}"

            stream = stream.option(key, value)

    return stream
