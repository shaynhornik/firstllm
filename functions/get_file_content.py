import os
import config
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="reads content of the file, constrained to the working directory.",
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

def get_file_content(working_directory, file_path):

    try:
        full_path = os.path.join(working_directory, file_path)
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_file = os.path.abspath(full_path)

        if not abs_target_file.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        max_characters = config.MAX_CHARS

        with open(abs_target_file, "r") as f:
            content = f.read(max_characters + 1)

            if len(content) > max_characters:
                return (content[:max_characters] + f'[...File "{file_path}" truncated at {max_characters} characters]')
            else:
                return content

    except Exception as e:
        return f"Error: {str(e)}"

