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

def update_csv_patching_status():
    with open('notebooks.csv', 'r') as notebooks_csv:
        notebooks = csv.DictReader(notebooks_csv)
        notebook_paths = [row['Absolute Path'] for row in notebooks]

    with open('directories_info.csv', 'r') as dirs_csv:
        reader = csv.DictReader(dirs_csv)
        rows = list(reader)

    with open('directories_info.csv', 'w', newline='') as write_csv:
        writer = csv.DictWriter(write_csv, fieldnames=reader.fieldnames)
        writer.writeheader()
        
        for row in rows:
            dir_name = row['Directory Name']
            
            if any(dir_name in path for path in notebook_paths):
                print("Found:", dir_name)
                row['Status'] = 'Notebooks exist'
            else:
                print("Not found:", dir_name)  
                row['Status'] = 'No Notebooks'
                
            writer.writerow(row)

def edit_csv():
    # update the values of field "Directory Path" in all rows by replacing the start "../" with "/home/saurabh/method-energy-dataset/"
    with open('directories_info.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                print(row['Directory Path'])
                row['Directory Path'] = row['Directory Path'].replace('../', '/home/saurabh/method-energy-dataset/')
                print()
                with open('directories_info.csv', 'w', newline='') as csvfile:
                    fieldnames = ['Directory Name', 'Directory Path', 'Status']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for row in reader:
                        print("1")
                        writer.writerow(row)
        except Exception as e:
            print(e)


# Replace 'repositories_dir' with your desired path
repositories_dir = '../projects'
# create_csv_for_directories(repositories_dir)

# edit_csv()

update_csv_patching_status()
