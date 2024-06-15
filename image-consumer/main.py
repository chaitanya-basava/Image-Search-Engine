import json
import argparse
import mlflow.pyfunc
from io import BytesIO
from confluent_kafka.avro import AvroConsumer
from elasticsearch import Elasticsearch, helpers
from fastavro import schemaless_reader, parse_schema


def load_model(path: str):
    return mlflow.pyfunc.load_model(path)


def load_schema(schema_path: str):
    with open(schema_path, 'r') as file:
        schema = json.load(file)
    return parse_schema(schema)


parser = argparse.ArgumentParser(description="Flickr image embedding extractor application")
parser.add_argument("-t", "--topic", dest="topic_name", type=str, required=True)
parser.add_argument("-sp", "--schema_path", dest="schema_path", type=str, required=True)
parser.add_argument("-m", "--model_uri", dest="model_uri", default="../model/mlflow_clip_model", type=str)
parser.add_argument("-kp", "--kafka_props", dest="kafka_props_path", default="../kafka/local.properties", type=str)
parser.add_argument("-ep", "--es_props", dest="es_props_path", default="../elasticsearch/local.properties", type=str)
args = parser.parse_args()


def process_messages(consumer, model, es, avro_schema):
    actions = []
    while True:
        msg = consumer.poll(timeout=1.0)
        print(msg)
        if msg is None:
            continue

        try:
            message_value = schemaless_reader(BytesIO(msg.value()), avro_schema)
        except Exception as e:
            print(f"Error deserializing message: {e}")
            continue

        img_url = message_value['imgUrl']
        img_id = message_value['id']
        full_img_url = f"https://farm66.staticflickr.com/{img_url}"
        image_emb = model.predict(full_img_url)

        action = {
            "_index": args.topic_name,
            "_id": img_id,
            "_source": {
                "imgUrl": img_url,
                "image_emb": image_emb.tolist()
            }
        }
        actions.append(action)
        print(message_value)
        if len(actions) >= 30:
            helpers.bulk(es, actions)
            actions = []

    if actions:
        helpers.bulk(es, actions)


def load_configs(path: str):
    configs = {}
    with open(path, 'r') as file:
        for line in file:
            line = line.strip().split("=")
            key, value = line[0], line[1]
            configs[key] = value
    return configs


if __name__ == "__main__":
    kafka_configs = load_configs(args.kafka_props_path)

    consumer = AvroConsumer({
        'bootstrap.servers': kafka_configs['bootstrap.servers'],
        'group.id': 'image-embedding-extractor',
        'auto.offset.reset': 'earliest'
    }, schema_registry=kafka_configs['schema.registry.url'])
    consumer.subscribe([args.topic_name])

    es = Elasticsearch(
        [{'host': 'localhost', 'port': 9200, 'scheme': 'http'}],
        basic_auth=("admin", "admin"),
        verify_certs=False
    )

    print(es.ping())

    model = load_model(args.model_uri)

    avro_schema = load_schema(args.schema_path)

    print("Starting to process messages")

    process_messages(consumer, model, es, avro_schema)
