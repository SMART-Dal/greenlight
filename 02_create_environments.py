import os
import subprocess
import json

# Define the directory where repositories are cloned
repositories_dir = "projects"  # Replace with the actual directory
data_dir = "dataset"  # Replace with the actual directory

# Function to create a virtual environment and install packages
def create_venv_and_install_requirements(repo_dir):
    venv_dir = os.path.join(repo_dir, "venv")
    requirements_file = os.path.join(repo_dir, "requirements.txt")
    
    if not os.path.exists(venv_dir):
        # Create a virtual environment
        try:
            subprocess.run(["python", "-m", "venv", venv_dir], check=True)
            print(f"Successfully created venv for {repo_dir}")
        except subprocess.CalledProcessError as e:
            print(f"Error while creating venv for {repo_dir}: {e}")
            raise e

    if os.path.exists(requirements_file):
        # Activate the virtual environment
        activate_script = os.path.join(venv_dir, "bin", "activate")
        activate_cmd = f". {activate_script}" if os.name != "nt" else f"{activate_script}"
        try:
            subprocess.run(activate_cmd, shell=True, check=True)
            print(f"Activated venv for {repo_dir}")
            # print current active environment name
            subprocess.run("echo $VIRTUAL_ENV", shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error while activating venv for {repo_dir}: {e}")
            raise e

        # Install packages using pip
        try:
            print("__"*50)
            subprocess.run(["pip", "install", "-r", requirements_file], check=True)
            print(f"Successfully installed requirements for {repo_dir}")
        except subprocess.CalledProcessError as e:
            print(f"Error while installing requirements for {repo_dir}: {e}")
            raise e

        # Deactivate the virtual environment
        subprocess.run("deactivate", shell=True, check=True)

# Iterate through the cloned repositories and check if repo_name is a directory not file
# for repo_name in os.listdir(repositories_dir):
repo_name ="tensorflow_docs"
repo_dir = os.path.join(repositories_dir, repo_name)

# Check if repo_name is a directory not file
if os.path.isdir(repo_dir):
    # Check if requirements.txt exists
    requirements_file = os.path.join(repo_dir, "requirements.txt")

    # add status key to git_metadata.json file
    with open(os.path.join(data_dir, repo_name, "git_metadata.json"), "r") as git_metadata_file:
        git_metadata = json.load(git_metadata_file)

    if os.path.exists(requirements_file):
        print(f"Setting up venv and installing requirements for {repo_name}")
        try:
            create_venv_and_install_requirements(repo_dir)
            git_metadata["status"] = "venv_and_requirements_installed"
            print(f"Successfully set up venv and installed requirements for {repo_name}")
        except subprocess.CalledProcessError as e:
            print(f"Error while setting up venv and installing requirements for {repo_name}: {e}")
            git_metadata["status"] = "error_while_setting_up_venv_and_installing_requirements"
    else:
        print(f"No requirements.txt found for {repo_name}. You can install dependencies manually.")
        git_metadata["status"] = "no_requirements_file"
    
    # add git_metadata.json file to dataset folder
    with open(os.path.join(data_dir, repo_name, "git_metadata.json"), "w") as git_metadata_file:
        json.dump(git_metadata, git_metadata_file)
        

print("Setup completed.")
