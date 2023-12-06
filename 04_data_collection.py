import datetime
import os
import subprocess
import json
# import codegreen.fecom.patching.patching_config


#  loop through the dataset folder and read git_metadata.json files

# Define the directory where repositories are cloned
repositories_dir = "/home/saurabh/method-energy-dataset/projects/1_done"  # Replace with the actual directory
data_dir = "/home/saurabh/method-energy-dataset/dataset"  # Replace with the actual directory

# set environment variable for data and project folder
os.environ["DATA_DIR"] = data_dir
os.environ["PROJECTS_DIR"] = repositories_dir

# codegreen.fecom.patching.patching_config.EXPERIMENT_DIR = data_dir
# codegreen.fecom.patching.patching_config.PROJECT_PATH = repositories_dir

# Iterate through the cloned repositories and check if repo_name is a directory not file
# for repo_name in os.listdir(repositories_dir):
repo_name = "akanyaani_gpt-2-tensorflow2"
repo_dir = os.path.join(repositories_dir, repo_name)

# Check if repo_name is a directory not file
if os.path.isdir(repo_dir):

    # add status key to git_metadata.json file
    with open(os.path.join(data_dir, repo_name, "git_metadata.json"), "r") as git_metadata_file:
        git_metadata = json.load(git_metadata_file)

    # execution_metadata = {}

    # check if status key exists and is equal to venv_and_requirements_installed
    if "status" in git_metadata:
        activate_script = os.path.join(repositories_dir, repo_name,  "venv","bin", "activate")
        activate_cmd = f". {activate_script}" if os.name != "nt" else f"{activate_script}"
        try:
            subprocess.run(activate_cmd, shell=True, check=True)
            print(f"Activated venv for {repo_dir}")
            # print current active environment name
            subprocess.run("echo $VIRTUAL_ENV", shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error while activating venv for {repo_dir}: {e}")
            raise e

        # get current time in execution_metadata
        # execution_metadata["start_time"] = datetime.datetime.now().isoformat()
        # subprocess to run cli tool
        process = subprocess.Popen(["codegreen", "start-energy-measurement", "--project", repo_dir] ,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        # keep track of files that were successful to skip next time

        # create a list to store process output
        # output = []
        # write process stdoutput logs while running subprocess in a json file
        # with open(os.path.join(data_dir, repo_name, "execution_metadata.json"), "w") as execution_metadata_file:
        for line in process.stdout:
            print(line, end='')
                # execution_metadata_file.write(line)
                # output.append(line)

        # Wait for the subprocess to complete
        process.wait()

        # execution_metadata["end_time"] = datetime.datetime.now().isoformat()
        # execution_metadata["output"] = output
        # execution_metadata["return_code"] = process.returncode

        if process.returncode == 0:
            print(f"{repo_name} completed successfully.")
            git_metadata["status"] = "codegreen_completed_successfully"
        else:
            print(f"Error running {repo_name}. Return code: {process.returncode}")
            # git_metadata["status"] = "codegreen_failed"
        # Deactivate the virtual environment
        subprocess.run("deactivate", shell=True, check=True)
    else:
        print(f"{repo_name} skipped.")
        # execution_metadata["start_time"] = None
        # execution_metadata["end_time"] = None
        # execution_metadata["output"] = None
        # execution_metadata["return_code"] = None
    
    # git_metadata["execution_metadata"] = execution_metadata

    # add git_metadata.json file to dataset folder
    with open(os.path.join(data_dir, repo_name, "git_metadata.json"), "w") as git_metadata_file:
        json.dump(git_metadata, git_metadata_file)


# run all python scripts
# deactivate environment and continue loop
