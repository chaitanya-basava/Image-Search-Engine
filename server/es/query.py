from typing import List


async def search_embeddings(
        es,
        vector: List[float],
        index: str,
        source: List[str],
        page: int,
        k: int
):
    from_ = page * k
    size_ = k

    knn_query = {
        "field": "image_emb",
        "query_vector": vector,
        "k": 100,
        "num_candidates": 100
    }

    res = await es.search(index=index, knn=knn_query, source=source, from_=from_, size=size_)
    return res["hits"]["hits"]
