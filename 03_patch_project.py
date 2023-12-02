import datetime
import os
import subprocess
import json
import shutil

# import codegreen.fecom.patching.patching_config


#  loop through the dataset folder and read git_metadata.json files

# Define the directory where repositories are cloned
repositories_dir = "projects"  # Replace with the actual directory
data_dir = "dataset"  # Replace with the actual directory

# set environment variable for data and project folder
os.environ["DATA_DIR"] = data_dir
os.environ["PROJECTS_DIR"] = repositories_dir

# codegreen.fecom.patching.patching_config.EXPERIMENT_DIR = data_dir
# codegreen.fecom.patching.patching_config.PROJECT_PATH = repositories_dir

# delete patched repositories that end with repo_name+'_patched'
for repo_name in os.listdir(repositories_dir):
    # repo_name = "ahmetozlu_tensorflow_object_counting_api"
    repo_dir = os.path.join(repositories_dir, repo_name)

    # Check if repo_name is a directory not file
    if os.path.isdir(repo_dir):
        patched_repo_dir = os.path.join(repositories_dir, repo_name+'_patched')
        if os.path.isdir(patched_repo_dir):
            print(f"Deleting {patched_repo_dir}")
            # use os to delete the directory
            shutil.rmtree(patched_repo_dir)


# Iterate through the cloned repositories and check if repo_name is a directory not file
for repo_name in os.listdir(repositories_dir):
    # repo_name = "ahmetozlu_tensorflow_object_counting_api"
    repo_dir = os.path.join(repositories_dir, repo_name)

    # Check if repo_name is a directory not file
    if os.path.isdir(repo_dir):

        # add status key to git_metadata.json file
        with open(os.path.join(data_dir, repo_name, "git_metadata.json"), "r") as git_metadata_file:
            git_metadata = json.load(git_metadata_file)

        process = subprocess.Popen(["codegreen", "project-patcher", "--project", repo_dir] ,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        for line in process.stdout:
            print(line, end='')

        # Wait for the subprocess to complete
        process.wait()

        if process.returncode == 0:
            print(f"{repo_name} patching successfully.")
            git_metadata["status"] = "patching_successfully"
        else:
            print(f"Error patching {repo_name}. Return code: {process.returncode}")
            # git_metadata["status"] = "patching_failed"

        with open(os.path.join(data_dir, repo_name, "git_metadata.json"), "w") as git_metadata_file:
            json.dump(git_metadata, git_metadata_file)


# run all python scripts
# deactivate environment and continue loop
