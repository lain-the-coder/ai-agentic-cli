from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ],
)

def call_function(function_call, verbose=False):

    # Check for verbose command from user for user to see
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")
        
    # Create a dictionary since function calls cannot be made with strings
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file
    }

    # Copy the .name property of function_call argument into a variable since it could be None
    function_name = function_call.name or ""

    # If provided function name is not found in the mapping defined earlier then return a types.Content object
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ]
        )

    # copy the args into a new dict variable since we need to add our own argument like working dir to it
    args = dict(function_call.args) if function_call.args else {}

    # If the AI tries to name the folder we are already in, 
    # we can override it to "." so it doesn't double up the path
    if args.get("directory") == "calculator":
        args["directory"] = "."

    # now add the working_directory arg to the dict; ./calculator means look for a folder named calc that is located here in the same place as my script
    args["working_directory"] = "./calculator"

    # Call functions
    function_result = function_map[function_name](**args)

    # Return the result not as string because Gemini wants it in as types.Content object with types.Part.from_function_response for function calls
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result":function_result},
            )
        ]
    )    

    
