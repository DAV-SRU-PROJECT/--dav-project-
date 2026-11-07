import pandas as pd
import numpy as np

# Read the CSV file
df = pd.read_csv("city.csv")
print("Original Dataset Shape:", df.shape)
print("\nMissing Values:")
print(df.isnull().sum())

# Remove duplicate rows
df = df.drop_duplicates()

# Remove extra spaces from column names
df.columns = df.columns.str.strip()

# Convert date column
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Convert pollution columns to numeric
pollutants = [
    "PM2.5", "PM10", "NO", "NO2", "NOx",
    "NH3", "CO", "SO2", "O3",
    "Benzene", "Toluene", "Xylene", "AQI"
]

for col in pollutants:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df.loc[df[col] < 0, col] = np.nan

# Fill missing numeric values with median
for col in df.select_dtypes(include="number").columns:
    median_value = df[col].median()
    if pd.notna(median_value):
        df[col] = df[col].fillna(median_value)

# Fill missing text values with mode
for col in df.select_dtypes(include=["object", "string"]).columns:
    mode_value = df[col].mode()
    if not mode_value.empty:
        df[col] = df[col].fillna(mode_value[0])

# Save cleaned data
df.to_csv("cleaned_city.csv", index=False)

print("\nCleaned Dataset Shape:", df.shape)
print("\nRemaining Missing Values:")
print(df.isnull().sum())
print("\nData cleaning completed successfully!")
print("Saved as cleaned_city.csv")