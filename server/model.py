from sentence_transformers import SentenceTransformer


def init_model(model_name: str = "clip-ViT-B-32") -> SentenceTransformer:
    return SentenceTransformer(model_name)


def extract_text_embeddings(model: SentenceTransformer, phrase: str):
    phrase = phrase.strip()
    text_emds = model.encode(phrase, convert_to_numpy=True, normalize_embeddings=True)
    return text_emds.tolist()
