import os
import subprocess


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a specified Python file within the working directory and returns its output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to run, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of arguments to pass to the Python script",
                },
            },
            "required": ["file_path"],
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_filepath = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_filepath = (
            os.path.commonpath([working_dir_abs, target_filepath]) == working_dir_abs
        )
        if not valid_target_filepath:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_filepath):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_filepath.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_filepath]
        if args is not None:
            command.extend(args)

        execute = subprocess.run(command, cwd=working_dir_abs, capture_output = True, text = True, timeout = 30)

        if execute.returncode > 0:
            return f"Process exited with code {execute.returncode}"

        if execute.stdout == None and execute.stderr == None:
            return "No output produced"

        output_str = f"STDOUT:{execute.stdout}, STDERR:{execute.stderr}"
        return output_str

    except Exception as e:
        return f"Error: executing Python file: {e}"
