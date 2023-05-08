import torch
import mlflow
import shutil
import requests
import numpy as np
import pandas as pd
from PIL import Image
from transformers import logging
from sentence_transformers import SentenceTransformer

from pyspark.sql import SparkSession
from pyspark.sql.types import ArrayType, DoubleType

logging.set_verbosity(40)


class ClipImageEmbeddingModel(mlflow.pyfunc.PythonModel):
    def __init__(self, model_name="clip-ViT-B-32"):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def predict(self, context, df):
        images = []
        for row in df.iloc:
            images.append(Image.open(requests.get(row.to_list()[0], stream=True).raw))

        image_embeds = self.model.encode(images, device=self.device, convert_to_tensor=True, normalize_embeddings=True)

        return pd.DataFrame(image_embeds.tolist())


default_model_path = "./mlflow_clip_model"


def save_model(path=default_model_path):
    clip_image_embedding_model = ClipImageEmbeddingModel()
    mlflow.pyfunc.save_model(path=path, python_model=clip_image_embedding_model)


def load_model(path=default_model_path):
    return mlflow.pyfunc.load_model(path)


def load_model_udf(spark: SparkSession, path=default_model_path):
    return mlflow.pyfunc.spark_udf(spark=spark, model_uri=path, result_type=ArrayType(DoubleType()))


if __name__ == '__main__':
    shutil.rmtree(default_model_path)
    save_model(default_model_path)
    model = load_model(default_model_path)

    url = pd.DataFrame([
        "https://farm66.staticflickr.com/65535/52743059408_a9eac98298_z.jpg",
        "https://farm66.staticflickr.com/65535/52743059408_a9eac98298_z.jpg"
    ])
    embeds = model.predict(url)
    print(embeds.shape)

    # validate unit vector trait - necessary for writing to ES
    print((embeds.apply(np.linalg.norm, axis=1)))

    print(embeds)
