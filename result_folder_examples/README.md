# README for `result_folder_examples`

This directory contains **example RO-Crate result folders** from different experiment runs.
Each folder is named using a **timestamp (`YYYY-MM-DD_HH-MM-SS_xxxxxx`)**, and a **human-readable time format** is provided for reference.

---

## Experiment Folders

### 1. MoonGen Network Test
- **Folder:** `2025-03-18_12-00-36_925581`
- **Human-readable Time:** March 18, 2025, 12:00:36 PM
- **Related Tool:** [MoonGen (GitHub)](https://github.com/emmericp/MoonGen)
- **Description:**
  This experiment uses **MoonGen**, a high-performance packet generator, to evaluate network performance.
  It includes energy measurements and system metadata collected during the test.

---

### 2. CPU Stress Test
- **Folder:** `2025-03-18_13-03-16_395230`
- **Human-readable Time:** March 18, 2025, 1:03:16 PM
- **Related Tool:** [`stress` (Linux Manual)](https://linux.die.net/man/1/stress)
- **Description:**
  This experiment runs the **`stress`** tool to utilize **1, 2, 4, and 8 CPU cores**.
  The results include energy consumption data under different CPU loads to analyze power efficiency and build CPU power models.

---

### 3. GPU Stress Test (gpu-burn)
- **Folder:** `2026-01-20_12-29-40_302478`
- **Human-readable Time:** January 20, 2026, 12:29:40 PM
- **Related Tool:** [gpu-burn (GitHub)](https://github.com/wilicc/gpu-burn)
- **Description:**
  This experiment uses **gpu-burn** to generate controlled GPU load on a GPU-enabled testbed node.
  The workload is executed using a **duty-cycle approach** to emulate effective GPU load levels of:

  - **25%**
  - **50%**
  - **75%**
  - **100%**

  Energy measurements collected during these runs are used to **fit GPU power models**, analogous to the CPU stress-based modeling workflow.

---

## Notes

- Each folder contains:
  - an **RO-Crate metadata file (`ro-crate-metadata.json`)**
  - experiment logs
  - energy measurement CSV files
- The experiment timestamp is embedded in the folder name and converted to a **human-readable date format** above for convenience.
- These example results can be used to test:
  - energy evaluation and visualization
  - CPU and GPU power model generation
  - interactive power prediction tooling