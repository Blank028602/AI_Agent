import os

def get_files_info(working_directory, directory=None):

	if directory is None:
		directory = working_directory

	if directory.startswith("/"):
		directory = os.path.abspath(directory)

	else:
		full_path = os.path.join(working_directory, directory)
		directory = os.path.abspath(full_path)

	working_directory = os.path.abspath(working_directory)
	result = directory.startswith(working_directory)


	if result == False:
		return f"Error: Cannot list '{directory}' as it is outside the permitted working directory"
	elif os.path.isdir(directory) == False:
		return f"Error: '{directory}' is not a directory"
	elif result and os.path.isdir(directory):
		lines = []
		try:
			for item in os.listdir(directory):
				full_path = os.path.join(directory, item)
				is_dir = os.path.isdir(full_path)
				size = os.path.getsize(full_path)
				line = f"- {item}: file_size={size} bytes, is_dir={is_dir}"
				lines.append(line)
			result = "\n".join(lines)
			return result
		except FileNotFoundError:
			return "Error: File not found"
		except PermissionError:
			return "Error: Permission denied"
		except OSError:
			return "Error: Could not access directory"


def get_file_content(working_directory, file_path):

	working_directory = os.path.abspath(working_directory)
	full_file_path = os.path.join(working_directory, file_path)
	full_file_path = os.path.abspath(full_file_path)
	result = full_file_path.startswith(working_directory)

	try:
		if result == False:
			return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

		if os.path.isfile(full_file_path) == False:
			return f'Error: File not found or is not a regular file: "{file_path}"'

		with open(full_file_path, "r") as f:
			file_content_string = f.read(10001)
			if len(file_content_string) > 10000:
				full_file_content_string = file_content_string[:10000] + f'[...File "{file_path}" truncated at 10000 characters]'
				return full_file_content_string
			elif len(file_content_string) < 10000:
				return file_content_string
			elif len(file_content_string) == 10000:
				return file_content_string

	except FileNotFoundError:
		return "Error: File not found"
	except PermissionError:
		return "Error: Permission denied"
	except OSError:
		return "Error: Could not access directory"



























