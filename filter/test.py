import csv

directory_names = []

# get directories_info.csv and read directory name from "Directory name" column field into a list
with open("notebooks.csv", 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    # read value of "Directory name" column and append to list and move to next row
    for row in reader:
        # if row[2]== "Notebooks exist":
        directory_names.append(row[0])

print(len(directory_names))