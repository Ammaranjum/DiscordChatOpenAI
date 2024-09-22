import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the token
discord_token = os.getenv("AZURE_OPENAI_API_KEY")

# Print the token for debugging
print("Disco Token:", discord_token)  # For debugging only, remove this before deploying
