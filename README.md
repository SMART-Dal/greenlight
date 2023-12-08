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

Place projects to profile in `Projects/projects_to_measure/`. Each one should have its own subdirectory.

See `Projects/projects_to_measure/README.md` for guidelines.

Here is an expanded "Generate Dataset" section explaining each script individually:

### 2. Generate Dataset

The dataset generation involves 5 key scripts:

#### 01_clone_project.py

This clones the projects to profile from their repositories into the `Projects/` directory. 

By default, it will clone from `projects/projects.json`, which lists each project's git URL.

#### 02_create_environments.py

This creates isolated virtual environments for each project cloned in the previous step.

Environments are created in `projects/project_name/` with the requirements installed.

#### 03_patch_project.py 

This instruments the project source code for energy profiling by invoking codegreen's `project-patcher` command.

The patched source files are written to `projects/` with `_patched` suffix.

#### 04_data_collection.py

This executes the patched project scripts and collects energy profiling data using codegreen's `start-energy-measurement` command.

The energy profiles are saved as JSON to `dataset/project_name/script_name`; this script also get the execution logs of the scripts and execution status metadata.

#### 05_data_analysis.py

This analyzes the raw energy profiles to generate aggregated statistics and visualizations.

The final dataset json and plots are output to `Dataset/final_dataset/`.

In summary, the scripts handle:

- Cloning repositories 
- Isolating environments
- Instrumenting code
- Executing and collecting data
- Analyzing and outputting dataset

The result is an end-to-end pipeline to generate an energy profile dataset for Python projects using codegreen.

The final dataset will be located in `dataset/`.

### 3. Explore Dataset

Use the Jupyter notebooks in `analysis/` to explore the dataset.

## Contributing 

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding new projects to profile.

## License

The Greenlight dataset is licensed under Apache 2.0. codegreen is licensed under the Apache 2.0. See [LICENSE](https://github.com/SMART-Dal/codegreen/blob/main/LICENSE) for more details.
