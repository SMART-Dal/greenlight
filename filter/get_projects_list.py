import os
import csv

def create_csv_for_directories(path):
    with open('directories_info.csv', 'w', newline='') as csvfile:
        fieldnames = ['Directory Name', 'Directory Path', 'Status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for directory in os.listdir(path):
            dir_path = os.path.join(path, directory)
            if os.path.isdir(dir_path):
                writer.writerow({'Directory Name': directory, 'Directory Path': dir_path, 'Status': 'Pending'})

def update_csv_patching_status(path):
    pass

# Replace 'repositories_dir' with your desired path
repositories_dir = '../projects'
create_csv_for_directories(repositories_dir)
