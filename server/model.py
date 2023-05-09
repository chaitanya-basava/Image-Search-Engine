from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    def __init__(self, model_name: str = "clip-ViT-B-32"):
        self.model = SentenceTransformer(model_name)

    def extract_text_embeddings(self, phrase: str):
        phrase = phrase.strip()
        text_emds = self.model.encode(phrase, convert_to_numpy=True, normalize_embeddings=True)
        return text_emds.tolist()
