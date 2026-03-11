import os
from google.genai import types

def write_file(working_directory, file_path, content):

    abs_working_directory = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(
    os.path.join(abs_working_directory, file_path)
    )
    # 1. Security Check
    common_path = os.path.commonpath([target_file_path, abs_working_directory])
    if common_path != abs_working_directory:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    # 2. Collision Check    
    if os.path.isdir(target_file_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
        
    try:
        # Get the directory containing the file; example: "calculator/logs/trace.log" -> "calculator/logs"
        target_dir = os.path.dirname(target_file_path)
        # Create the folder structure if it's missing; exist_ok=True no error is raised if the tgt dir exists
        os.makedirs(target_dir, exist_ok=True)
        # Write the File
        with open(target_file_path, "w") as file:
            file.write(content)
            
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            
    except Exception as e:
        return f'Error: {e}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Creates a new file or overwrites an existing file with the provided content.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path where the file should be created, relative to the working directory.",            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The full text content to be written into the file.",
            ),
        },
        required=["file_path", "content"]
    ),
)
