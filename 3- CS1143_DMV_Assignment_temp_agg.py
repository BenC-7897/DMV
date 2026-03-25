import pandas as pd

folder_path = "temp_by_region_year"

years = range(1945, 2025)
dfs = []

for y in years:
    fname = folder_path / f"temp_region_year_{y}.csv"
    print(fname)
    if not fname.exists():
        print("WARNING: missing file", fname.name)
        continue

    print("Loading", fname.name)
    df = pd.read_csv(fname)
    dfs.append(df)

if dfs:
    temp_all = pd.concat(dfs, ignore_index=True)
    temp_all["year"] = temp_all["year"].astype(int)
    temp_all = temp_all.sort_values(["region", "year"]).reset_index(drop=True)

    out_path = f"{folder_path}/aggregates/temp_region_year_1945_2024_all_3.csv"
    temp_all.to_csv(out_path, index=False)
    print("Combined shape:", temp_all.shape)
    print("Saved", out_path)
else:
    print("No CSV files loaded.")

