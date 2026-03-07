import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
       raise RuntimeError("API Key is blank, please add it to the .env file")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
       model="gemini-2.5-flash",
       contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    )
    print(response.text)

if __name__ == "__main__":
    main()
