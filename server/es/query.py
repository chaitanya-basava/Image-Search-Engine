from typing import List


async def search_embeddings(es, vector: List[float], index: str, source: List[str]):
    knn_query = {
        "field": "image_emb",
        "query_vector": vector,
        "k": 10,
        "num_candidates": 100
    }

    res = await es.search(index=index, knn=knn_query, source=source)
    return res["hits"]["hits"]
