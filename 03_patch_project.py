import datetime
import os
import subprocess
import json
import shutil
from codegreen.fecom.patching.repo_patching import patch_project
from utils.metadata import get_repo_metadata, get_script_path
from pathlib import Path
from fecom.patching.patching_config import EXPERIMENT_DIR

import csv

directory_names = []

# get directories_info.csv and read directory name from "Directory name" column field into a list
with open("./filter/directories_info.csv", 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    # read value of "Directory name" column and append to list and move to next row
    for row in reader:
        if row[2]== "Notebooks exist":
            directory_names.append(row[0])

# import codegreen.fecom.patching.patching_config


#  loop through the dataset folder and read git_metadata.json files

# Define the directory where repositories are cloned
repositories_dir = "projects/"  # Replace with the actual directory
data_dir = "dataset"  # Replace with the actual directory

# set environment variable for data and project folder
os.environ["DATA_DIR"] = data_dir
os.environ["PROJECTS_DIR"] = repositories_dir

def project_patcher(
    project : Path,
    ):
    """
    This will start patching the scripts.
    """
    # Start patching all the files in the argument and store them in the same location as the original file with suffix "_patched"
    project = project.resolve()
    patched_dir = project.parent / (project.stem + "_patched")
    metadata = get_repo_metadata(project)
    print("metadata",metadata)
    method_level_python_scripts, project_level_python_scripts, og_python_scripts, scripts_with_target_framework = patch_project(patched_dir,project,metadata)
    print("method_level_python_scripts",method_level_python_scripts)

        # create a list with json objects having filepaths of scripts_with_target_framework and their corresponding execution status
    # This will be used to determine if the script was executed successfully after patching and also contain logs for the file
    scripts_execution_metadata = []
    script_status = {}
    for script in scripts_with_target_framework:
        # get file name from the script_to_run path with removed "_method-level.py" substring
        # base_script_path = os.path.basename(script).replace("_method-level.py","")
        script_status[str(script)] = "not_executed_yet"
    
    # store the metadata of the experiment in the experiment directory
    with open(EXPERIMENT_DIR/ Path(project.stem) / Path("scripts_execution_metadata.json"), "w") as f:
        f.write(str(script_status))

    # store the metadata of the experiment in the experiment directory
    with open(EXPERIMENT_DIR/ Path(project.stem) / Path("scripts_execution_status.json"), "w") as f:
        f.write(str(script_status))

# codegreen.fecom.patching.patching_config.EXPERIMENT_DIR = data_dir
# codegreen.fecom.patching.patching_config.PROJECT_PATH = repositories_dir

# delete patched repositories that end with repo_name+'_patched'
# for repo_name in os.listdir(repositories_dir):
#     # repo_name = "ahmetozlu_tensorflow_object_counting_api"
#     repo_dir = os.path.join(repositories_dir, repo_name)

#     # Check if repo_name is a directory not file
#     if os.path.isdir(repo_dir):
        # patched_repo_dir = os.path.join(repositories_dir, repo_name+'_patched')
        # if os.path.isdir(patched_repo_dir):
        #     print(f"Deleting {patched_repo_dir}")
        #     # use os to delete the directory
        #     shutil.rmtree(patched_repo_dir)


# Iterate through the cloned repositories and check if repo_name is a directory not file
# for repo_name in os.listdir(repositories_dir):
#     # repo_name = "ahmetozlu_tensorflow_object_counting_api"
#     repo_dir = os.path.join(repositories_dir, repo_name)

#     # Check if repo_name is a directory not file
#     if os.path.isdir(repo_dir):

#         # add status key to git_metadata.json file
#         with open(os.path.join(data_dir, repo_name, "git_metadata.json"), "r") as git_metadata_file:
#             git_metadata = json.load(git_metadata_file)

#         process = subprocess.Popen(["codegreen", "project-patcher", "--project", repo_dir] ,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
#         for line in process.stdout:
#             print(line, end='')

#         # Wait for the subprocess to complete
#         process.wait()

#         if process.returncode == 0:
#             print(f"{repo_name} patching successfully.")
#             git_metadata["status"] = "patching_successfully"
#         else:
#             print(f"Error patching {repo_name}. Return code: {process.returncode}")
#             # git_metadata["status"] = "patching_failed"

#         with open(os.path.join(data_dir, repo_name, "git_metadata.json"), "w") as git_metadata_file:
#             json.dump(git_metadata, git_metadata_file)

directory_names = ["tensorflow_quantum"]
for repo_name in directory_names:
# repo_name = "akanyaani_gpt-2-tensorflow2"
    repo_dir = os.path.join(repositories_dir, repo_name)
    patched_repo_dir = os.path.join(repositories_dir, repo_name+'_patched')
    if os.path.isdir(patched_repo_dir):
        print(f"Deleting {patched_repo_dir}")
        # use os to delete the directory
        shutil.rmtree(patched_repo_dir)

    # Check if repo_name is a directory not file
    if os.path.isdir(repo_dir):

        # add status key to git_metadata.json file
        with open(os.path.join(data_dir, repo_name, "git_metadata.json"), "r") as git_metadata_file:
            git_metadata = json.load(git_metadata_file)

        project_patcher(Path(repo_dir))

        # process = subprocess.Popen(["codegreen", "project-patcher", "--project", repo_dir] ,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        # for line in process.stdout:
        #     print(line, end='')

        # # Wait for the subprocess to complete
        # process.wait()

        # if process.returncode == 0:
        #     print(f"{repo_name} patching successfully.")
        #     git_metadata["status"] = "patching_successfully"
        # else:
        #     print(f"Error patching {repo_name}. Return code: {process.returncode}")
        #     # git_metadata["status"] = "patching_failed"

        with open(os.path.join(data_dir, repo_name, "git_metadata.json"), "w") as git_metadata_file:
            json.dump(git_metadata, git_metadata_file)


# run all python scripts
# deactivate environment and continue loop

