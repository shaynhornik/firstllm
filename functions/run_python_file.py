import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Returns the outputs of running a subprocess of a taget py file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path):

    try:

        full_path = os.path.join(working_directory, file_path)
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_file = os.path.abspath(full_path)
        
        if not abs_target_file.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(abs_target_file):
            return f'Error: File "{file_path}" not found.'

        if not abs_target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        result = subprocess.run(["python3", f'{abs_target_file}'], capture_output=True, cwd=abs_working_dir, timeout=30, text=True) 

        if (result.stdout == "") and (result.stderr == ""):
            return "No output produced"

        final_result = ""

        final_result += "STDOUT:" + result.stdout
        final_result += "STDERR:" + result.stderr

        if result.returncode != 0:
            final_result += f"Process exited with code {result.returncode}"

        return final_result

    except Exception as e:
        return f"Error: {str(e)}"

