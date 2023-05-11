import base64
import requests
import validators
from PIL import Image
from io import BytesIO
from typing import List
from sentence_transformers import SentenceTransformer


def get_image_from_url(url: str) -> Image:
    return Image.open(requests.get(url, stream=True).raw)


def get_image_from_base64(base64_str: str) -> Image:
    return Image.open(BytesIO(base64.b64decode(base64_str)))


class EmbeddingModel:
    def __init__(self, model_name: str = "clip-ViT-B-32"):
        self.model = SentenceTransformer(model_name)

    def extract_text_embeddings(self, phrase: str) -> List[float]:
        phrase = phrase.strip()
        text_emds = self.model.encode(phrase, convert_to_numpy=True, normalize_embeddings=True)
        return text_emds.tolist()

    def extract_image_embeddings(self, image_str: str) -> List[float]:
        if validators.url(image_str):
            image = get_image_from_url(image_str)
        else:
            image = get_image_from_base64(image_str)

        return self.__image_embedding(image)

    def __image_embedding(self, image: Image) -> List[float]:
        image_emds = self.model.encode(image, convert_to_numpy=True, normalize_embeddings=True)
        return image_emds.tolist()


if __name__ == '__main__':
    model = EmbeddingModel()
