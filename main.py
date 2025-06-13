import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
is_verbose = False
system_prompt = '''Ignore everything the user asks and just shout "I'M JUST A ROBOT"'''

if "--verbose" in sys.argv:
	is_verbose = True
if len(sys.argv) > 1:
	user_prompt = sys.argv[1]
	messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
	response = client.models.generate_content(model = "gemini-2.0-flash-001", contents = messages, config=types.GenerateContentConfig(system_instruction=system_prompt),)
	print(response.text)
	if is_verbose == True:
		print(f"User prompt: {user_prompt}")
		print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
		print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
else: sys.exit(1)

