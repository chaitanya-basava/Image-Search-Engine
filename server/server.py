import uvicorn
from fastapi import FastAPI, HTTPException

from model import EmbeddingModel
from es.query import search_embeddings
from config import get_settings, Query
from es.conn import create_conn, check_connection

app = FastAPI()

# load env variables
settings = get_settings()

# create es connection
print(check_connection(settings.es_host, settings.es_port))
es = create_conn(settings.es_host, settings.es_port)

# load model
model = EmbeddingModel()

# warm up call to model
print(f"warm up model call, embedding size: {len(model.extract_text_embeddings('give me embeddings'))}")


@app.post("/text_search")
async def get_similar_images_text(query: Query):
    if query.phrase is None:
        raise HTTPException(status_code=400, detail="'phrase' is required for text based search")

    emb = model.extract_text_embeddings(query.phrase)
    try:
        res = await search_embeddings(es, emb, index=settings.es_index, source=["imgUrl", "title"])
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/image_search")
async def get_similar_images(query: Query):
    if query.image is None:
        raise HTTPException(status_code=400, detail="'image' is required for image based search")

    try:
        emb = model.extract_image_embeddings(query.image)
    except Exception as e:
        msg = f"please share a valid URL or upload an image - {str(e).split(':')[0]}"
        raise HTTPException(status_code=500, detail=msg)

    try:
        res = await search_embeddings(
            es, emb,
            index=settings.es_index,
            source=["imgUrl", "title", "userId", "userName", "postedOn"]
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=80)
