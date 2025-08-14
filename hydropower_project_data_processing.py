import os
import re
import pandas as pd
from pyproj import CRS, Transformer

# ──────── DMS to Decimal Degrees ────────
def dms_to_dd(dms_str):
    parts = re.findall(r'\d+\.?\d*', str(dms_str))
    if len(parts) == 3:
        d, m, s = map(float, parts)
        return d + m / 60 + s / 3600
    return None

# ──────── Everest → WGS84 CRS ────────
everest_crs = CRS.from_proj4("+proj=longlat +ellps=evrst30 +towgs84=293.17,726.18,245.36 +no_defs")
wgs84_crs = CRS.from_epsg(4326)
transformer = Transformer.from_crs(everest_crs, wgs84_crs, always_xy=True)

def transform_coords(lon_dd, lat_dd):
    return transformer.transform(lon_dd, lat_dd)

# ──────── Sheet Mapping (Default Excel names) ────────
sheet_map = {
    "Sheet1": "Survey",
    "Sheet2": "Construction_Application",
    "Sheet3": "Construction",
    "Sheet4": "Hydropower"
}

# ──────── Parent Folder ────────
root_dir = r"D:\HYDRO\From doed 2"

# ──────── Process Each Year Folder ────────
for folder in sorted(os.listdir(root_dir)):
    folder_path = os.path.join(root_dir, folder)
    if not os.path.isdir(folder_path) or not folder.isdigit():
        continue

    xlsx_file = os.path.join(folder_path, f"{folder}.xlsx")
    if not os.path.exists(xlsx_file):
        print(f" Missing: {xlsx_file}")
        continue

    print(f" Processing: {xlsx_file}")

    for input_sheet, output_name in sheet_map.items():
        try:
            df = pd.read_excel(xlsx_file, sheet_name=input_sheet)

            # Filter: Only keep rows where Capacity (MW) > 1 and not NaN
            df = df[pd.to_numeric(df["Capacity (MW)"], errors="coerce") > 1]

            rows = []
            for _, row in df.iterrows():
                try:
                    proj = str(row["Project"])
                    river = str(row["River"])
                    cap = float(row["Capacity (MW)"])
                    lon1 = dms_to_dd(row["Longitude 1"])
                    lon2 = dms_to_dd(row["Longitude 2"])
                    lat1 = dms_to_dd(row["Latitude 1"])
                    lat2 = dms_to_dd(row["Latitude 2"])

                    if None in (lon1, lon2, lat1, lat2):
                        continue

                    corners = [
                        (lon1, lat1),  # 1. top-left
                        (lon2, lat1),  # 2. top-right
                        (lon2, lat2),  # 3. bottom-right
                        (lon1, lat2)   # 4. bottom-left
                    ]

                    for i, (x, y) in enumerate(corners, start=1):
                        wgs_x, wgs_y = transform_coords(x, y)
                        rows.append({
                            "Project": f"{proj} ({cap} MW)",
                            "River": river,
                            "Capacity (MW)": cap,
                            "Order": i,
                            "WGS_Longitude": round(wgs_x, 6),  # X
                            "WGS_Latitude": round(wgs_y, 6)    # Y
                        })
                except:
                    continue

            # ─── Save each sheet to its own CSV file ───
            output_file = os.path.join(folder_path, f"{folder}_{output_name}.csv")
            pd.DataFrame(rows).to_csv(output_file, index=False)
            print(f" Saved: {output_file}")

        except Exception as e:
            print(f" Error processing sheet {input_sheet} in {folder}: {e}")
