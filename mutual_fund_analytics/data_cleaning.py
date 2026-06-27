import os
import glob
import pandas as pd
import numpy as np

# Set paths matching your newly created terminal folders
RAW_DIR = "."
PROCESSED_DIR = os.path.join("data", "processed")

print("🚀 Starting Complete Capstone Data Cleaning Pipeline...")

# Find all 10 raw CSV files in your workspace
csv_files = sorted(glob.glob(os.path.join(RAW_DIR, "0*.csv")) + glob.glob(os.path.join(RAW_DIR, "10_*.csv")))
print(f"📋 Found {len(csv_files)} source files to clean.\n")

for file_path in csv_files:
    file_name = os.path.basename(file_path)
    print(f"⏳ Cleaning file: {file_name}...")
    df = pd.read_csv(file_path)
    
    # Standardize Column Names (Strip unwanted whitespaces)
    df.columns = df.columns.str.strip()
    
    # Strip spaces from any text columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()
        
    # Drop completely duplicate rows
    df = df.drop_duplicates()
    
    # --- IMPLEMENTING TARGETED BLUESTOCK DATA CLEANING RULES ---
    
    # 1. Clean NAV History (02_nav_history.csv)
    if "nav_history" in file_name or "02_" in file_name:
        if 'date' in df.columns and 'amfi_code' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values(by=['amfi_code', 'date']).reset_index(drop=True)
            df['nav'] = df.groupby('amfi_code')['nav'].ffill()
            df = df[df['nav'] > 0]
            
    # 2. Clean Investor Transactions (08_investor_transactions.csv)
    elif "investor_transactions" in file_name or "08_" in file_name:
        if 'transaction_type' in df.columns:
            df['transaction_type'] = df['transaction_type'].str.capitalize()
            type_mapping = {'Sip': 'SIP', 'Lump sum': 'Lumpsum', 'Lumpsum': 'Lumpsum', 'Redemption': 'Redemption'}
            df['transaction_type'] = df['transaction_type'].map(type_mapping).fillna(df['transaction_type'])
        if 'amount' in df.columns:
            df = df[df['amount'] > 0]
        if 'transaction_date' in df.columns:
            df['transaction_date'] = pd.to_datetime(df['transaction_date']).dt.strftime('%Y-%m-%d')
        if 'kyc_status' in df.columns:
            df['kyc_status'] = df['kyc_status'].str.upper()
            
    # 3. Clean Scheme Performance (07_scheme_performance.csv)
    elif "scheme_performance" in file_name or "07_" in file_name:
        return_cols = [col for col in df.columns if 'return' in col.lower() or 'cagr' in col.lower()]
        for col in return_cols:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace('%', ''), errors='coerce').fillna(0.0)
        if 'expense_ratio' in df.columns:
            df['expense_ratio'] = pd.to_numeric(df['expense_ratio'].astype(str).str.replace('%', ''), errors='coerce')
            df['expense_ratio'] = df['expense_ratio'].clip(lower=0.1, upper=2.5)
            
    # 4. Standard Fallback Cleaning for Dimension Files (01, 03, 04, 05, 06, 09, 10)
    else:
        for col in df.select_dtypes(include=[np.number]).columns:
            df[col] = df[col].fillna(0)
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].replace('nan', 'Unknown').fillna('Unknown')

    # Assign output names with a unified 'cleaned_' prefix
    clean_name = f"cleaned_{file_name.split('_', 1)[-1]}" if file_name[0].isdigit() else f"cleaned_{file_name}"
    output_path = os.path.join(PROCESSED_DIR, clean_name)
    
    # Save processed dataset
    df.to_csv(output_path, index=False)
    print(f"✅ Saved clean file: {output_path}\n")

print("🎉 Complete automated dataset cleaning executed successfully, bro!")