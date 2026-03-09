import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    abs_working_directory = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(
    os.path.join(abs_working_directory, file_path)
    )
    common_path = os.path.commonpath([abs_working_directory, target_file_path])
    if common_path != abs_working_directory:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(target_file_path, "r") as file:
            # Read the first chunk
            content = file.read(MAX_CHARS)
            # Peek: try to read one more character; it's like a scroll - it's currently at 10000 char and (1) it's like moving pointer to one after that
            if file.read(1):
                # if we get something, the file was bigger than 10,000
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content
    except Exception as e:
        return f'Error: {e}'
