# Energy Data Visualization

This Jupyter Notebook processes and visualizes energy measurement data from testbed experiments. It extracts energy metrics from CSV files and retrieves detailed node metadata from RO-Crate JSON files, including CPU, memory, NICs, and topology information.

## Features
•	Loads energy measurement data from multiple experiment runs.
•	Parses timestamps and associates data with respective nodes.
•	Extracts node metadata (FQDN, topology, CPU, memory, and NICs) from ro-crate-metadata.json.
•	Automatically detects available experiment runs and processes them dynamically.
•	Handles missing data gracefully, ensuring smooth execution.
•	Generates multiple visualizations:
•	Power consumption trends over time.
•	Cumulative energy counter trends for total energy usage.
•	Current and voltage trends to analyze stability.
•	Formats node metadata output, including:
•	Clickable topology links (if available).
•	Structured hardware details (CPU, RAM, NICs).
•	Automatic summary of system-wide specs.

## File Structure
•	Energy CSV files are stored inside:
```
/srv/testbed/results/warmuth/default/energy/
```
•	RO-Crate metadata is stored in:
```
/srv/testbed/results/warmuth/default/ro-crate-metadata.json
```
•	Topology files are referenced inside ro-crate-metadata.json and extracted dynamically.

## Requirements

```
pip install pandas matplotlib seaborn
````

## Usage

Run the Jupyter Notebook and specify the experiment folder when prompted.
If only the timestamp (YYYY-MM-DD_HH-MM-SS_xxxxxx) is provided, the script automatically prepends the base path.

Output
	•	Plots:
	•	Time-series visualizations of power, current, voltage, and energy trends.
	•	Comparison of energy usage across nodes.
	•	Node Metadata Report:
	•	Extracted and formatted node details (FQDN, CPU, RAM, NICs).
	•	Clickable links to topology PDFs (if available).
	•	Summary table with system-wide stats (total cores, RAM, unique CPUs).

## Example Output

### Extracted Node Metadata Table

| Name  | FQDN           | Topology                          | CPU                        | Cores | Threads | Memory      | NICs                           |
|-------|--------------|--------------------------------|---------------------------|-------|---------|------------|--------------------------------|
| Node1 | node1.testbed | [Open PDF](path/to/topology1.pdf) | Xeon E31230 @ 3.20GHz      | 4     | 8       | RAM: 16 GiB | Intel 82574L, Broadcom NetXtreme |
| Node2 | node2.testbed | No topology available          | Xeon E31230 @ 3.20GHz                 | Unknown | Unknown | Unknown      | No NICs detected               |
