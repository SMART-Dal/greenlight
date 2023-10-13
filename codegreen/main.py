import typer
from rich import print
from rich.markdown import Markdown
from codegreen.fecom.measurement import start_measurement
from typing_extensions import Annotated
from pathlib import Path
from typing import List
import shutil

import subprocess
from codegreen.fecom.patching.patching_config import METHOD_LEVEL_PATCHING_SCRIPT_PATH
from codegreen.fecom.patching.repo_patching import patch_project
import git
import os

app = typer.Typer(rich_markup_mode="rich",help="[green]🍃 CodeGreen: Your Passport to a Greener Code! 🍃[/green]")


def get_repo_metadata(repo_dir):
  metadata = {}
  
  try:

    repo = git.Repo(repo_dir)

    # Project name
    metadata["project_name"] = os.path.basename(repo_dir)

    # Project repository 
    metadata["project_repository"] = repo.remote().url

    # Project owner
    metadata["project_owner"] = repo.remote().url.split("/")[-2]

    # Project branch
    metadata["project_branch"] = repo.active_branch.name

    # Project commit
    metadata["project_commit"] = repo.head.commit.hexsha

    # Project commit date
    metadata["project_commit_date"] = repo.head.commit.committed_datetime.isoformat()

    # Script path - would need to pass this explicitly
    metadata["script_path"] = None

    # API call line - would need to parse files to get this
    metadata["api_call_line"] = None

  except git.InvalidGitRepositoryError:
    print(f"{repo_dir} is not a Git repository, so git metadata cannot be retrieved.")

  return metadata

@app.command()
def run_energy_profiler():
    """
    This command will start the energy measurement server
    """
    print("Starting measurement...")
    start_measurement.main()

@app.command()
def start_energy_measurement(
    project : Annotated[Path,typer.Option(help="Path to the source code of the project to be measured.")],
    scripts : Annotated[List[Path],typer.Option(help="List of paths to the project scripts to be measured.")],
):
    """
    This command will start running the scripts and collecting data for energy measurement.
    """
    # Start patching all the files in the argument and store them in the same location as the original file with suffix "_patched"
    project = project.resolve()
    patched_dir = project.parent / (project.stem + "_patched")
    metadata = get_repo_metadata(project)
    print("metadata",metadata)
    method_level_python_scripts, project_level_python_scripts, og_python_scripts = patch_project(patched_dir,project,metadata)

    # run the patched files in the provided sequence in arguments
    for idx, script in enumerate(method_level_python_scripts):
        # script = script.resolve()
        print(f"Running {script}...")
        base_path, ext = os.path.splitext(og_python_scripts[idx])
        
        # Start the subprocess
        process = subprocess.Popen(['python3', script,"1",base_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        # Capture and print the output in real-time
        for line in process.stdout:
            print(line, end='')

        # Wait for the subprocess to complete
        process.wait()

        if process.returncode == 0:
            print(f"{script} completed successfully.")
        else:
            print(f"Error running {script}. Return code: {process.returncode}")

    # store the data and log

    # Delete the patched directory
    # shutil.rmtree(patched_dir)
    # print(f"Deleted {patched_dir}")

    # stop measurement process

# only use this by uncommenting for testing purposes
if __name__ == "__main__":
    app()