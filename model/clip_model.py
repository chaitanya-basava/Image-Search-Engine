import os
import torch
import mlflow
import shutil
import base64
import requests
import validators
import numpy as np
import pandas as pd
from PIL import Image
from io import BytesIO
from typing import List
from transformers import logging
from sentence_transformers import SentenceTransformer

logging.set_verbosity(40)


class ClipImageEmbeddingModel(mlflow.pyfunc.PythonModel):
    def __init__(self, model_name="clip-ViT-B-32", batch_size=32):
        self.batch_size = batch_size
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def predict(self, context, df):
        images = []
        for row in df.iloc:
            images.append(Image.open(requests.get(row.to_list()[0], stream=True).raw))

        image_embeds = self.model.encode(
            images,
            batch_size=self.batch_size,
            device=self.device,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        return pd.DataFrame(image_embeds.tolist())

    def extract_text_embeddings(self, phrase: str) -> List[float]:
        phrase = phrase.strip()
        text_emds = self.model.encode(phrase, convert_to_numpy=True, normalize_embeddings=True)
        return text_emds.tolist()

    def extract_image_embeddings(self, image_str: str) -> List[float]:
        if validators.url(image_str):
            image = Image.open(requests.get(image_str, stream=True).raw)
        else:
            image = Image.open(BytesIO(base64.b64decode(image_str)))

        image_emds = self.model.encode(image, convert_to_numpy=True, normalize_embeddings=True)
        return image_emds.tolist()


default_model_path = "../model/mlflow_clip_model"


def save_model(path=default_model_path):
    clip_image_embedding_model = ClipImageEmbeddingModel()
    mlflow.pyfunc.save_model(path=path, python_model=clip_image_embedding_model)


def load_model(path=default_model_path):
    return mlflow.pyfunc.load_model(path)


if __name__ == '__main__':
    if os.path.exists(default_model_path):
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
