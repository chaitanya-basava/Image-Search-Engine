# Image producer

This module includes the code used for fetching images from Flickr and push an avro message to specified topic.

### Prerequisites to run
- Flickr API. You can create one from [here](https://www.flickr.com/services/api/).
- Kafka and Schema registry.
  - For local use, you can install and run them using [confluent](https://www.confluent.io/).

### Run on local

#### kafka self setup 
1. Setup env variables in `.bash_profile` or `.zshrc`
```
CONFLUENT_PATH="<PATH-TO-CONFLUENT-DIR>"
CONFLUENT_CONFIG_PATH="$CONFLUENT_PATH/etc"

PATH="$PATH:$CONFLUENT_PATH/bin"
```

2. Run kafka by running these 2 cmds in separate terminals
```
zookeeper-server-start $CONFLUENT_CONFIG_PATH/kafka/zookeeper.properties
```
```
kafka-server-start $CONFLUENT_CONFIG_PATH/kafka/server.properties
```

3. Start the schema registry using this cmd
```
schema-registry-start $CONFLUENT_CONFIG_PATH/schema-registry/schema-registry.properties
```

#### Kafka using docker-compose

1. Run the `docker-compose.yml` file in [kafka](../kafka) folder.
```
RESOURCE_HOST_URL=localhost docker-compose -f ./kafka/docker-compose.yml up -d
```
This will set up kafka, schema-registry and control center of confluent v7.4.0

#### image producer

1. Create `flickr-images` (you may use any name of choice) topic using
```
kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 2 --topic flickr-images
```
```
kafka-configs --alter --add-config retention.ms=21600000 --bootstrap-server=localhost:9092 --topic flickr-images
```
```
kafka-configs --alter --add-config retention.bytes=1073741824 --bootstrap-server=localhost:9092 --topic flickr-images
```

Msg retention is set to 6hrs with max storage of 1GB. Check config using this cmd
```
kafka-configs --bootstrap-server localhost:9092 --entity-type topics --entity-name flickr-images --describe --all
```
2. Create `secrets.json` file inside [resources](src/main/resources) folder and pass Flickr's `API_KEY` and `SECRET`.
3. Run `mvn clean package`, this will generate the `FlickrImage` avro class, which is generated from the schema
provided in `schemas` directory and also generates tje necessary jar file in `target` directory.
4. Build a jar of the [image-producer](./README.md) project
5. Run the application by supplying the respective kafka properties (ex: [local.properties](../kafka/local.properties))
and `tags.json` files (ex: [tags.json](../cache/tags.json))
```
java -jar <path to jar> -kp <path to kafka properties> -c <path to tags.json> -k 10
```
You can use this cmd when executed from root directory of this project
```
java -jar ./image-producer/target/image-producer-1.0-SNAPSHOT-jar-with-dependencies.jar -kp "./kafka/local.properties" -c "./cache/tags.json"
```

**NOTE:** Set `KAFKA_TOPIC_NAME` env variable if using a different topic name from `flickr-images`.

**NOTE:** You can verify the produced messages using following cmd
```
kafka-avro-console-consumer --topic flickr-images --from-beginning --bootstrap-server localhost:9092 --property schema.registry.url=http://localhost:8081
```
