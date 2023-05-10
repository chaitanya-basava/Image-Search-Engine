FROM python:3.8-slim-buster

WORKDIR /code
COPY ./ /code

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "server:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]