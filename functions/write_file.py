import os
from google.genai import types

def write_file(working_directory, file_path, content):
  try:
    abs_working_directory = os.path.abspath(working_directory)
    target_path = os.path.abspath(
        os.path.join(abs_working_directory, file_path)
    )
    if os.path.commonpath([abs_working_directory, target_path]) != abs_working_directory:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    parent_directory = os.path.dirname(target_path)
    os.makedirs(parent_directory, exist_ok=True)

    with open(target_path, "w") as f:
      f.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
  except Exception as e:
    return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites the contents of a file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text content to write into the file",
            ),
        },
        required=["file_path", "content"],
    ),
)