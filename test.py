import os
import openai
import config as cfg
from PIL import Image
from io import BytesIO
import requests
# Set up your OpenAI API credentials
# os.environ["OPENAI_API_KEY"] = cfg.open_ai_key

openai.api_key = cfg.open_ai_key
response = openai.Image.create(
  model="dall-e-3",
  prompt="a white siamese cat",
  size="1024x1024",
  quality="standard",
  n=1,
)
image_url = response.data[0].url

# Make a GET request to the image URL
response = requests.get(image_url)

# Load the image from the response content
image = Image.open(BytesIO(response.content))

# Display the image
image.show()