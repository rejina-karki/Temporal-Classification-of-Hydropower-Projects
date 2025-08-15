# Temporal Classification of Hydropower Projects

## Purpose
Process hydropower project data from the **Department of Electricity Development (DoED) of Nepal**.

## Functionality
- Converts coordinates from **Everest 1830 (DMS)** to **WGS84 (decimal degrees)**.
- Filters projects with **capacity > 1 MW**.
- Categorizes data into:
  - **Survey**
  - **Construction Application**
  - **Construction**
  - **Hydropower**
- Outputs cleaned **CSV files** for each category and year.

## Requirements
- Python **3.x**
- Libraries:
  - `pandas`
  - `pyproj`

## How to Run
1. Place yearly Excel files in folders named by year (e.g., `2015`, `2020`).
2. Update `root_dir` in the script with your data path.
3. Run:
   ```bash
   python hydropower_project_data_processing.py
