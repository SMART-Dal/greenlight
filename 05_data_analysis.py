
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from codegreen.fecom.experiment.analysis import init_project_energy_data, create_summary, export_summary_to_latex, export_summary_to_csv, build_total_energy_df
from codegreen.fecom.experiment.experiment_kinds import ExperimentKinds
from pathlib import Path

#  analysis of the dataset

def get_energy_data():
    # crawl through dataset folder and read experiment-1.json file's content which is a list of dicts
    # each dict contains the details of a single api call, merge these into a single list of dicts
    for exper in range(1, 6):
        energy_data = []
        for root, dirs, files in os.walk('dataset'):
            for file in files:
                if file.endswith('experiment-'+str(exper)+'.json'):
                    with open(os.path.join(root, file)) as f:
                        data = json.load(f)
                        # data is a list of dicts for api calls energy data, append to energy_data list
                        energy_data.extend(data)

        print(len(energy_data))

        # write energy_data list to a json file names final_dataset.json
        with open('analysis/cumulative_data/experiment-'+str(exper)+'.json', 'w') as outfile:
            json.dump(energy_data, outfile)

    energy_data = []
    for root, dirs, files in os.walk('dataset'):
        for file in files:
            if file.endswith('skip_calls.json'):
                with open(os.path.join(root, file)) as f:
                    data = json.load(f)
                    # data is a list of dicts for api calls energy data, append to energy_data list
                    energy_data.extend(data)

    print(len(energy_data))

    # write energy_data list to a json file names final_dataset.json
    with open('analysis/cumulative_data/skip_calls.json', 'w') as outfile:
        json.dump(energy_data, outfile)

    #     # write energy_data list to a json file names final_dataset.json
    # with open('dataset/method-level/combined/final_dataset.json ', 'w') as outfile:
    #     json.dump(energy_data, outfile)

def energy_disribution():

    # Load CSVs into dataframes
    df_ram = pd.read_csv('analysis/method-level/combined/ram_summary_mean.csv') 
    df_cpu = pd.read_csv('analysis/method-level/combined/cpu_summary_mean.csv')
    df_gpu = pd.read_csv('analysis/method-level/combined/gpu_summary_mean.csv')

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
    # print("Standard deviation of total energy:", std_dev)

    mean = df_merged['total'].mean()

    # Print for validation
    print("Standard deviation:", std_dev)
    print("Mean:", mean)  
    print("Std dev percentage of mean:", (std_dev/mean)*100)

    # # Create box plot
    # fig, ax = plt.subplots()
    # ax.boxplot([df_ram['total'], df_cpu['total'], df_gpu['total']], labels=['RAM', 'CPU', 'GPU'])
    # ax.set_title('Energy Consumption by Hardware')
    # ax.set_ylabel('Energy (Joules)')
    # # plt.show()
    # plt.savefig('plot.pdf')

    # Create figure 
    fig, ax = plt.subplots()

    # Generate violin plot
    ax.violinplot([df_ram['total'], df_cpu['total'], df_gpu['total']], 
                showmeans=False,
                showmedians=True)

    # Set axis labels
    ax.set_ylabel('Energy (Joules)', fontsize=14)
    ax.set_xticks([1, 2, 3]) 
# ax.set_xticklabels(['RAM', 'CPU', 'GPU'], fontsize=14)
    ax.set_xticklabels(['RAM', 'CPU', 'GPU'], fontsize=14)

    # Remove title
    ax.set_title('')

    # Save figure
    plt.savefig('analysis/plot_violin.pdf', bbox_inches='tight')

def get_func_signatures():
    # read final_dataset.json that has list of dictionaries and create a list of all keys
    # unique_func = 0
    with open('dataset/final_dataset.json', 'r') as f:
        data = json.load(f)
        keys = []
        for d in data:
            for k in d.keys():
                if k not in keys:
                    keys.append(k)
    print(len(keys))


def create_summary_and_save_to_latex(project_name: str, experiment_kind: ExperimentKinds, first_experiment: int, last_experiment: int):
    data = init_project_energy_data(project_name, experiment_kind, first_experiment, last_experiment)
    summary_dfs = create_summary(data)
    LATEX_OUTPUT_PATH = Path("analysis")
    export_summary_to_latex(LATEX_OUTPUT_PATH/experiment_kind.value/project_name.replace('/','-'), summary_dfs=summary_dfs)
    export_summary_to_csv(LATEX_OUTPUT_PATH/experiment_kind.value/project_name.replace('/','-'), summary_dfs=summary_dfs)


def appendix_summary_dfs_all_experiments():
    first_exp = 1
    last_exp = 5
    project_name = "combined"
    create_summary_and_save_to_latex(project_name, ExperimentKinds.METHOD_LEVEL, first_exp, last_exp)


# create a main block to call all the functions
if __name__ == "__main__":
    # get_energy_data()
    # energy_disribution()
    # get_func_signatures()
    appendix_summary_dfs_all_experiments()
    pass
