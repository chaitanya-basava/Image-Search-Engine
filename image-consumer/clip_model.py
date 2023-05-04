import torch
import mlflow
import requests
import pandas as pd
from PIL import Image
from transformers import logging
from transformers import AutoProcessor, CLIPModel

from pyspark.sql import SparkSession
from pyspark.sql.types import DoubleType, ArrayType

logging.set_verbosity(40)


class ClipImageEmbeddingModel(mlflow.pyfunc.PythonModel):
    def __init__(self, model_name="openai/clip-vit-base-patch32"):
        self.model_name = model_name
        self.device = torch.cuda if torch.cuda.is_available() else torch.cpu
        self.model = CLIPModel.from_pretrained(self.model_name)
        self.processor = AutoProcessor.from_pretrained(self.model_name)

    def predict(self, context, image_url):
        image = Image.open(requests.get(image_url, stream=True).raw)
        inputs = self.processor(images=image, return_tensors="pt")
        image_features = self.model.get_image_features(**inputs)

        return pd.Series(image_features.squeeze(0).cpu().detach().numpy())


# clipImageEmbeddingModel = ClipImageEmbeddingModel()
# mlflow.pyfunc.save_model(path="./mlflow_clip_model", python_model=clipImageEmbeddingModel)

# url = "https://farm66.staticflickr.com/65535/52743059408_a9eac98298_z.jpg"
# loaded_model = mlflow.pyfunc.load_model("./mlflow_clip_model")
# print(loaded_model.predict(url))

spark = SparkSession \
    .builder \
    .master("local[3]") \
    .appName("Image Consumer App") \
    .config("spark.port.maxRetries", 100) \
    .getOrCreate()

clip_model = mlflow.pyfunc.spark_udf(
    spark,
    model_uri="./mlflow_clip_model",
    result_type=ArrayType(DoubleType()),
    env_manager="conda"
)
print(clip_model)
