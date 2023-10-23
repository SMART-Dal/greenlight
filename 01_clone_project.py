import json
import os

# Define the path to your local JSON file
json_file_path = "projects/projects.json"  # Replace with the actual path to your JSON file

# Define the target directory where repositories will be cloned
target_dir = "projects/"  # Replace with your target directory

# Make the target directory if it doesn't exist
# os.makedirs(target_dir, exist_ok=True)

# Read the JSON data from the local file
with open(json_file_path, "r") as json_file:
    data = json.load(json_file)

# Check if the 'items' key exists
if "items" in data:
    repositories = data["items"]
    for repo in repositories:
        repo_name = repo["name"]
        folder_name = repo_name.replace("/", "_")
        repo_url = f"https://github.com/{repo_name}.git"
        repo_folder = os.path.join(target_dir, folder_name)

        # Clone the repository and add the status of the clone to the JSON data
        try:
            os.system(f"git clone {repo_url} {repo_folder}")
            repo["status"] = "cloned"
            print(f"Cloned: {folder_name}")
        except Exception as e:
            repo["status"] = "failed"
            print(f"Failed: {folder_name} : " + str(e))
            continue

        # create a folder with same folder_name in dataset folder
        os.system(f"mkdir dataset/{folder_name}")

        # create a json file named git_metadata.json in dataset folder
        os.system(f"touch dataset/{folder_name}/git_metadata.json")

        # add a new key to repo object with value of repo_folder
        repo["repo_folder"] = repo_folder

        # add repo object to git_metadata.json file
        with open(f"dataset/{folder_name}/git_metadata.json", "w") as git_metadata_file:
            json.dump(repo, git_metadata_file)
else:
    print("No 'items' key found in the JSON data.")

print("Cloning completed.")
