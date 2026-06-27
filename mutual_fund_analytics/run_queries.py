import sqlite3
import pandas as pd

DB_PATH = "bluestock_mf.db"

def run_analysis():
    conn = sqlite3.connect(DB_PATH)
    
    queries = {
        "1. Top 5 Funds by Total Assets Under Management (AUM)": """
            SELECT f.scheme_name, a.total_aum 
            FROM fact_aum a
            JOIN dim_fund f ON a.amfi_code = f.amfi_code
            ORDER BY a.total_aum DESC 
            LIMIT 5;
        """,
        "2. Average Net Asset Value (NAV) per Month": """
            SELECT strftime('%Y-%m', date) as month, AVG(nav) as avg_nav
            FROM fact_nav
            GROUP BY month
            ORDER BY month DESC
            LIMIT 6;
        """,
        "3. Scheme Performance with High Expense Ratios (> 1%)": """
            SELECT f.scheme_name, p.expense_ratio, p.return_1yr
            FROM fact_performance p
            JOIN dim_fund f ON p.amfi_code = f.amfi_code
            WHERE p.expense_ratio > 1.0
            ORDER BY p.expense_ratio DESC
            LIMIT 5;
        """,
        "4. Investor Transaction Volume and Counts Grouped by State": """
            SELECT state, COUNT(*) as total_transactions, SUM(amount_inr) as total_volume_inr
            FROM fact_transactions
            GROUP BY state
            ORDER BY total_transactions DESC
            LIMIT 5;
        """,
        "5. Complete Volume & Value Breakdown of Transaction Types": """
            SELECT transaction_type, COUNT(*) as count, SUM(amount_inr) as total_amount_inr
            FROM fact_transactions
            GROUP BY transaction_type;
        """
    }
    
    print("📊 Executing Capstone Business Intelligence Queries...\n")
    
    for title, sql in queries.items():
        print(f"--- {title} ---")
        try:
            df = pd.read_sql_query(sql, conn)
            if df.empty:
                print("(No rows returned - check if related source dimension table is empty)\n")
            else:
                print(df.to_string(index=False))
                print("\n")
        except Exception as e:
            print(f"⚠️ Query execution failed: {e}\n")
            
    conn.close()

if __name__ == "__main__":
    run_analysis()