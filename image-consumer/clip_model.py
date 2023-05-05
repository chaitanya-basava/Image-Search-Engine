import torch
import mlflow
import requests
import pandas as pd
from PIL import Image
from transformers import logging
from transformers import AutoProcessor, CLIPModel

from pyspark.sql import SparkSession
from pyspark.sql.types import ArrayType, DoubleType

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


default_model_path = "./mlflow_clip_model"


def save_model(path=default_model_path):
    clip_image_embedding_model = ClipImageEmbeddingModel()
    mlflow.pyfunc.save_model(path=path, python_model=clip_image_embedding_model)


def load_model(path=default_model_path):
    return mlflow.pyfunc.load_model(path)


def load_model_udf(spark: SparkSession, path=default_model_path):
    return mlflow.pyfunc.spark_udf(spark=spark, model_uri=path, result_type=ArrayType(DoubleType()))
