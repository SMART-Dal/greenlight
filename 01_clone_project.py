import json
import os

# Define the path to your local JSON file
json_file_path = "projects/results.json"  # Replace with the actual path to your JSON file

# Define the target directory where repositories will be cloned
target_dir = "projects/"  # Replace with your target directory

# Make the target directory if it doesn't exist
os.makedirs(target_dir, exist_ok=True)

# Read the JSON data from the local file
with open(json_file_path, "r") as json_file:
    data = json.load(json_file)

# Check if the 'items' key exists
if "items" in data:
    repositories = data["items"]
    for repo in repositories:
        repo_name = repo["name"]
        repo_url = f"https://github.com/{repo_name}.git"
        repo_folder = os.path.join(target_dir, repo_name)

        # Clone the repository
        os.system(f"git clone {repo_url} {repo_folder}")

        print(f"Cloned: {repo_name}")
else:
    print("No 'items' key found in the JSON data.")

print("Cloning completed.")
