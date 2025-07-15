import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
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

def get_files_info(working_directory, directory=None):
    try:
        
        full_path = os.path.join(working_directory, directory)
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_dir = os.path.abspath(full_path)

        if not abs_target_dir.startswith(abs_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
        if not os.path.isdir(abs_target_dir):
            return f'Error: "{directory}" is not a directory'
    
        result_lines = []

        for dir in os.listdir(abs_target_dir):
            full_item_path = os.path.join(abs_target_dir, dir)
            file_size = os.path.getsize(full_item_path)
            is_directory = os.path.isdir(full_item_path)
        
            result_lines.append(f"- {dir}: file_size={file_size} bytes, is_dir={is_directory}")

        result = "\n".join(result_lines)
    
        return result

    except Exception as e:
        return f"Error: {str(e)}"
