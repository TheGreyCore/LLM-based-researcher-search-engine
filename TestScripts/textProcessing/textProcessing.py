import os
from aiLib import AILib

client = AILib(
    api_key=os.environ["OPENAI_API_KEY"],
    api_version="2024-02-01",
    azure_endpoint="https://tu-openai-api-management.azure-api.net/oltatkull/openai/deployments/IDS2024_MATETSKI_gpt_4o_mini/chat/completions?api-version=2024-02-01"
)

input_text = "Find me all researchers in the University of Tartu who have applied machine learning in their papers."

response = client.extract(input_text)

print(response)