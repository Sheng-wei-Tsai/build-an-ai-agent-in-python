import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
  try:
    abs_working_directory = os.path.abspath(working_directory)
    target_path = os.path.abspath(
        os.path.join(abs_working_directory, file_path)
    )
    if os.path.commonpath([abs_working_directory, target_path]) != abs_working_directory:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    with open(target_path, "r") as f:
      content = f.read(MAX_CHARS)
      if f.read(1):
        content += f'[...File] "{file_path}" truncated at {MAX_CHARS} characters]'
    return content
  except Exception as e:
    return f"Error: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)
