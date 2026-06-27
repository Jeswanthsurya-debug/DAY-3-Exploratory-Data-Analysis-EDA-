import pandas as pd

print("=========================================")
print("🔍 STEP 1: EXPLORING FUND MASTER DATA")
print("=========================================")

# Load datasets safely
master_df = pd.read_csv("01_fund_master.csv")
live_df = pd.read_csv("live_nav_history.csv")

# Dynamically find the correct column names by checking what exists
master_cols = [c.lower().strip() for c in master_df.columns]
live_cols = [c.lower().strip() for c in live_df.columns]

# Standardize data columns to lowercase for mapping
master_df.columns = master_cols
live_df.columns = live_cols

print("📁 Found columns in Fund Master:", list(master_df.columns))
print("📁 Found columns in Live NAV History:", list(live_df.columns))

# Find the AMC/Fund House column dynamically
amc_col = next((c for c in master_df.columns if 'amc' in c or 'house' in c or 'provider' in c), None)
if amc_col:
    print(f"\n🏢 Unique Fund Houses Available ({amc_col}):")
    print(master_df[amc_col].unique())

# Print other unique categories if they exist
for col in ['category', 'sub_category', 'risk_grade', 'scheme_type', 'risk']:
    if col in master_df.columns:
        print(f"🔹 Unique {col}: {master_df[col].unique()}")

print("\n=========================================")
print("🛡️ STEP 2: VALIDATING AMFI SCHEME CODES")
print("=========================================")

# Dynamically find the scheme/amfi code column name in both files
master_code_col = next((c for c in master_df.columns if 'code' in c or 'amfi' in c or 'id' in c), None)
live_code_col = next((c for c in live_df.columns if 'code' in c or 'amfi' in c or 'id' in c), None)

if master_code_col and live_code_col:
    master_codes = set(master_df[master_code_col].astype(str).unique())
    live_codes = set(live_df[live_code_col].astype(str).unique())

    print(f"📌 Using column '{master_code_col}' for Master Codes.")
    print(f"📌 Using column '{live_code_col}' for Live Codes.")
    print(f"🔢 Key Codes in Master List: {master_codes}")
    print(f"🔢 Key Codes in Live Fetched Data: {live_codes}")

    # Check for mismatches
    missing_in_live = master_codes - live_codes

    print("\n📈 Validation Report:")
    if len(missing_in_live) == 0:
        print("✅ DATA INTEGRITY VERIFIED: Every code in fund_master matches up perfectly with nav_history!")
    else:
        print(f"⚠️ Anomaly Detected: The following codes are in master but missing from live timeline: {missing_in_live}")
else:
    print("❌ Could not automatically detect a code/amfi/id column to link the tables.")