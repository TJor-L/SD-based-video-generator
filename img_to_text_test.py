# -*- coding: utf-8 -*-
# File : img_to_text_test.py
# Time : 2024/4/5 14:34 
# Author : Dijkstra Liu
# Email : l.tingjun@wustl.edu
# 
# 　　　    /＞ —— フ
# 　　　　　| `_　 _ l
# 　 　　　ノ  ミ＿xノ
# 　　 　 /　　　 　|
# 　　　 /　 ヽ　　ﾉ
# 　 　 │　　|　|　\
# 　／￣|　　 |　|　|
#  | (￣ヽ＿_ヽ_)__)
# 　＼_つ
#
# Description:


import base64
import requests
import os

# Your OpenAI API Key
api_key = ""


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


# Path to your folder containing images
folder_path = "img_data"

# Text file to save descriptions
output_file = "image_descriptions.txt"

# Headers for the HTTP request
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Open the output file in write mode
with open(output_file, "w") as file_out:
    # Loop through each file in the folder
    for image_name in os.listdir(folder_path):
        # Construct the full image path
        image_path = os.path.join(folder_path, image_name)

        # Skip if it's not a file
        if not os.path.isfile(image_path):
            continue

        # Getting the base64 string
        base64_image = encode_image(image_path)

        # JSON payload for the request
        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "describe this image. you shall not begin with 'this image', just simply describe it",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }

        # Send the request to the API
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            # Extract the description from the response
            description = response.json()  # You might need to adjust this line to correctly parse the description
            image_description = description['choices'][0]['message']['content']
            # Write the description to the file
            file_out.write(f"Description for {image_name}: {image_description}\n")
        else:
            print(f"Failed to get description for {image_name}")

# Note: This code is for educational purposes and should be tested and adapted for your specific requirements and API response format.