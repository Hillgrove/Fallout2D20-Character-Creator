import os
import subprocess
import sys

# Define the folder containing the scripts
scripts_folder = os.path.dirname(__file__)

# List of population scripts to run
scripts = [
    "populate_origins_and_traits.py",
    "populate_stats.py",
    "populate_perks.py",
    "populate_skills.py",
    "populate_attributes.py"
]

def run_script(script_folder, script_name):
    script_path = os.path.join(script_folder, script_name)
    python_executable = sys.executable  # Get the current Python interpreter
    try:
        # Ensure the working directory is set to the script folder
        result = subprocess.run([python_executable, script_path], check=True, capture_output=True, text=True, cwd=script_folder)
        print(f"Script {script_path} executed successfully.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running script {script_path}.")
        print(e.stderr)

def main():
    for script in scripts:
        run_script(scripts_folder, script)

if __name__ == "__main__":
    main()
