import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

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
    # Agent Loop (max 20 attempts)
    for _ in range(20):
        # Reset the results list for this specific turn
        function_results=[]
        # Call the model
        response = client.models.generate_content(
           model="gemini-2.5-flash",
           contents=messages,
           config=types.GenerateContentConfig(
           tools=[available_functions],
            system_instruction=system_prompt
           ),
        )
        # Process the response
        if response.usage_metadata is None:
            raise RuntimeError("Failed API Request, please try again later")
        else:
            # Record what the model just said/requested
            if response.candidates:
                for candidate in response.candidates:
                    messages.append(candidate.content)
            # Check for function calls
            function_calls = response.function_calls
            if args.verbose:
                print(f"User prompt: {args.prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")
            print("Response:")
            if function_calls:
                for function_call in function_calls:
                    function_call_result = call_function(function_call, args)
                    if not function_call_result.parts:
                        raise RuntimeError("Empty .parts list")
                    if not function_call_result.parts[0].function_response:
                        raise RuntimeError("Returned None value")
                    if not function_call_result.parts[0].function_response.response:
                        raise RuntimeError("Returned None value")
                    function_results.append(function_call_result.parts[0])
                    if args.verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
            else:
                print(response.text)
                return # if there are no function calls, the agent is DONE
if __name__ == "__main__":
    main()
