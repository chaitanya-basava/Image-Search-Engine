from flask import Flask
from es.query import search_embeddings
from model import init_model, extract_text_embeddings


app = Flask(__name__)
model = init_model()
img_url_prefix = "https://farm66.staticflickr.com/"


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == '__main__':
    emb = extract_text_embeddings(model, "sky")
    print(search_embeddings(emb, "flickr-images", ["imgUrl", "title"]))
