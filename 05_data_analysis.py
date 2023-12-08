import datetime
import os
import subprocess
import json

#  analysis of the dataset

# crawl through dataset folder and read experiment-1.json file's content which is a list of dicts
# each dict contains the details of a single api call, merge these into a single list of dicts
energy_data = []
for root, dirs, files in os.walk('dataset'):
    for file in files:
        if file.endswith('experiment-1.json'):
            with open(os.path.join(root, file)) as f:
                data = json.load(f)
                # data is a list of dicts for api calls energy data, append to energy_data list
                energy_data.extend(data)

print(len(energy_data))
