# Greenlight

Greenlight is a repository for generating an energy consumption dataset for Python projects using the [codegreen](https://github.com/SMART-Dal/codegreen) tool.

## Installation

Clone the repository:

```bash
git clone https://github.com/user/Greenlight.git
cd Greenlight
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Greenlight provides a workflow to profile Python projects and generate an energy dataset:

### 1. Add Projects

Place projects to profile in `Projects/projects_to_measure/`. Each one should have its own subdirectory, which can be individial github repositories.

See `Projects/projects_to_measure/README.md` of the corresponding projects for guidelines.

### 2. Generate Dataset

The dataset generation involves 5 key scripts:

#### 01_clone_project.py

This clones the projects to profile from their repositories into the `Projects/` directory. 

By default, it will clone from `projects/projects.json`, which lists each project's git URL and other metadata.

#### 02_create_environments.py

This creates isolated virtual environments for each project cloned in the previous step.

Environments are created in `projects/project_name/` with the requirements installed.

#### 03_patch_project.py 

This instruments the project source code for energy profiling by invoking codegreen's `project-patcher` command.

The patched source files are written to `projects/` with `_patched` suffix.

#### 04_data_collection.py

This executes the patched project scripts and collects energy profiling data using codegreen's `start-energy-measurement` command.

The energy profiles are saved as JSON to `dataset/project_name/script_name/experiment-n.json`; this script also get the execution logs of the scripts and execution status metadata, for debugging and further analysis. The combined JSON files are at `analysis/cumulative_data`. These json files can be used to perform further analysis of the energy profiles.

#### 05_data_analysis.py

This analyzes the raw energy profiles to generate aggregated statistics and visualizations.

The analysis report and visualization are output to `Dataset/analysis/method-level/combined`. 

Additional analysis and visualization scripts are available in `codegreen.fecom.experiment` package, that can be for instance used as:

`from codegreen.fecom.experiment.analysis import init_project_energy_data, create_summary, export_summary_to_latex, build_total_energy_df`

In summary, the scripts handle:

- Cloning repositories 
- Isolating environments
- Instrumenting code
- Executing and collecting data
- Analyzing and outputting dataset

The result is an end-to-end pipeline to generate an energy profile dataset for Python projects using codegreen.

The final dataset json are output to `Dataset/final_dataset/`.

<!-- ### 3. Explore Dataset

Use the script `05_data_analysis.py` to explore the dataset. -->
<!--
## Contributing 

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding new projects to profile.
-->

## License

The Greenlight dataset is licensed under Apache 2.0. The tool Codegreen is licensed under the Apache 2.0. See [LICENSE](https://www.apache.org/licenses/LICENSE-2.0) for more details.
