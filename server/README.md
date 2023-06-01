# Server

## Prerequisite

1. Set up `elasticsearch` and `kibana`.

```
docker-compose -f ./elasticsearch/docker-compose.yml up -d
```

2. Create a `.env` file same folder as the `server.py`, you can use this sample

```
ES_HOST=elasticsearch
ES_PORT=9200
ES_INDEX=flickr-images
```

3. Create `flickr-images` index in elasticsearch

```
python create_index_es.py
```

## Local set up

1. Install all the necessary libraries

```
pip install -r requirements.txt
```

2. Create the necessary model artifact

```
python ../model/clip_model.py
```

3. Run the server

```
ES_HOST=localhost uvicorn server:app --host 0.0.0.0 --port 80
```

## Docker container set up

1. Build the docker image, run this from parent directory

```
docker build -t image-search-server -f ./server/Dockerfile .
```

2. Run the container

```
docker run --name image-search-server --network elasticsearch_default -p 80:80 image-search-server
```

**The api can be accessed at localhost:80**