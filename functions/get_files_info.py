import os
def get_files_info(working_directory, directory="."):
  try:
    # 1. Absolute path of the working directory
    working_dir_abs = os.path.abspath(working_directory)

    # 2. Build the normalized absolute path to the target directory
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

    # 3. Validate target_dir is inside working_dir_abs
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    if not valid_target_dir:
        raise ValueError(f"Error: cannot list files in '{directory}'as it is outside the permitted working directory.")

    # 4. Ensure it's actually a directory
    if not os.path.isdir(target_dir):
        raise ValueError(f"Error: '{directory}' is not a valid directory.")

    # 5. Interate items and collect formatted info
    lines = []
    for name in os.listdir(target_dir):
        item_path = os.path.join(target_dir, name)
        is_dir = os.path.isdir(item_path)
        file_size = os.path.getsize(item_path)
        lines.append(f"- {name}: file_size={file_size} bytes, is_dir={is_dir}")

    lines.sort()
    return "\n".join(lines)
  except Exception as e:
    return f"Error: {e}"


