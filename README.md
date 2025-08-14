# 🌱🌍♻️ Energy Analysis & Prediction Tools

This Jupyter-based toolset supports **energy analysis, modeling, and prediction** for network experiment testbeds. It utilizes [RO-Crate](https://www.researchobject.org/ro-crate/) metadata and CSV energy logs to generate rich visualizations, create machine learning models, and simulate power draw under configurable load conditions.

## Notebooks Overview

### 1. `evaluation.ipynb` — **Energy Data Visualization**

Analyzes raw energy CSV files for multiple nodes and runs.

#### Key Features

- Loads and processes CSV energy data dynamically.
- Extracts node-level metadata from `ro-crate-metadata.json`.
- Provides in-depth visualizations:
  - Power over time
  - Cumulative energy usage
  - Energy rate (mW/s)
  - Power vs. CPU load (if CPU data available)
  - Current and voltage trends
  - Per-node energy bar charts
- Generates formatted metadata summaries and clickable topology links.

> Input: `energy/` folder & `ro-crate-metadata.json`
> Output: Visual plots + metadata tables

### 2. `energy_model.ipynb` — **CPU Energy Modeling**

Fits regression models (linear/polynomial) to stress test results.

#### Key Features

- Uses stress-run outputs from previous testbed executions.
- Fits two model types:
  - **Linear (with or without idle intercept)**
  - **Polynomial (quadratic)**
- Stores each trained model as a `.json` file for later prediction.

> Input: CPU-only energy runs (per node)
> Output: Model file `cpu_model_<node>.json` stored in `data/cpu_models/`

### 3. `prediction.ipynb` — **Interactive Power Prediction**

Predicts server power draw using trained models and user-defined configurations.

#### Key Features

- Select multiple nodes to simulate total or individual power draw.
- For each node:
  - Choose active NICs
  - Set number of active CPU cores
  - Select target CPU load (0–100%)
- Visual prediction modes:
  - **Per-node stacked plots**
  - **System-wide stacked summary**
- Fully interactive and updates live on input change.

> Input: CPU model files (`cpu_model_<node>.json`)

> Output: Live power prediction visualizations

### 4. `api_integration.ipynb` — Publish RO-Crates to GreenDIGIT Catalogue

Extracts metadata from a local RO-Crate and publishes it to the GreenDIGIT catalogue using the gCat API.

#### Key Features

- Extracts title, description, keywords, and authors from ro-crate-metadata.json
- Prompts user to upload the zipped RO-Crate to their D4Science Workspace and input the public link
- Builds and submits a package_create-compatible metadata entry
- Automatically detects and prints the final dataset URL in the catalogue

> Input: RO-Crate folder (e.g. `./result_folder_examples/...`)

> Output: Published dataset visible at <<https://data.d4science.org/ctlg/GreenDIGIT/>...

## Setup & Requirements

### Dependencies

```bash
pip install pandas matplotlib seaborn
```

Or use the virtual environment setup:

```bash
python3 -m venv .venv_energy
source .venv_energy/bin/activate
pip install -r requirements.txt
```

## Folder Structure

```text
results/
  └── <timestamped_result_folder>/
        ├── energy/                    # CSV measurements per node
        ├── ro-crate-metadata.json    # RO-Crate metadata
        └── config/                   # Optional extra info (e.g., variable sets)

data/
  └── cpu_models/                     # Fitted model files for prediction
```

## Notebook Outputs

| Notebook           | Input                                | Output                                      |
|--------------------|---------------------------------------|---------------------------------------------|
| `evaluation`       | CSV + RO-Crate metadata               | Energy trend plots & hardware summary       |
| `energy_model`     | Energy runs from stress tests         | Fitted model `.json` files                  |
| `prediction`       | Model files + interactive inputs      | Live power prediction per scenario          |
| `api_integration`  | Local RO-Crate + public ZIP URL       | Dataset published to GreenDIGIT catalogue   |

## Preventing Unwanted Git Changes in Jupyter Notebooks

Jupyter notebooks track metadata such as `execution_count`, which can cause unnecessary changes in Git. To prevent Git from detecting these changes after each run, follow these steps:

### 1. Install `nbstripout`

`nbstripout` removes unnecessary metadata before committing:

```bash
pip install nbstripout
```

### 2. Enable `nbstripout` for Your Repository

Run the following command inside your Git repository:

```bash
nbstripout --install
```

### 3. Verify Installation

Check that `nbstripout` is active:

```bash
nbstripout --status
```

### 4. Configure Git to Ignore Execution Counts

Add the following rule to `.gitattributes` in your repository:

```bash
*.ipynb filter=jupyter
```

Then set up the Git filter:

```bash
git config filter.jupyter.clean nbstripout
git config filter.jupyter.smudge cat
```

Apply the filter to existing files (each time after execution the notebook):

```bash
git add --renormalize .
```

To automate it use pre-commit hooks.

### Alternative: Strip Metadata Manually

If you prefer a manual approach, you can clear metadata using `nbconvert` before committing:

```bash
jupyter nbconvert --ClearMetadataPreprocessor.enabled=True --to notebook --inplace my_notebook.ipynb
```

This ensures that execution counts and other unnecessary metadata do not clutter your Git history.
