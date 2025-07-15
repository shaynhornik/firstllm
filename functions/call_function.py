from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file # Correct Python function import
from functions.write_file import write_file
from google.genai import types

def call_function(function_call_part, verbose=False):
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    # Initialize actual_args here to hold the arguments we'll pass to the functions
    actual_args = {}

    # Copy all arguments from the LLM's function_call_part.args first
    # This covers cases where argument names already match
    actual_args.update(function_call_part.args)

    # Manually add the working_directory to the arguments for ALL calls
    actual_args["working_directory"] = "./calculator"

# ... (rest of your code above) ...

    result = None # Initialize result to None

    # LLM sends "run_python_file"
    if function_call_part.name == "run_python_file": # <--- CHANGE THIS LINE
        # The LLM gives 'directory', but run_python_file expects 'file_path'
        if 'directory' in actual_args:
            actual_args['file_path'] = actual_args.pop('directory')
        result = run_python_file(**actual_args)

    # LLM sends "get_file_content"
    elif function_call_part.name == "get_file_content": # <--- CHANGE THIS LINE
        # The LLM gives 'directory', but get_file_content expects 'file_path'
        if 'directory' in actual_args:
            actual_args['file_path'] = actual_args.pop('directory')
        result = get_file_content(**actual_args)

    # LLM sends "write_file" (this one is already correct)
    elif function_call_part.name == "write_file":
        result = write_file(**actual_args)

    # LLM sends "get_files_info"
    elif function_call_part.name == "get_files_info": # <--- CHANGE THIS LINE
        result = get_files_info(**actual_args)

    # ... (rest of your code below) ...    # --- End of conditional logic ---

    else:
        # This handles cases where the LLM calls an unknown function name
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    # This return statement is for successful function calls
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result},
            )
        ],
    )
