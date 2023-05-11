import sys
from functools import lru_cache
from elasticsearch import AsyncElasticsearch, Elasticsearch


@lru_cache()
def create_conn(es_host: str = "localhost", es_port: int = 9200) -> AsyncElasticsearch:
    return AsyncElasticsearch(
        [{'host': es_host, 'port': es_port, 'scheme': 'http'}],
        basic_auth=("admin", "admin"),
        verify_certs=False
    )


def check_connection(es_host: str = "localhost", es_port: int = 9200):
    es = Elasticsearch(
        [{'host': es_host, 'port': es_port, 'scheme': 'http'}],
        basic_auth=("admin", "admin"),
        verify_certs=False
    )
    ping = es.ping()
    if not ping:
        print(es.info())
        sys.exit()

    return f"Connected to ES at {es_host}:{es_port}"
