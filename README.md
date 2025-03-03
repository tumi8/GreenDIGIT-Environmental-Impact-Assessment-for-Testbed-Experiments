# Energy Data Visualization

This Jupyter Notebook script processes and visualizes energy measurement data from testbed experiments. It extracts energy metrics from CSV files and retrieves node metadata from RO-Crate JSON files.

## Features
- Loads energy measurement data from multiple experiment runs.
- Parses timestamps and associates data with respective nodes.
- Extracts node metadata (FQDN, topology) from `ro-crate-metadata.json`.
- Generates visualizations for:
  - Power consumption trends
  - Cumulative energy counter trends
  - Current and voltage trends

## File Structure
- **Energy CSV files** are stored inside:
  ```
  /srv/testbed/results/warmuth/default/2025-02-26_18-06-05_836417/energy/<node>/
  ```
- **RO-Crate metadata** is stored in:
  ```
  /srv/testbed/results/warmuth/default/2025-02-26_18-06-05_836417/ro-crate-metadata.json
  ```
- **Topology files** are referenced inside `ro-crate-metadata.json` and extracted dynamically.

## Installation
Ensure you have the required Python libraries:
```
pip install pandas matplotlib seaborn
```

## Usage
Run the script in a Jupyter Notebook or as a standalone Python script.

### 1. Load and Visualize Energy Data
```
df = load_energy_data()
plot_energy_data(df)
```

### 2. Extract Node Metadata
```
nodes_info = load_rocrate_metadata()
for node in nodes_info:
    print(f"Node: {node['name']}, FQDN: {node['fqdn']}")
    print(f"Topology Data:\n{node['topology']}\n")
```

## Output
- **Plots:** Time-series visualizations of power, current, voltage, and energy trends.
- **Node Metadata:** Extracted and printed node details, including topology information.
