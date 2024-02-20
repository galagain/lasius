import os
import subprocess


def execute_commands(commands: list[str], work_path: str = os.getcwd()) -> None:
    """Executes a list of shell commands in a specified working directory.

    Args:
        commands (list[str]): A list of shell commands to be executed.
        work_path (str): The directory in which the commands should be executed.
                         Defaults to the current working directory of the script.
    """
    for command in commands:
        # Create the working directory if it does not exist
        if not os.path.exists(work_path):
            os.makedirs(work_path)

        # Execute each command in the specified working directory
        subprocess.run(command, shell=True, cwd=work_path)
