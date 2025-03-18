# README for `result_folder_examples`

This directory contains **example RO-Crate result folders** from two different experiment runs. Each folder is named using a **timestamp (`YYYY-MM-DD_HH-MM-SS_xxxxxx`)**, and a **human-readable time format** is provided for reference.

---

## Experiment Folders

### 1. MoonGen Network Test
- **Folder:** `2025-03-18_12-00-36_925581`
- **Human-readable Time:** March 18, 2025, 12:00:36 PM
- **Related Tool:** [MoonGen (GitHub)](https://github.com/emmericp/MoonGen)
- **Description:**
This experiment uses **MoonGen**, a high-performance packet generator, to evaluate network performance. It includes energy measurements and system metadata collected during the test.

---

### 2. CPU Stress Test
- **Folder:** `2025-03-18_13-03-16_395230`
- **Human-readable Time:** March 18, 2025, 1:03:16 PM
- **Related Tool:** [`stress` (Linux Manual)](https://linux.die.net/man/1/stress)
- **Description:**
This experiment runs the **`stress`** tool to utilize **1, 2, 4, and 8 CPU cores**. The results include energy consumption data under different CPU loads to analyze power efficiency.

---

## Notes
- Each folder contains an **RO-Crate metadata file (`ro-crate-metadata.json`)**, experiment logs, and energy measurements.
- The experiment timestamp is embedded in the folder name and is converted to a **readable date format** above for convenience.

These example results can be used to test the energy measurement analysis tool.