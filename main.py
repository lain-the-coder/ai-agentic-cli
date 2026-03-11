import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions

load_dotenv()

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("API Key is blank, please add it to the .env file")
    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser(description="AI Agentic CLI tool")
    parser.add_argument("prompt", type=str, help="Provide your prompt here")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Constructing the message - a list that holds the entire history of the chat
    # types.Content is a single entry in the chat, if multiple, then multiple types.Content in the messages list separated by comma
    # role is the identity and first arg for types.Content
    # parts is the payload list that holds the actual data
    # types.Part is an individual item, multiple data which will have multiple lines of types.Part separated by comma in parts list
    # the data - the final argument where your actual content lives
    messages = [
       types.Content(
          role="user",
          parts=[
              types.Part(
                   text=args.prompt
              )
          ]
       )
    ]
    response = client.models.generate_content(
       model="gemini-2.5-flash",
       contents=messages,
       config=types.GenerateContentConfig(
       tools=[available_functions],
        system_instruction=system_prompt
       ),
    )
    if response.usage_metadata is None:
        raise RuntimeError("Failed API Request, please try again later")
    else:
        # Check for function calls
        function_calls = response.function_calls
        if args.verbose:
            print(f"User prompt: {args.prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")
        print("Response:")
        if function_calls:
            for function_call in function_calls:
                print(f"Calling function: {function_call.name}({function_call.args})")  
        else:
            print(response.text)
if __name__ == "__main__":
    main()
