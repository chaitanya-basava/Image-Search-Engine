import torch
import mlflow
import shutil
import requests
import pandas as pd
from PIL import Image
from transformers import logging
from torch.nn.functional import normalize
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

    def predict(self, context, df):
        images = []
        for row in df.iloc:
            images.append(Image.open(requests.get(row.to_list()[0], stream=True).raw))

        inputs = self.processor(images=images, return_tensors="pt")
        outputs = normalize(self.model.get_image_features(**inputs), dim=1)
        image_embeds = outputs.squeeze(0).cpu().detach().numpy().tolist()

        return pd.DataFrame(image_embeds)


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
    print(embeds)
