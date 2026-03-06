import os
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
