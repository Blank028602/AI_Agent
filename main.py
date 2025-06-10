import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
is_verbose = False

if "--verbose" in sys.argv:
	is_verbose = True 
if len(sys.argv) > 1:
	user_prompt = sys.argv[1]
	messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
	result = client.models.generate_content(model = "gemini-2.0-flash-001", contents = messages)
	print(result.text)
	if is_verbose == True:
		print(f"User prompt: {user_prompt}")
		print(f"Prompt tokens: {result.usage_metadata.prompt_token_count}")
		print(f"Response tokens: {result.usage_metadata.candidates_token_count}")
else: sys.exit(1)

