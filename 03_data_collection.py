import datetime
import os
import subprocess
import json

#  loop through the dataset folder and read git_metadata.json files

# Define the directory where repositories are cloned
repositories_dir = "dummy_projects"  # Replace with the actual directory
data_dir = "dummy_dataset"  # Replace with the actual directory

# Iterate through the cloned repositories and check if repo_name is a directory not file
for repo_name in os.listdir(repositories_dir):
    repo_dir = os.path.join(repositories_dir, repo_name)
    
    # Check if repo_name is a directory not file
    if os.path.isdir(repo_dir):

        # add status key to git_metadata.json file
        with open(os.path.join(data_dir, repo_name, "git_metadata.json"), "r") as git_metadata_file:
            git_metadata = json.load(git_metadata_file)

        execution_metadata = {}

        # check if status key exists and is equal to venv_and_requirements_installed
        if "status" in git_metadata and git_metadata["status"] == "venv_and_requirements_installed":
            # get current time in execution_metadata
            execution_metadata["start_time"] = datetime.datetime.now().isoformat()
            # subprocess to run cli tool
            process = subprocess.Popen(["codegreen", "start-energy-measurement", "--project", repo_dir], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

            output = []
            # write process stdoutput logs while running subprocess in a json file
            with open(os.path.join(data_dir, repo_name, "execution_metadata.json"), "w") as execution_metadata_file:
                for line in process.stdout:
                    print(line, end='')
                    execution_metadata_file.write(line)
                    output.append(line)

            # Wait for the subprocess to complete
            process.wait()

            execution_metadata["end_time"] = datetime.datetime.now().isoformat()
            execution_metadata["output"] = output
            execution_metadata["return_code"] = process.returncode

            if process.returncode == 0:
                print(f"{repo_name} completed successfully.")
                git_metadata["status"] = "codegreen_completed_successfully"
            else:
                print(f"Error running {repo_name}. Return code: {process.returncode}")
                git_metadata["status"] = "codegreen_failed"
        else:
            print(f"{repo_name} skipped.")
            execution_metadata["start_time"] = None
            execution_metadata["end_time"] = None
            execution_metadata["output"] = None
            execution_metadata["return_code"] = None
        
        git_metadata["execution_metadata"] = execution_metadata

        # add git_metadata.json file to dataset folder
        with open(os.path.join(data_dir, repo_name, "git_metadata.json"), "w") as git_metadata_file:
            json.dump(git_metadata, git_metadata_file)


# run all python scripts
# deactivate environment and continue loop
