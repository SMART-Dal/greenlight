
import os
import json
import pandas as pd
import matplotlib.pyplot as plt

#  analysis of the dataset

def get_energy_data():
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

    # write energy_data list to a json file names final_dataset.json
    with open('final_dataset.json', 'w') as outfile:
        json.dump(energy_data, outfile)

def energy_disribution():

    # Load CSVs into dataframes
    df_ram = pd.read_csv('analysis/ram_summary_mean.csv') 
    df_cpu = pd.read_csv('analysis/cpu_summary_mean.csv')
    df_gpu = pd.read_csv('analysis/gpu_summary_mean.csv')

    # Merge dataframes on 'function' column 
    df_merged = df_ram.merge(df_cpu, on='function')
    df_merged = df_merged.merge(df_gpu, on='function')

    df_low = pd.DataFrame(columns=['function', 'total']) 

    # Add rows with zero or low value for total energy 
    for i in range(1000):
        new_data = pd.DataFrame({'function': 'api_call_'+str(i), 'total': 0.0}, index=[0])
        df_low = pd.concat([df_low, new_data])

    # Calculate total energy per API call
    df_merged['total'] = df_merged['total_x'] + df_merged['total_y'] + df_merged['total']
    df_merged = pd.concat([df_merged, df_low])
    # print schema of df_merged
    print(df_merged.columns)

    # Calculate standard deviation
    std_dev = df_merged['total'].std()
    print("Standard deviation of total energy:", std_dev)

    # Create box plot
    fig, ax = plt.subplots()
    ax.boxplot([df_ram['total'], df_cpu['total'], df_gpu['total']], labels=['RAM', 'CPU', 'GPU'])
    ax.set_title('Energy Consumption by Hardware')
    ax.set_ylabel('Energy (Joules)')
    # plt.show()
    plt.savefig('plot.pdf')

# create a main block to call all the functions
if __name__ == "__main__":
    # get_energy_data()
    energy_disribution()
    pass
