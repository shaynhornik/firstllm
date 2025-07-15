import os
from dotenv import load_dotenv
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai
import sys
from google.genai import types

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file
    ]
)


system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

user_prompt = sys.argv[1]

messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)]),
            ]

client = genai.Client(api_key=api_key)

is_verbose = False

if len(sys.argv)<2:
    print("Error")
    sys.exit(1)

for i in range(20):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
        )

        # Always append the model's response (candidate content) to messages first.
        # This records what the model "said" or "intended to do".
        for candidate in response.candidates:
            messages.append(candidate.content)

        # Now, check if the model is making function calls.
        if response.function_calls != None:
            # If there are function calls, process them as before
            for function_call_part in response.function_calls:
                result = call_function(function_call_part, verbose=is_verbose)
                messages.append(types.Content(role="tool", parts=[result.parts[0]])) # Append tool result

                if result.parts[0].function_response.response == None:
                    raise Exception("Fatal Error")
                elif is_verbose == True:
                    print(f"-> {result.parts[0].function_response.response}")
        # If there are NO function calls, then check for a final text response.
        elif response.text:
            print(response.text)
            break # Exit loop if final text response is received

        # The verbose output for prompt/response tokens should also be inside the loop
        # and after the initial response is received.
        is_verbose = False # Reset or determine verbose each iteration
        if (len(sys.argv)>2 and (sys.argv[2] == "--verbose")):
            print(f"User prompt: {user_prompt}") # This line is potentially redundant inside loop
            print("Prompt tokens: " + str(response.usage_metadata.prompt_token_count))
            print("Response tokens: " + str(response.usage_metadata.candidates_token_count))
            is_verbose = True

        # The sys.argv<2 check is already correctly outside the loop.
        # This part should be removed from here:
        # if len(sys.argv)<2:
        #     print("Error")
        #     sys.exit(1)

    except Exception as e:
        print(f"An error occurred: {e}")
        # Consider if you want to break here or continue. For fatal errors, breaking is fine.
        break # Added break to prevent infinite error loops
