import requests
from PIL import Image
from transformers import logging
from transformers import AutoProcessor, CLIPModel, AutoTokenizer

logging.set_verbosity(40)

model_name = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(model_name)
processor = AutoProcessor.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

url = "https://farm66.staticflickr.com/65535/52743059408_a9eac98298_z.jpg"
image = Image.open(requests.get(url, stream=True).raw)
inputs = processor(images=image, return_tensors="pt")

image_features = model.get_image_features(**inputs)
print(image_features.shape)

inputs = tokenizer(["a photo of a cat"], padding=True, return_tensors="pt")

text_features = model.get_text_features(**inputs)
print(text_features.shape)
