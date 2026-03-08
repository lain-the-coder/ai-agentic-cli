import os
import argparse
from dotenv import load_dotenv
from google import genai

load_dotenv()

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
       raise RuntimeError("API Key is blank, please add it to the .env file")
    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser(description="AI Agentic CLI tool")
    parser.add_argument("prompt", type=str, help="Provide your prompt here")
    args = parser.parse_args()
    response = client.models.generate_content(
       model="gemini-2.5-flash",
       contents=args.prompt
    )
    if response.usage_metadata is None:
       raise RuntimeError("Failed API Request, please try again later")
    else:
       print("User prompt: Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")
       print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")
       print(f"Response:\n{response.text}")

if __name__ == "__main__":
    main()
