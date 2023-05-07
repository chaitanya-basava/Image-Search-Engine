import sys
from elasticsearch import Elasticsearch


es = Elasticsearch(
    [{'host': 'localhost', 'port': 9200, 'scheme': 'http'}],
    basic_auth=("admin", "admin"),
    verify_certs=False
)

if not es.ping():
    print("Couldn't connect to ES")
    print(es.info())
    sys.exit()
