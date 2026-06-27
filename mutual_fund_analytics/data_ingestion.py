import pandas as pd
import glob
import os

# Find all CSV files in your main folder
csv_files = glob.glob("*.csv")
print(f"--- Found {len(csv_files)} CSV files in your folder! ---")

# Loop through every single file and print its profile info
for file_path in csv_files:
    file_name = os.path.basename(file_path)
    try:
        df = pd.read_csv(file_path)
        print(f"\n=========================================")
        print(f"📁 FILE NAME: {file_name}")
        print(f"=========================================")
        print(f"📊 Dimensions (Rows, Columns): {df.shape}")
        print("\n⚙️ Column Data Types:")
        print(df.dtypes)
        print("\n👀 Sample Data (Top 3 Rows):")
        print(df.head(3))
    except Exception as e:
        print(f"❌ Error reading {file_name}: {e}")