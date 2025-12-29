# config stuff - handles env vars
import os
from dotenv import load_dotenv

load_dotenv()  # load .env file
# TODO: maybe add validation for the api key format?

def get_openrouter_api_key():
    # gets the api key from env, throws error if not found
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY not found. Please set it in your .env file or environment variables.\n"
            "Create a .env file in the project root with: OPENROUTER_API_KEY=your_api_key_here\n"
            "Get your API key from: https://openrouter.ai/keys"
        )
    return api_key

def get_openrouter_model():
    # default model is gpt-4o-mini, can override in .env
    return os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

