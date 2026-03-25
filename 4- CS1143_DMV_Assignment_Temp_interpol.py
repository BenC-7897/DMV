import pandas as pd

# ---------- 1. Load original temperature data ----------

# Adjust this path if needed
input_path = r"Data_Final/temp_region_year_1945_2024.csv"

temp_df = pd.read_csv(input_path)

# Sanity check
print("Original shape:", temp_df.shape)
print("Regions:", sorted(temp_df["region"].unique()))
print("Year range:", temp_df["year"].min(), "→", temp_df["year"].max())

# ---------- 2. Define full year range and regions ----------

full_years = pd.Series(range(1945, 2025), name="year")  # 1945..2024 inclusive
regions = temp_df["region"].unique()

interpolated_list = []

# ---------- 3. Interpolate per region ----------

for region in regions:
    df_r = temp_df[temp_df["region"] == region].copy()

    # Reindex to all years for this region
    # We merge full_years with this region's data on 'year'
    df_full = (
        pd.DataFrame({"year": full_years})
        .merge(df_r, on="year", how="left")
    )

    # Make sure region column is set (will be NaN for missing years)
    df_full["region"] = region

    # Interpolate temperature columns (linear, both directions)
    # This fills internal gaps and also extrapolates at the edges
    df_full["temp_mean_c"] = df_full["temp_mean_c"].interpolate(
        method="linear", limit_direction="both"
    )
    df_full["temp_mean_f"] = df_full["temp_mean_f"].interpolate(
        method="linear", limit_direction="both"
    )

    interpolated_list.append(df_full)

# ---------- 4. Combine all regions back ----------

temp_interpolated = pd.concat(interpolated_list, ignore_index=True)

# Sort for cleanliness
temp_interpolated = temp_interpolated.sort_values(
    ["region", "year"]
).reset_index(drop=True)

print("Interpolated shape:", temp_interpolated.shape)

# Optional quick check: any remaining NaNs?
print("NaNs after interpolation:\n", temp_interpolated.isna().sum())

# ---------- 5. Save to new CSV ----------

output_path = r"Data_Final/temp_region_year_1945_2024_INTERPOLATED.csv"
temp_interpolated.to_csv(output_path, index=False)
print("Saved:", output_path)
