FROM python:3.8-slim-buster

WORKDIR /code
COPY ./model /code/../model
COPY ./server /code

RUN pip install --no-cache-dir -r requirements.txt

# pre downloads the model artifacts
# helps avoid download time of ~3min upon container start
RUN python ../model/clip_model.py

CMD ["uvicorn", "server:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
