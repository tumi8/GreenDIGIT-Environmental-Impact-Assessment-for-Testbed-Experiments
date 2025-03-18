# **Energy Data Visualization**

This Jupyter Notebook processes and visualizes **energy measurement data** from testbed experiments. It extracts **energy metrics** from CSV files and retrieves **detailed node metadata** from RO-Crate JSON files, including CPU, memory, NICs, and topology information.

---

## **Features**
- **Loads energy measurement data** from multiple experiment runs.
- **Parses timestamps** and associates data with respective nodes.
- **Extracts node metadata** (FQDN, topology, CPU, memory, and NICs) from `ro-crate-metadata.json`.
- **Automatically detects available experiment runs** and processes them dynamically.
- **Handles missing data gracefully**, ensuring smooth execution.
- **Generates multiple visualizations** for energy analysis:
  - **Power consumption trends over time**.
  - **Cumulative energy counter trends for total energy usage**.
  - **Energy consumption rate (mW/s) to detect workload changes**.
  - **Power vs. CPU Load (if CPU usage data is available)**.
  - **Current and voltage trends to analyze stability**.
  - **Total energy used per node for quick comparison**.
- **Formats node metadata output**, including:
  - **Clickable topology links (if available)**.
  - **Structured hardware details (CPU, RAM, NICs)**.
  - **Automatic summary of system-wide specs**.

---

## **File Structure**
- **Energy CSV files** are stored inside:
```
<path_to_result_folder>/energy/
```
- **RO-Crate metadata** is stored in:
```
<path_to_result_folder>/ro-crate-metadata.json
```
- **Topology files** are referenced inside `ro-crate-metadata.json` and extracted dynamically.

---

## **Requirements**
Install required Python libraries:
For local execution of Juypter Notebook you need the jupyter kernel as well.
```
pip install pandas matplotlib seaborn
```
Or use the `requirements.txt` for all needed packages at once:
```
pip install -r requirements.txt
```

---

## **Usage**
Run the Jupyter Notebook and **specify the experiment folder** when prompted.
If only the **timestamp (`YYYY-MM-DD_HH-MM-SS_xxxxxx`)** is provided, the script automatically **prepends the base path**. This only works if executed from the management host of the testbed. Otherwise just provide the full path to the result folder.

---

## **Output**

### **Creator Information**
- **Name**
- **ORCID (clickable link to researcher profile)**
- **Affiliation (clickable link to organization)**

### **Plots & Their Purpose**

| **Plot Name**                                | **Description** |
|---------------------------------------------|---------------|
| **Power Consumption Over Time**             | Shows how power draw (W) changes over time for each node and experiment run. |
| **Cumulative Energy Consumption (mWh)**     | Tracks how much total energy has been used over time. |
| **Energy Consumption Rate (mW/s)**    | Shows the rate at which energy is being consumed per second. |
| **Power vs. CPU Load [If CPU data available]** | Compares power draw against CPU utilization, useful for efficiency analysis. |
| **Current Trend Over Time**                 | Shows how much electrical current (mA) was drawn over time. |
| **Voltage Trend Over Time**                 | Displays voltage variations, usually stable unless there is a power issue. |
| **Total Energy Used Per Node**        | A bar chart comparing the total energy consumption of different test setups. |

---

## **Node Metadata**
- Extracted and formatted **node details** (FQDN, CPU, RAM, NICs).
- **Clickable links** to topology PDFs (if available).
- **Summary table** with system-wide specs (**total cores, RAM, unique CPUs**).

---

## **Example Output**

### **Extracted Node Metadata Table**

| Name  | FQDN           | Topology                          | CPU                        | Cores | Threads | Memory      | NICs                           |
|-------|--------------|--------------------------------|---------------------------|-------|---------|------------|--------------------------------|
| Node1 | node1.testbed | [Open PDF](path/to/topology1.pdf) | Xeon E31230 @ 3.20GHz      | 4     | 8       | RAM: 16 GiB | Intel 82574L, Broadcom NetXtreme |
| Node2 | node2.testbed | No topology available          | Xeon E31230 @ 3.20GHz                 | Unknown | Unknown | Unknown      | No NICs detected               |
