import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info, get_file_content, run_python_file, write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
is_verbose = False
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
schema_get_files_info = types.FunctionDeclaration(
	name="get_files_info",
	description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
	parameters=types.Schema(
		type=types.Type.OBJECT,
		properties={
			"directory": types.Schema(
				type=types.Type.STRING,
				description="The directory (relative to the working directory) to list files from. Use '.' to indicate the working directory itself.",
			),
		},
		required=["directory"]
	),
)
schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Lists the length of the specified file and returns the content, constrained to the working directory.",
        parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                        "file_path": types.Schema(
                                type=types.Type.STRING,
                                description="The path to the file in question (relative to the working directory). Use '.' to indicate the working directory itself.",
                        ),
                },
                required=["file_path"]
        ),
)
schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Runs a specified python file, constrained to the working directory.",
        parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                        "file_path": types.Schema(
                                type=types.Type.STRING,
                                description="The path to the file in question (relative to the working directory). Use '.' to indicate the working directory itself.",
                        ),
                },
                required=["file_path"]
        ),
)
schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Overwrites the content of a specified file, constrained to the working directory.",
        parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                        "file_path": types.Schema(
                                type=types.Type.STRING,
                                description="The path to the file in question (relative to the working directory). Use '.' to indicate the working directory itself.",),
			"content": types.Schema(
				type=types.Type.STRING,
				description="The content that overwrites the content of the given file"
                        ),
                },
                required=["file_path", "content"]
        ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
	schema_get_file_content,
	schema_run_python_file,
	schema_write_file,
    ]
)

def call_function(function_call_part, verbose=False):
	if verbose == True:
		print(f"Calling function: {function_call_part.name}({function_call_part.args})")
	else:
		print(f" - Calling function: {function_call_part.name}")

	function_map = {
		"get_files_info": get_files_info,
		"get_file_content": get_file_content,
		"run_python_file": run_python_file,
		"write_file": write_file,
		}

	if function_call_part.name not in function_map:
                return types.Content(
                        role="tool",
                        parts=[
                                types.Part.from_function_response(
                                        name=function_call_part.name,
                                        response={"error": f"Unknown function: {function_call_part.name}"},
                                )
                        ],
                )

	else:
		actual_function = function_map[function_call_part.name]
		args = function_call_part.args.copy()
		args["working_directory"] = "./calculator"
		result = actual_function(**args)
		return types.Content(
			role="tool",
			parts=[
				types.Part.from_function_response(
					name=function_call_part.name,
					response={"result": result},
				)
			],
		)


if "--verbose" in sys.argv:
	is_verbose = True
if len(sys.argv) > 1:
	user_prompt = ' '.join(sys.argv[1:])
	messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
	response = client.models.generate_content(model =  "gemini-1.5-flash-latest", contents = messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),)
	if response.function_calls:
		function_call_result = call_function(response.function_calls[0], verbose=is_verbose)
		if function_call_result.parts[0].function_response.response:
			if is_verbose:
				print(f"-> {function_call_result.parts[0].function_response.response}")
		else:
			raise Exception("Function call didn't return expected response structure")
	if is_verbose == True:
		print(f"User prompt: {user_prompt}")
		print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
		print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
else: sys.exit(1)

