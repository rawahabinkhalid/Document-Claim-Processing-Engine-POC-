import os
import base64
from langchain.tools import tool
from openai import AzureOpenAI
import httpx

class VisionTools():

    @tool("Analyze the image")
    def analyze_image(image_path:str):
        """Useful to perform image analysis and OCR.
        """
        try:
            with open(image_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('ascii')

            client = AzureOpenAI(
                api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
                api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
                azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
                http_client=httpx.Client(verify=False)
            )

            response = client.chat.completions.create(
                model=os.environ.get("AZURE_MODEL_DEPLOYMENT"),
                messages=[
                    {"role": "system", "content": "You are a professional image analysis expert."},
                    {"role": "user", "content": [
                        {
                            "type": "text",
                            "text": '''Analyze the image and extract required 
                                        information from the image'''
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_image}",
                            }
                        }
                    ]}
                ],
                max_tokens=2000
            )
            return response
        except FileNotFoundError:
            return "Error: Image file not found!"
        except Exception as e:
            return f"{e}"