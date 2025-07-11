import base64
import requests
import os
from PIL import Image
from io import BytesIO
import ollama
import pathlib

# Configuration
output_folder = "D:\\CGVR\\CP\\Test\\images\\output"
api_url = "http://127.0.0.1:7860/sdapi/v1/txt2img"
steps = 50
cfg_scale = 7.5
width = 720
height = 660
num_images = 1
folder_path = pathlib.Path("D:\\CGVR\\CP\\Test\\images\\input")

# Ensure there are JPG files in the folder
jpg_files = sorted(
    (file for file in folder_path.iterdir() if file.suffix == ".jpg"),
    key=lambda x: x.stat().st_mtime
)

if not jpg_files:
    print("No JPG files found in the input folder.")
    exit(1)

image_path = jpg_files[-1]
image = Image.open(image_path)

# Generate prompt using Ollama
try:
    with open(image_path, 'rb') as file:
        response = ollama.chat(
            model='llava',
            messages=[
                {
                    'role': 'user',
                    'content': 'Summarize this image as if you would describe it to a child.',
                    'images': [file.read()],
                },
            ], 
            options={"temperature": 0.1}
        )
        prompt = response['message']['content']
        print(f"Generated prompt: {prompt}")
except Exception as e:
    print(f"Failed to generate prompt: {e}")
    exit(1)

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Prepare the payload
payload = {
    "prompt": prompt,
    "steps": steps,
    "cfg_scale": cfg_scale,
    "width": width,
    "height": height,
    "n_iter": num_images
}

# Send the request to the Stable Diffusion API
try:
    response = requests.post(api_url, json=payload)
    if response.status_code == 200:
        result = response.json()
        for idx, img_base64 in enumerate(result.get("images", [])):
            output_image = Image.open(BytesIO(base64.b64decode(img_base64)))
            output_path = os.path.join(output_folder, f"generated_image_.png")
            output_image.save(output_path)
            print(f"Generated image saved to: {output_path}")
    else:
        print(f"Failed to generate images. Status Code: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Error occurred while generating images: {e}")
