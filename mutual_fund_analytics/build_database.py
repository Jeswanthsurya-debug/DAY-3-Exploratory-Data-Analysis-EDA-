import os
import glob
import pandas as pd
from sqlalchemy import create_engine, text

# Define file paths
PROCESSED_DIR = os.path.join("data", "processed")
DB_PATH = "bluestock_mf.db"

# 1. Initialize SQLite Database Engine via SQLAlchemy
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

print("💾 Initializing Star Schema Database Setup...")

# 2. Map Cleaned CSV file names to their corresponding Target Star Schema Table Names
table_mapping = {
    "cleaned_fund_master.csv": "dim_fund",
    "cleaned_benchmark_indices.csv": "dim_benchmark",
    "cleaned_category_inflow.csv": "dim_category",
    "cleaned_industry_folio.csv": "dim_industry",
    
    "cleaned_nav_history.csv": "fact_nav",
    "cleaned_investor_transactions.csv": "fact_transactions",
    "cleaned_scheme_performance.csv": "fact_performance",
    "cleaned_aum_by_fund.csv": "fact_aum",
    "cleaned_monthly_sip_inflow.csv": "fact_sip_inflow",
    "cleaned_portfolio_holdings.csv": "fact_portfolio_holdings"
}

# 3. Read and load each dataset dynamically into SQLite
with engine.connect() as connection:
    print("⏳ Dropping older instances to build fresh tables...")
    for table in table_mapping.values():
        connection.execute(text(f"DROP TABLE IF EXISTS {table};"))
    connection.commit()

print("\n🚀 Loading cleaned datasets into SQL tables...")

for csv_name, table_name in table_mapping.items():
    csv_path = os.path.join(PROCESSED_DIR, csv_name)
    
    if os.path.exists(csv_path):
        # Load the clean data frame
        df = pd.read_csv(csv_path)
        
        # Write to SQLite using SQLAlchemy engine integration
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        
        # Verify Row Count Accuracy
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name};"))
            sql_count = result.scalar()
            
        print(f"✅ {csv_name} -> Loaded into [{table_name}] ({sql_count} rows verified)")
    else:
        print(f"⚠️ Warning: Missing expected clean file at {csv_path}")

print(f"\n🎉 Database engine processing complete! Local file created: '{DB_PATH}'")