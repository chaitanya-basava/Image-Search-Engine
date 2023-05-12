import json
import asyncio
from conn import create_conn
from elasticsearch import AsyncElasticsearch


async def create_index(_es: AsyncElasticsearch, index_name: str, _schema: dict) -> bool:
    index_setting = {
        "index": {
            "number_of_replicas": 0
        }
    }
    index_body = {
        "properties": {
            "image_emb": {
                "type": "dense_vector",
                "dims": 512,
                "element_type": "float",
                "index": True,
                "similarity": "dot_product",
                "index_options": {
                    "type": "hnsw",
                    "m": 32,
                    "ef_construction": 100
                }
            }
        }
    }

    index_body["properties"].update(_schema)
    # print(json.dumps(index_body, indent=1))

    created = False
    try:
        if not await _es.indices.exists(index=index_name):
            await _es.indices.create(index=index_name, settings=index_setting, mappings=index_body)
            print(f"{index_name} created - {await _es.indices.exists(index=index_name)}")
            created = True
        else:
            print("Already created!!")
    except Exception as ex:
        print(ex)

    return created


def parse_avro(path: str) -> dict:
    avro_fields = json.loads(open(path, "rb").read())["fields"]

    _schema = {}
    for field in avro_fields:
        _type = field["type"]

        if _type == "string" or field["name"] == "tags":
            _type = "text"

        _schema[field["name"]] = {"type": _type}

    return _schema


if __name__ == '__main__':
    schema = parse_avro("../../schemas/flickr_image.avsc")
    es = create_conn()
    index_created = asyncio.run(create_index(es, "flickr-images", schema))
    print(index_created)
