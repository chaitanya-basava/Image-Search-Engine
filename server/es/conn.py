import sys
from elasticsearch import AsyncElasticsearch


es = AsyncElasticsearch(
    [{'host': 'localhost', 'port': 9200, 'scheme': 'http'}],
    basic_auth=("admin", "admin"),
    verify_certs=False
)


async def check_connection():
    if not await es.ping():
        print("Couldn't connect to ES")
        print(await es.info())
        sys.exit()

    return await es.ping()
