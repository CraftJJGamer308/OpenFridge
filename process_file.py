import os
from openai import OpenAI
import base64

client = OpenAI(
    # This is the default and can be omitted
    api_key="xxxxxx",
)


prompt = "create a list with every food item in the image and its quantity, WITHOUT ANY COMMENTARY. "
with open("uploads/bild.jpg", "rb") as image_file:
    b64_image = base64.b64encode(image_file.read()).decode("utf-8")

response = client.responses.create(
    model="gpt-4o",
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": prompt},
                {"type": "input_image", "image_url": f"data:image/png;base64,{b64_image}"},
            ],
        }
    ],
)

print(response.output_text.strip("`"))