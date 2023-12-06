import os
import csv

notebook_rows = []

# Path to search  
root_dir = '/home/saurabh/method-energy-dataset/projects'

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".ipynb"):

            # Get directory info
            dir_name = os.path.basename(root)
            dir_path = root
            
            # Construct row
            row = {
                "Filename": file,
                "Absolute Path": os.path.join(root, file),
                "Directory Name": dir_name,
                "Directory Path": dir_path, 
                "Status": "Pending",
                "Patching_status": "Pending"
            }
            
            # Append row to list
            notebook_rows.append(row)

# Write rows to CSV             
with open("notebooks.csv", 'w', newline='') as csvfile:
    fieldnames = ['Filename','Absolute Path','Directory Name','Directory Path', 'Status', 'Patching_status']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
              
    writer.writeheader()
    for row in notebook_rows:
        writer.writerow(row)
        
print("Done")

import csv

# Replace 'file.csv' with your CSV file path
file_path = 'notebooks.csv'

# Open the CSV file in read mode
with open(file_path, 'r', newline='') as file:
    # Create a CSV reader object
    reader = csv.reader(file)
    
    # Calculate the number of rows
    num_rows = sum(1 for row in reader)

# Print the number of rows
print(f"Number of rows in {file_path}: {num_rows}")
