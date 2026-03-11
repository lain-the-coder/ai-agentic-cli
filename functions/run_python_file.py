import os
from google.genai import types
import subprocess

def run_python_file(working_directory, file_path, args=None):

    abs_working_directory = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(abs_working_directory, file_path))

    common_path = os.path.commonpath([target_file_path, abs_working_directory])
    if common_path != abs_working_directory:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
    if not os.path.isfile(target_file_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file'

    output = ""

    try:
        # Setup the command list
        command = ["python", target_file_path]
        if args is not None:
            command.extend(args)
        # Run the subprocess
        completedProcess = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=abs_working_directory
        )
        # Build the output string
        if completedProcess.returncode != 0:
            output += f"Process exited with code {completedProcess.returncode}\n"
            
        if not completedProcess.stdout and not completedProcess.stderr:
            output += "No output produced"
        else:
            if completedProcess.stdout:
                output += f"STDOUT: {completedProcess.stdout}"
            if completedProcess.stderr:
                if completedProcess.stdout:
                    output += "\n"
                output += f"STDERR: {completedProcess.stderr}"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file and returns the STDOUT and STDERR. Use this to run scripts, tests, or calculations.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the .py file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of command-line arguments to pass to the script.",
            ),
        },
        required=["file_path"],
    ),
)
