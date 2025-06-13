import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
is_verbose = False
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

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

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

if "--verbose" in sys.argv:
	is_verbose = True
if len(sys.argv) > 1:
	user_prompt = ' '.join(sys.argv[1:])
	messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
	response = client.models.generate_content(model =  "gemini-1.5-flash-latest", contents = messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),)
	if response.function_calls:
		print(f"Calling function: {response.function_calls[0].name}({response.function_calls[0].args})")
		print(response.text)
	else: print(response.text)
	if is_verbose == True:
		print(f"User prompt: {user_prompt}")
		print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
		print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
else: sys.exit(1)

