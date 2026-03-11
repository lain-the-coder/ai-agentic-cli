import os
from google.genai import types

def get_files_info(working_directory, directory="."):

    # Find Baseline absolute path
    abs_working_directory = os.path.abspath(working_directory)

    # Find target by combining absolute and directory AI wants to access
    target_dir = os.path.normpath(os.path.join(abs_working_directory, directory))

    # Security check - find the longest common path and verify if it's same as absolute working path, if not then directory tried to escape
    common_path = os.path.commonpath([abs_working_directory, target_dir])
    if common_path != abs_working_directory:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    # Check if the final requested directory is an actual directory
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    # Create a container for our lines since we can't print, we collect as we go
    items = []

    try:
        # loop through items in a dir path
        for item in os.listdir(target_dir):
            # always use os.path.join to get append paths
            item_path = os.path.join(target_dir, item)
            # get size of file or dir
            size = os.path.getsize(item_path)
            # check if it is a directory or not
            is_dir = os.path.isdir(item_path)
            # add to a list
            items.append(f"- {item}: file_size={size} bytes, is_dir={is_dir}")
        # combine list into a string separated by newlines
        return '\n'.join(items)
    except Exception as e:
        return f'Error: {e}'
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
