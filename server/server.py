import uvicorn
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

from model import EmbeddingModel
from es.query import search_embeddings


app = FastAPI()
model = EmbeddingModel()

index = "flickr-images"
img_url_prefix = "https://farm66.staticflickr.com/"


class Query(BaseModel):
    phrase: Union[str, None]
    image: Union[str, None]


@app.post("/text_search")
async def get_similar_images_text(query: Query):
    if query.phrase is None:
        raise HTTPException(status_code=400, detail="'phrase' is required for text based search")

    emb = model.extract_text_embeddings(query.phrase)
    try:
        res = await search_embeddings(emb, index=index, source=["imgUrl", "title"])
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
        res = await search_embeddings(emb, index=index, source=["imgUrl", "title"])
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    # warm up call to model
    print(len(model.extract_text_embeddings("sky")))
    uvicorn.run(app, host="0.0.0.0", port=80)
