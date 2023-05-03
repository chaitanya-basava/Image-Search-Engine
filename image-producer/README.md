# Image producer

This module includes the code used for fetching images from Flickr and push an avro message to specified topic.

### Prerequisites to run
- Flickr API. You can create one from [here](https://www.flickr.com/services/api/).
- Kafka and Schema registry.
  - For local use, you can install and run them using [confluent](https://www.confluent.io/).

### Run on local

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

3. Create `flickr-images` (you may use any name of choice) topic using
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

4. Start the schema registry using this cmd
```
schema-registry-start $CONFLUENT_CONFIG_PATH/schema-registry/schema-registry.properties
```

5. Run `mvn clean install`, this will generate the `FlickrImage` avro class, which is generated from the schema
provided in `schemas` directory.
6. Create `secrets.json` file inside [resources](src/main/resources) folder and pass Flickr's `API_KEY` and `SECRET`.
7. Supply Kafka producer properties as a `{KAFKA_RUN_TYPE}.properties` file places inside `resources/kafka` dir.
View [local.properties](src/main/resources/kafka/local.properties) for reference.
8. Execute the main method in Main class, this will start the producer.

**NOTE:** Set `KAFKA_TOPIC_NAME` env variable if using a different topic name.

**NOTE:** You can verify the produced messages using following cmd
```
kafka-avro-console-consumer --topic flickr-images --from-beginning --bootstrap-server localhost:9092 --property schema.registry.url=http://localhost:8081
```
