import base64
from openai import OpenAI

client = OpenAI(
        # openai系列的sdk，包括langchain，都需要这个/v1的后缀
        base_url='https://api.openai-proxy.org/v1',
        api_key='sk-Cinx17W4V8Ss4B7HSfxUrf2kikhbvZE7EGHy5SYwWJBWs6Qm',
    )

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Path to your image
image_path = "../image/vl_now.jpg"

# Getting the Base64 string
base64_image = encode_image(image_path)

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                { "type": "text", "text": "what's in this image?" },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    },
                },
            ],
        }
    ],
)

print(completion.choices[0].message.content)