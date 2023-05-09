from .conn import es
from typing import List


def search_embeddings(vector: List[float], index: str, source: List[str]):
    knn_query = {
        "field": "image_emb",
        "query_vector": vector,
        "k": 10,
        "num_candidates": 100
    }

    return es.search(index=index, knn=knn_query, source=source)
