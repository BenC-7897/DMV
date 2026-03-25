import pandas as pd

# load interpolated temperature data
temp_path = r"Data_Final/temp_region_year_1945_2024_INTERPOLATED.csv"

temp_df = pd.read_csv(temp_path)
print("Loaded temperature data shape:", temp_df.shape)

# load CO2 data aggregated by region and year
co2_path = r"Data_Final/co2_region_year_10regions.csv"
co2_df = pd.read_csv(co2_path)
print("Loaded CO2 data shape:", co2_df.shape)

# Merge temperature and CO2 data on region and year
merged_df = pd.merge(
    temp_df,
    co2_df,
    on=["region", "year"],
    how="inner"  # only keep rows with both temp and CO2 data
)
print("Merged data shape:", merged_df.shape)
# Save merged data to CSV
output_path = r"Data_Final/temp_co2_region_year_1945_2024.csv"
merged_df.to_csv(output_path, index=False)
print("Saved merged data to:", output_path)

