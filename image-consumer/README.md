# Image consumer

## Prerequisite

1. Set up `elasticsearch` and `kibana`.

```
docker-compose -f ./elasticsearch/docker-compose.yml up -d
```

2. Install all the necessary libraries

```
pip install -r requirements.txt
```

## Create model artifact

Model artifact is needed for running the spark streaming application. This model is used to
extract image embeddings of the records from kafka using their Flickr url.

```
python clip_model.py
```

This will save the model in `mlflow_clip_model` directory.

## Spark application

run the spark application using following command

```
spark-submit --master "local[3]" --deploy-mode client --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0,org.apache.spark:spark-avro_2.12:3.4.0,org.elasticsearch:elasticsearch-spark-30_2.12:8.7.1 main.py -t flickr-images 
```

## Extra spark setup

Needed if Spark 3.4.0 is being used

Check available java versions 
```
/usr/libexec/java_home -V
```

Set the java version to 8/11/17
```
export JAVA_HOME=<java 8/11/17 versions>
```
