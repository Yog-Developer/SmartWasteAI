import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

base_url = os.getenv("AZURE_OPENAI_BASE_URL")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

if not all([base_url, api_key, deployment]):
    raise ValueError("Missing Azure credentials in .env file.")

client = OpenAI(
    base_url=base_url,
    api_key=api_key
)

print("Connecting to Azure AI...")

try:
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {
                "role": "system",
                "content": "You are the SmartWaste AI assistant."
            },
            {
                "role": "user",
                "content": "Introduce yourself in one short sentence."
            }
        ]
    )

    print("\nAzure AI connection successful!")
    print("\nModel response:")
    print(response.choices[0].message.content)

except Exception as e:
    print("\nConnection failed.")
    print(str(e))