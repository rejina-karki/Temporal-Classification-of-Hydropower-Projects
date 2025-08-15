Purpose: Process hydropower project data from the Department of Electricity Development (DoED) of Nepal.

Functionality:

Converts coordinates from Everest 1830 (DMS) to WGS84 (decimal degrees).

Filters projects with capacity > 1 MW.

Categorizes data into:

Survey

Construction Application

Construction

Hydropower

Outputs cleaned CSV files for each category and year.

Requirements:

Python 3.x

pandas, pyproj

How to Run:

Place yearly Excel files in folders named by year (e.g., 2015, 2020).

Update root_dir in the script with your data path.

Run:

python hydropower_project_data_processing.py


CSV files will be saved in the same folder as the original Excel.

Output:

CSV files with WGS84 decimal degree coordinates.

One file per category, per year.
